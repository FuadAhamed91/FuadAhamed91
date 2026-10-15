"""Build the profile banner and avatar.

  python build.py --still 3.4     -> out/still.png (one frame with type)
  python build.py                 -> ../banner-purple-team.avif + .webp (seamless 8 s loop)
  python build.py --avatar        -> ../avatar.png (500 x 500, no type)
"""
import argparse
import os
import time
from multiprocessing import Pool

import numpy as np
from PIL import Image

from scene import Scene
from typeset import Typeset

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ASSETS = os.path.dirname(HERE)

W, H, T, FPS = 1600, 500, 8.0, 24

SPEC = dict(
    x=92,
    overline="SOC ANALYST  ×  PENETRATION TESTER",
    over_size=17, over_y=116,
    name=["FUAD", "AHAMED"], name_size=86, name_y=[208, 298], name_track=9,
    tags=["SOC", "PENTEST", "AGENTIC AI", "FULL-STACK"],
    tag_colors=[(110, 168, 255), (255, 92, 104), (182, 140, 255), (238, 236, 248)],
    tag_size=15.5, tag_y=356,
    caption="blue team + red team = purple team  ·  every event inspected, every path tested",
    cap_size=11.5, cap_y=446,
)

_scene = None
_type = None


def _init(exposure):
    global _scene, _type
    _scene = Scene(W=W, H=H, T=T)
    _scene.exposure = exposure
    _type = Typeset(W, H, T, SPEC)


def frame(t):
    img = _scene.render(t, grain=0.006, seed=11) * 255.0  # static grain: it compresses, flicker doesn't
    hud = _scene.anomaly_center(t)
    return _type.compose(img, t, hud).astype(np.uint8)


def calibrate():
    s = Scene(W=W, H=H, T=T)
    return s.calibrate(t=3.4, target=1.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", type=float)
    ap.add_argument("--avatar", action="store_true")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--fps", type=int, default=FPS)
    ap.add_argument("--encode-only", action="store_true", help="re-encode out/frames without rendering")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    if a.avatar:
        s = Scene(W=1000, H=1000, T=T, tilt_deg=16, center_px=(500, 500), R_px=405, aperture=0.02,
                  n_fib=1900, per_fib=230, n_fg=6, sway=0.0, streak=0.04, burst=False, fg_xmin=0.0)
        s.a_th0 = np.radians(-70)
        s.calibrate(t=2.9, target=1.05)
        img = s.render(2.9, vignette=0.55, grain=0.008)
        Image.fromarray((img * 255).astype(np.uint8)).resize((500, 500), Image.LANCZOS).save(
            os.path.join(ASSETS, "avatar.png"))
        print("avatar ->", os.path.join(ASSETS, "avatar.png"))
        return

    if a.encode_only:
        fdir = os.path.join(OUT, "frames")
        frames = [Image.open(os.path.join(fdir, n)).convert("RGB") for n in sorted(os.listdir(fdir))]
        encode(frames, a.fps)
        return

    exposure = calibrate()
    print("exposure", exposure)
    if a.still is not None:
        _init(exposure)
        Image.fromarray(frame(a.still)).save(os.path.join(OUT, "still.png"))
        print("still ->", os.path.join(OUT, "still.png"))
        return

    n = int(round(T * a.fps))
    ts = [i / a.fps for i in range(n)]
    t0 = time.time()
    with Pool(a.workers, initializer=_init, initargs=(exposure,)) as pool:
        frames = []
        for i, f in enumerate(pool.imap(frame, ts)):
            frames.append(Image.fromarray(f))
            if i % 12 == 0:
                print(f"frame {i}/{n}  {time.time() - t0:.0f}s", flush=True)
    fdir = os.path.join(OUT, "frames")
    os.makedirs(fdir, exist_ok=True)
    for i, f in enumerate(frames):
        f.save(os.path.join(fdir, f"{i:04d}.png"))
    frames[0].save(os.path.join(ASSETS, "banner-purple-team-still.png"))
    encode(frames, a.fps)


def encode(frames, fps, avif_q=48, webp_q=60):
    dur = int(round(1000 / fps))
    t0 = time.time()
    frames[0].save(os.path.join(ASSETS, "banner-purple-team.avif"), save_all=True, append_images=frames[1:],
                   duration=dur, loop=0, quality=avif_q, speed=6)
    print("avif", os.path.getsize(os.path.join(ASSETS, "banner-purple-team.avif")) // 1024, "KB",
          f"{time.time() - t0:.0f}s")
    half = frames[::2]
    half[0].save(os.path.join(ASSETS, "banner-purple-team.webp"), save_all=True, append_images=half[1:],
                 duration=dur * 2, loop=0, quality=webp_q, method=4)
    print("webp", os.path.getsize(os.path.join(ASSETS, "banner-purple-team.webp")) // 1024, "KB")


if __name__ == "__main__":
    main()
