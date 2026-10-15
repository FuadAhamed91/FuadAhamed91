"""The hackathon-wins card, set in the banner's type system.  python cards.py -> ../wins.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

from typeset import font, draw_tracked, GROTESK, MONO, MONO_B, S

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 486

BLUE = (96, 150, 255)
VIOLET = (168, 120, 255)
RED = (255, 78, 92)
GOLD = (246, 200, 110)

CARDS = [
    dict(n="01", place="1ST PLACE", event=["AI Everything", "Hackathon"], team="team build · Awaiz · Bilal · Umar · Fuad",
         project="UnderGrid", pcol=BLUE,
         body=["A live 3D digital twin of a city's underground pipes",
               "and cables. Finds the failing pipe days before it bursts."],
         flow="detect → predict → prioritize → plan"),
    dict(n="02", place="1ST PLACE · OF 48 TEAMS", event=["Oriane × Replit", "Video Economy"], team="build for the video economy · dubai",
         project="PRE//FLIGHT", pcol=RED,
         body=["Tells brands if their campaign idea has already been",
               "done, before they spend money shooting it."],
         flow="brief → IG/TikTok search → saturation → white space"),
]


def background(rng):
    img = np.zeros((H, W, 3))
    img[:] = (7, 7, 14)
    # sparse star dust, softly blurred, cooler on the left and warmer on the right
    n = 2600
    xs, ys = rng.integers(0, W, n), rng.integers(0, H, n)
    dust = np.zeros((H, W))
    np.add.at(dust, (ys, xs), rng.lognormal(0, 0.9, n))
    dust = gaussian_filter(dust, 0.7) * 38
    u = np.linspace(0, 1, W)[None, :, None]
    tint = np.array(BLUE)[None, None] * (1 - u) + np.array(RED)[None, None] * u
    img += dust[..., None] * tint / 255.0
    yy, xx = np.mgrid[0:H, 0:W]
    for cx, col in ((400, VIOLET), (1200, RED)):
        g = np.exp(-(((xx - cx) / 520.0) ** 2 + ((yy - H * 0.2) / 300.0) ** 2))
        img += g[..., None] * np.array(col) * 0.05
    return img


def main():
    rng = np.random.default_rng(3)
    base = Image.fromarray(np.clip(background(rng), 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC)
    over = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    f_n = font(GROTESK, 120, 700)
    f_place = font(GROTESK, 15, 600)
    f_event = font(GROTESK, 40, 700)
    f_team = font(MONO, 13.5)
    f_proj = font(GROTESK, 34, 700)
    f_body = font(GROTESK, 18.5, 400)
    f_flow = font(MONO, 13.5)

    pad, gap = 24, 24
    cw = (W - 2 * pad - gap) // 2
    for i, c in enumerate(CARDS):
        x0, y0 = pad + i * (cw + gap), pad
        x1, y1 = x0 + cw, H - pad
        d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=18 * S, fill=(12, 12, 22, 200),
                            outline=(255, 255, 255, 26), width=S)
        # hairline accent along the top edge, in the project colour
        d.line([((x0 + 40) * S, y0 * S), ((x0 + 210) * S, y0 * S)], fill=c["pcol"] + (230,), width=2 * S)
        # big ghost numeral
        d.text(((x1 - 36) * S, (y0 + 140) * S), c["n"], font=f_n, fill=(255, 255, 255, 14), anchor="rs")
        x = x0 + 40
        draw_tracked(d, x, y0 + 62, c["place"], f_place, 4, fill=GOLD + (255,))
        for j, line in enumerate(c["event"]):
            draw_tracked(d, x - 1, y0 + 118 + j * 46, line, f_event, 0.5, fill=(244, 241, 252, 255))
        draw_tracked(d, x, y0 + 196, c["team"], f_team, 1.2, fill=(128, 126, 158, 255))
        d.line([(x * S, (y0 + 228) * S), ((x1 - 40) * S, (y0 + 228) * S)], fill=(255, 255, 255, 30), width=S)
        draw_tracked(d, x - 1, y0 + 290, c["project"], f_proj, 2, fill=c["pcol"] + (255,))
        for j, line in enumerate(c["body"]):
            draw_tracked(d, x, y0 + 336 + j * 28, line, f_body, 0, fill=(200, 198, 220, 255))
        draw_tracked(d, x, y1 - 40, c["flow"], f_flow, 1.2, fill=VIOLET + (235,))

    out = Image.alpha_composite(base.convert("RGBA"), over).resize((W, H), Image.LANCZOS).convert("RGB")
    path = os.path.join(os.path.dirname(HERE), "wins.png")
    out.save(path, optimize=True)
    print("wins ->", path)


if __name__ == "__main__":
    main()
