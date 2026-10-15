"""Typography and HUD for the banner. Text is set at 2x and composited in sRGB over the render."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, ".fonts")
S = 2

GROTESK = "SpaceGrotesk.ttf"
MONO = "consola.ttf"
MONO_B = "consolab.ttf"

BLUE = np.array([96, 150, 255.0])
VIOLET = np.array([168, 120, 255.0])
RED = np.array([255, 78, 92.0])


def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FD, name), int(round(size * S)))
    if weight is not None:
        f.set_variation_by_axes([weight])
    return f


def tracked_width(f, s, track):
    return (sum(f.getlength(c) for c in s) + track * S * (len(s) - 1)) / S


def draw_tracked(d, x, y, s, f, track, fill=255):
    X = x * S
    for c in s:
        d.text((X, y * S), c, font=f, fill=fill, anchor="ls")
        X += f.getlength(c) + track * S
    return X / S


def mask(W, H, draw_fn):
    m = Image.new("L", (W * S, H * S), 0)
    draw_fn(ImageDraw.Draw(m))
    return np.asarray(m.resize((W, H), Image.LANCZOS), dtype=np.float32) / 255.0


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


class Typeset:
    def __init__(self, W, H, T, spec):
        self.W, self.H, self.T = W, H, T
        self.spec = spec
        x0 = spec["x"]
        f_over = font(GROTESK, spec["over_size"], 560)
        f_name = font(GROTESK, spec["name_size"], 700)
        f_tag = font(MONO, spec["tag_size"])
        f_cap = font(MONO, spec["cap_size"])
        self.f_hud = font(MONO_B, 11)
        self.f_hud2 = font(MONO, 10.5)

        over = spec["overline"]
        self.over_end = tracked_width(f_over, over, 4.2) + x0
        self.m_over = mask(W, H, lambda d: draw_tracked(d, x0, spec["over_y"], over, f_over, 4.2))
        oy = spec["over_y"]
        self.cursor_box = (self.over_end + 9, oy - spec["over_size"] * 0.78, self.over_end + 17, oy + 3)

        def draw_name(d):
            for i, line in enumerate(spec["name"]):
                draw_tracked(d, x0 - 3, spec["name_y"][i], line, f_name, spec["name_track"])
        self.m_name = mask(W, H, draw_name)
        glow = Image.fromarray((self.m_name * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
        self.m_glow = np.asarray(glow, dtype=np.float32) / 255.0

        # tags: one mask per tag, plus separators
        self.m_tags = []
        x = x0
        sep = "  ·  "
        seps = []
        for i, tag in enumerate(spec["tags"]):
            self.m_tags.append(mask(W, H, lambda d, x=x, tag=tag: draw_tracked(d, x, spec["tag_y"], tag, f_tag, 3.0)))
            x += tracked_width(f_tag, tag, 3.0) + 3.0
            if i < len(spec["tags"]) - 1:
                seps.append(x)
                x += tracked_width(f_tag, sep, 3.0) + 3.0
        self.m_sep = mask(W, H, lambda d: [draw_tracked(d, sx, spec["tag_y"], sep, f_tag, 3.0) for sx in seps])
        self.m_cap = mask(W, H, lambda d: draw_tracked(d, x0, spec["cap_y"], spec["caption"], f_cap, 1.4))

        xs = np.arange(W, dtype=np.float32)[None, :]
        ys = np.arange(H, dtype=np.float32)[:, None]
        self.xs, self.ys = xs, ys
        # overline colour runs blue -> violet -> red across its width: blue team + red team
        u = np.clip((xs - x0) / max(1, self.over_end - x0), 0, 1)
        self.c_over = np.where(u[..., None] < 0.5,
                               BLUE + (VIOLET - BLUE) * (u[..., None] * 2),
                               VIOLET + (RED - VIOLET) * (u[..., None] * 2 - 1))
        ny0, ny1 = spec["name_y"][0] - spec["name_size"] * 0.72, spec["name_y"][-1]
        v = np.clip((ys - ny0) / (ny1 - ny0), 0, 1)[..., None]
        self.c_name = np.array([250, 247, 255.0]) * (1 - v) + np.array([200, 190, 236.0]) * v
        self.tag_cols = [np.array(c, dtype=np.float32) for c in spec["tag_colors"]]

    @staticmethod
    def over(img, m, col, a=1.0):
        a = (m * a)[..., None]
        return img * (1 - a) + col * a

    def compose(self, img, t, hud=None):
        """img: HxWx3 float sRGB in 0..255. hud: (x, y, vis, q) of the tracked anomaly or None."""
        T = self.T
        img = img.copy()
        # soft scrim behind the type so it never fights the particles
        scrim = 1 - 0.55 * smooth(self.spec["x"] + 620, self.spec["x"] + 120, self.xs)
        img *= scrim[..., None]

        img = self.over(img, self.m_over, self.c_over, 0.95)
        if (t * 2) % 2 < 1:  # 1 Hz block cursor
            x0, y0, x1, y1 = self.cursor_box
            cm = ((self.xs >= x0) & (self.xs < x1) & (self.ys >= y0) & (self.ys < y1)).astype(np.float32)
            img = self.over(img, cm, RED, 0.95)

        # name: soft glow, then fill, then a light sweep once per loop
        img = img + self.m_glow[..., None] * np.array([120, 90, 200.0]) * 0.22
        p = smooth(0.4, 2.6, t % T)
        bandx = -200 + p * (self.spec["x"] + 700)
        band = np.exp(-((self.xs + 0.45 * (self.ys - 250) - bandx) / 60.0) ** 2) * (0 < p < 1)
        img = self.over(img, self.m_name, self.c_name + band[..., None] * 60, 1.0)

        # tags light up in turn, 2 s each
        n = len(self.m_tags)
        slot = T / n
        for i, m in enumerate(self.m_tags):
            ph = ((t - i * slot) % T)
            lit = smooth(0, 0.35, ph) * (1 - smooth(slot - 0.1, slot + 0.25, ph))
            col = np.array([132, 132, 160.0]) * (1 - lit) + self.tag_cols[i] * lit
            img = self.over(img, m, col, 0.95)
        img = self.over(img, self.m_sep, np.array([90, 90, 118.0]), 0.9)
        img = self.over(img, self.m_cap, np.array([112, 110, 142.0]), 0.9)

        if hud is not None:
            img = self.draw_hud(img, *hud)
        return np.clip(img, 0, 255)

    def draw_hud(self, img, x, y, vis, q):
        if vis < 0.02 or not (0 < x < self.W and 0 < y < self.H):
            return img
        layer = Image.new("L", (self.W * S, self.H * S), 0)
        d = ImageDraw.Draw(layer)
        X, Y = x * S, y * S
        b, c = 17 * S, 7 * S
        for sx in (-1, 1):
            for sy in (-1, 1):
                cx, cy = X + sx * b, Y + sy * b
                d.line([(cx, cy), (cx - sx * c, cy)], fill=255, width=S)
                d.line([(cx, cy), (cx, cy - sy * c)], fill=255, width=S)
        right = x + 220 < self.W - 8
        dirx = 1 if right else -1
        diry = -1 if y > 90 else 1
        ax, ay = X + dirx * b, Y + diry * b
        bx, by = ax + dirx * 26 * S, ay + diry * 26 * S
        ex = bx + dirx * 150 * S
        d.line([(ax, ay), (bx, by), (ex, by)], fill=255, width=S)
        state = "DETECTED" if q < 0.22 else ("TRACKING" if q < 0.82 else "CONTAINING")
        risk = 0.58 + 0.39 * min(1.0, q * 1.3)
        tx = bx if right else ex
        d.text((tx, by - 5 * S), "THREAT · T1059.001", font=self.f_hud, fill=255, anchor="ls")
        layer2 = Image.new("L", (self.W * S, self.H * S), 0)
        ImageDraw.Draw(layer2).text((tx, by + 14 * S), f"risk {risk:.2f} · {state}", font=self.f_hud2,
                                    fill=255, anchor="ls")
        m1 = np.asarray(layer.resize((self.W, self.H), Image.LANCZOS), dtype=np.float32) / 255.0
        m2 = np.asarray(layer2.resize((self.W, self.H), Image.LANCZOS), dtype=np.float32) / 255.0
        img = self.over(img, m1, np.array([255, 92, 104.0]), 0.9 * vis)
        img = self.over(img, m2, np.array([205, 196, 225.0]), 0.85 * vis)
        return img
