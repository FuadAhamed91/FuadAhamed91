"""Purple Team: a particle iris rendered with real optics.

~400k emitters flow inward along iris fibres. Blue (defence) at the rim, red (offence) at the core,
violet where they meet. Every frame is rendered with:
  * a pinhole camera and per-particle circle of confusion (layered depth of field, disc bokeh),
  * motion blur (several sub-frame samples across a 180 degree shutter),
  * bloom, a soft anamorphic streak and ACES tone mapping.
Every motion is periodic in T seconds, so the animation loops seamlessly.
"""
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import fftconvolve

TAU = 2 * np.pi

# radial palette, linear RGB: pupil -> rim -> outer feeders
PAL_R = np.array([0.20, 0.25, 0.34, 0.48, 0.66, 0.90, 1.30, 2.40])
PAL_C = np.array([
    (1.00, 0.42, 0.22),  # ember at the pupil
    (1.00, 0.09, 0.08),  # crimson
    (0.95, 0.04, 0.30),  # magenta
    (0.52, 0.12, 1.00),  # violet
    (0.20, 0.30, 1.00),  # blue
    (0.22, 0.55, 1.00),  # ice
    (0.30, 0.55, 1.00),
    (0.50, 0.55, 0.95),
])

LAYER_SIG = np.array([0.5, 0.9, 1.5, 2.4, 3.8, 6.0, 9.5, 15.0, 24.0, 38.0])
DISC_FROM = 6  # layers with sigma >= LAYER_SIG[DISC_FROM] use a disc (bokeh) kernel


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def palette(r):
    out = np.empty(r.shape + (3,))
    for c in range(3):
        out[..., c] = np.interp(r, PAL_R, PAL_C[:, c])
    return out


def disc_kernel(radius):
    n = int(np.ceil(radius)) + 2
    y, x = np.mgrid[-n:n + 1, -n:n + 1]
    d = np.sqrt(x * x + y * y)
    k = np.clip(radius + 0.5 - d, 0, 1)          # anti-aliased edge
    k *= 0.85 + 0.15 * (d / max(radius, 1)) ** 4  # slightly brighter rim, like real bokeh
    return k / k.sum()


def aces(x):
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)


def to_srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)


class Scene:
    def __init__(self, W=1600, H=500, T=8.0, tilt_deg=63.0, center_px=(1135, 252), R_px=520.0,
                 Z0=6.0, aperture=0.042, seed=7, n_fib=1600, per_fib=230, n_bg=50000, n_fg=16,
                 sway=0.028, margin=56, streak=0.07, anomaly=True, burst=True, fg_xmin=0.45):
        self.W, self.H, self.T, self.M = W, H, T, margin
        self.f = R_px * Z0
        self.Z0 = Z0
        self.tilt = np.radians(tilt_deg)
        self.C = np.array([(center_px[0] - W / 2) / self.f * Z0, (center_px[1] - H / 2) / self.f * Z0, Z0])
        self.ap = aperture
        self.sway = sway
        self.streak = streak
        self.anomaly_on = anomaly
        self.burst_on = burst
        self.rp = 0.20
        rng = np.random.default_rng(seed)

        # ---- iris fibres -------------------------------------------------------------------
        n_bundle = n_fib // 6
        spacing = TAU / n_bundle
        bc = (np.arange(n_bundle) + rng.uniform(-0.3, 0.3, n_bundle)) * spacing
        bid = rng.integers(0, n_bundle, n_fib)
        th = bc[bid] + rng.normal(0, 0.28 * spacing, n_fib)
        bright = rng.lognormal(0, 0.7, n_fib) * rng.lognormal(0, 0.45, n_bundle)[bid]
        rs = 1.0 + rng.exponential(0.05, n_fib)
        feeder = rng.random(n_fib) < 0.14
        rs[feeder] = rng.uniform(1.25, 2.4, feeder.sum())
        bright[feeder] *= 0.45
        self.f_th, self.f_br, self.f_rs = th, bright, rs
        self.f_wa = rng.uniform(0.004, 0.02, n_fib)
        self.f_wf = rng.uniform(1.5, 6.0, n_fib)
        self.f_wp = rng.uniform(0, TAU, n_fib)

        n = n_fib * per_fib
        self.fid = np.repeat(np.arange(n_fib), per_fib)
        self.s0 = rng.random(n)
        self.k = rng.choice([1, 2], n, p=[0.55, 0.45]).astype(float)
        self.jit = rng.normal(0, 1, n)
        self.zz = rng.normal(0, 1, n)
        self.flux = rng.lognormal(0, 0.75, n) * self.f_br[self.fid]
        self.white = rng.random(n) ** 8

        # ---- anomaly (one red packet with a comet trail) ------------------------------------
        na = 1400
        self.a_dt = rng.exponential(0.35, na).clip(0, 1.6)
        self.a_off = rng.normal(0, 1, (na, 3))
        self.a_flux = rng.lognormal(0, 0.5, na)
        self.a_th0 = np.radians(-95)  # enters at the far (top) rim

        # ---- containment burst ring -----------------------------------------------------------
        nb = 5000
        self.b_th = rng.uniform(0, TAU, nb)
        self.b_dr = rng.normal(0, 1, nb)
        self.b_flux = rng.lognormal(0, 0.5, nb)

        # ---- background events (stars) and foreground bokeh ---------------------------------
        Zb = rng.uniform(9, 45, n_bg)
        half_w = (W / 2 + margin) / self.f * Zb * 1.05
        half_h = (H / 2 + margin) / self.f * Zb * 1.05
        self.bg = np.stack([rng.uniform(-1, 1, n_bg) * half_w, rng.uniform(-1, 1, n_bg) * half_h, Zb], 1)
        self.bg_flux = rng.lognormal(-0.2, 1.0, n_bg) * 0.5
        mix = rng.random(n_bg)[:, None]
        self.bg_col = (1 - mix) * np.array([0.55, 0.62, 1.0]) + mix * np.array([0.75, 0.55, 1.0])
        self.bg_tw = rng.uniform(0, TAU, n_bg)
        self.bg_twk = rng.integers(1, 4, n_bg)

        Zf = rng.uniform(1.3, 2.6, n_fg)
        sx = rng.uniform(fg_xmin, 1.05, n_fg) * W
        sy = rng.uniform(-0.05, 1.05, n_fg) * H
        self.fg = np.stack([(sx - W / 2) / self.f * Zf, (sy - H / 2) / self.f * Zf, Zf], 1)
        self.fg_flux = rng.uniform(4, 14, n_fg)
        mixf = rng.random(n_fg)[:, None]
        self.fg_col = (1 - mixf) * np.array([0.35, 0.45, 1.0]) + mixf * np.array([0.85, 0.25, 0.6])

        self.exposure = None

    # ---------------------------------------------------------------------------------------
    def to_world(self, r, th, zl):
        """iris-local polar (r, theta, thickness) -> camera space. Top of the disc tilts away."""
        x = r * np.cos(th)
        y = r * np.sin(th)
        ct, st = np.cos(self.tilt), np.sin(self.tilt)
        Y = y * ct + zl * st
        Z = -y * st + zl * ct
        return np.stack([x + self.C[0], Y + self.C[1], Z + self.C[2]], -1)

    def cam_offset(self, t):
        p = TAU * t / self.T
        return np.array([self.sway * np.sin(p), 0.5 * self.sway * np.sin(2 * p + 0.7), 0.0])

    def iris(self, t):
        T, rp = self.T, self.rp
        u = (self.s0 + self.k * t / T) % 1.0
        fid = self.fid
        rs = self.f_rs[fid]
        r = rp + (rs - rp) * (1 - u ** 1.7)
        th = (self.f_th[fid]
              + self.f_wa[fid] * np.sin(self.f_wf[fid] * TAU * r + self.f_wp[fid])
              + 0.32 * (1.0 - r)
              + self.jit * (0.0014 + 0.0018 * r) / r)
        zl = self.zz * (0.005 + 0.012 * r)

        b = 0.55 * np.ones_like(r)
        coll = 0.40 + 0.018 * np.sin(th * 28)
        b += 1.25 * np.exp(-((r - coll) / 0.022) ** 2)
        b += 2.6 * np.exp(-((r - rp - 0.012) / 0.013) ** 2)
        # crypts: small dark pockets between fibre bundles, not big petals
        crypt = (0.5 + 0.5 * np.sin(th * 37 + 9 * r)) * (0.5 + 0.5 * np.sin(th * 61 - 14 * r + 1.3))
        b *= 0.55 + 0.45 * crypt
        b *= np.interp(r, [0.2, 0.32, 0.5, 0.75, 1.0], [1.6, 1.35, 1.0, 0.62, 0.5])
        b *= np.where(r > 1.0, 0.8 * np.exp(-(r - 1.0) * 1.4), 1.0)
        b *= smoothstep(0.0, 0.07, u) * smoothstep(rp, rp + 0.03, r)

        # radar sweep: one full turn per loop, bright leading edge with a long afterglow
        d = (TAU * t / T - th) % TAU
        sw = np.exp(-d / 0.30)
        b *= 1.0 + 1.6 * sw

        col = palette(r)
        col = col * (1 - 0.55 * self.white[:, None]) + 0.55 * self.white[:, None]
        col = col * (1 - 0.35 * sw[:, None]) + 0.35 * sw[:, None] * np.array([0.7, 0.9, 1.0])
        return self.to_world(r, th, zl), col * (self.flux * b)[:, None]

    def a_path(self, q):
        """The threat cuts across the fibres (against the flow) on its way to the core."""
        ra = 1.32 - (1.32 - self.rp) * q ** 1.15
        tha = self.a_th0 - 1.55 * (1.32 - ra) / (1.32 - self.rp) + 0.03 * np.sin(q * 26)
        return ra, tha

    def anomaly(self, t):
        T, rp = self.T, self.rp
        q = ((t - self.a_dt) % T) / T
        ra, tha = self.a_path(q)
        spread = 0.010 + 0.004 * self.a_dt
        P = self.to_world(ra, tha, 0.0) + self.a_off * spread[:, None]
        fade = smoothstep(0.0, 0.05, q) * smoothstep(rp, rp + 0.04, ra)
        w = self.a_flux * np.exp(-self.a_dt / 0.45) * fade * 9.0
        hot = np.exp(-self.a_dt / 0.08)[:, None]
        col = (1 - hot) * np.array([1.0, 0.07, 0.06]) + hot * np.array([1.0, 0.75, 0.6])
        return P, col * w[:, None]

    def anomaly_center(self, t):
        q = (t % self.T) / self.T
        ra, tha = self.a_path(q)
        P = self.to_world(np.array([ra]), np.array([tha]), np.array([0.0]))[0] - self.cam_offset(t)
        x = self.f * P[0] / P[2] + self.W / 2
        y = self.f * P[1] / P[2] + self.H / 2
        vis = float(smoothstep(0.0, 0.05, q) * smoothstep(self.rp + 0.02, self.rp + 0.12, ra))
        return x, y, vis, q

    def burst(self, t):
        T = self.T
        tb = t % T
        a = tb / 1.1
        if a >= 1.0:
            return None
        r = self.rp + 0.02 + 0.55 * (1 - (1 - a) ** 2.2) + self.b_dr * 0.006
        P = self.to_world(r, self.b_th, self.b_dr * 0.004)
        w = self.b_flux * (1 - a) ** 1.6 * 2.2
        col = (1 - a) * np.array([1.0, 0.55, 0.45]) + a * np.array([1.0, 0.1, 0.25])
        return P, col[None, :] * w[:, None]

    def background(self, t):
        tw = 0.75 + 0.25 * np.sin(self.bg_twk * TAU * t / self.T + self.bg_tw)
        return self.bg, self.bg_col * (self.bg_flux * tw)[:, None]

    # ---------------------------------------------------------------------------------------
    def emitters(self, t):
        parts = [self.iris(t), self.background(t), (self.fg, self.fg_col * self.fg_flux[:, None])]
        if self.anomaly_on:
            parts.append(self.anomaly(t))
        if self.burst_on:
            b = self.burst(t)
            if b is not None:
                parts.append(b)
        P = np.concatenate([p[0] for p in parts])
        L = np.concatenate([p[1] for p in parts])
        return P - self.cam_offset(t), L

    def splat(self, t, shutter=0.5, samples=4, fps=24):
        W, H, M = self.W, self.H, self.M
        WW, HH = W + 2 * M, H + 2 * M
        nL = len(LAYER_SIG)
        acc = np.zeros((nL, 3, HH * WW), dtype=np.float32)
        mids = np.sqrt(LAYER_SIG[1:] * LAYER_SIG[:-1])
        for j in range(samples):
            ts = t + (j / samples - 0.5) * shutter / fps
            P, Lr = self.emitters(ts)
            Z = P[:, 2]
            ok = Z > 0.3
            P, Lr, Z = P[ok], Lr[ok] / samples, Z[ok]
            x = self.f * P[:, 0] / Z + W / 2 + M
            y = self.f * P[:, 1] / Z + H / 2 + M
            coc = self.ap * self.f * np.abs(1 / Z - 1 / self.Z0)
            lay = np.searchsorted(mids, coc)
            x0 = np.floor(x).astype(np.int64)
            y0 = np.floor(y).astype(np.int64)
            fx, fy = x - x0, y - y0
            for li in np.unique(lay):
                sl = lay == li
                for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                    w = (fx[sl] if dx else 1 - fx[sl]) * (fy[sl] if dy else 1 - fy[sl])
                    xx, yy = x0[sl] + dx, y0[sl] + dy
                    v = (xx >= 0) & (xx < WW) & (yy >= 0) & (yy < HH)
                    idx = (yy * WW + xx)[v]
                    for c in range(3):
                        acc[li, c] += np.bincount(idx, weights=(w * Lr[sl, c])[v], minlength=HH * WW)
        acc = acc.reshape(nL, 3, HH, WW)
        img = np.zeros((3, HH, WW))
        for li, s in enumerate(LAYER_SIG):
            layer = acc[li].astype(np.float64)
            if not layer.any():
                continue
            if li >= DISC_FROM:
                k = disc_kernel(1.7 * s)
                for c in range(3):
                    img[c] += fftconvolve(layer[c], k, mode="same")
            else:
                for c in range(3):
                    img[c] += gaussian_filter(layer[c], s, mode="constant")
        return img

    def render_hdr(self, t, **kw):
        img = self.splat(t, **kw)
        H, W, M = self.H, self.W, self.M
        # faint violet haze around the iris and a deep-space floor
        yy, xx = np.mgrid[0:H + 2 * M, 0:W + 2 * M]
        cx = self.f * self.C[0] / self.C[2] + W / 2 + M
        cy = self.f * self.C[1] / self.C[2] + H / 2 + M
        d2 = ((xx - cx) / 1.0) ** 2 + ((yy - cy) / 0.55) ** 2
        haze = np.exp(-d2 / (2 * 420.0 ** 2))
        img += haze[None] * np.array([0.020, 0.010, 0.045])[:, None, None]
        img += np.array([0.0025, 0.0025, 0.0060])[:, None, None]
        # bloom
        bl = np.zeros_like(img)
        for s, w in ((3, 0.07), (10, 0.05), (30, 0.035)):
            for c in range(3):
                bl[c] += w * gaussian_filter(img[c], s, mode="constant")
        img += bl
        if self.streak:
            lum = img.mean(0)
            thr = np.percentile(lum, 99.6)
            hi = np.clip(lum - thr, 0, None)
            st = gaussian_filter(hi, (1.2, 110), mode="constant")
            img += self.streak * st[None] * np.array([0.65, 0.45, 1.0])[:, None, None]
        return img[:, M:M + H, M:M + W]

    def calibrate(self, t=1.0, target=1.25, pct=99.85):
        hdr = self.render_hdr(t)
        lum = hdr.mean(0)
        self.exposure = target / max(np.percentile(lum, pct), 1e-9)
        return self.exposure

    def render(self, t, grain=0.010, vignette=0.35, seed=None):
        if self.exposure is None:
            self.calibrate()
        hdr = self.render_hdr(t) * self.exposure
        ldr = to_srgb(aces(hdr)).transpose(1, 2, 0)
        H, W = self.H, self.W
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / np.sqrt(2)
        ldr *= (1 - vignette * d ** 2.2)[..., None]
        rng = np.random.default_rng(seed if seed is not None else int(t * 1000))
        ldr += rng.normal(0, grain, ldr.shape[:2])[..., None]
        return np.clip(ldr, 0, 1)
