# Purple Team: banner renderer

The profile banner and avatar are renders, not illustrations. The scene is an iris made of about 400,000 light emitters
flowing inward along its fibres. They are blue (defence) at the rim, violet where the two sides meet and red (offence)
at the core: blue team plus red team equals purple team.

- **Scene** ([`scene.py`](scene.py)): fibres are grouped into evenly spaced bundles with small crypts between them,
  and drift toward the pupil at increasing speed. A radar sweep makes one full turn per loop, leaving an afterglow.
  One red packet (the threat) cuts *across* the fibres, against the flow, and is tracked into the core, where a
  containment ring fires.
- **Optics**: a pinhole camera looks at the disc tilted 63°, so the near and far rims fall out of focus. Depth of field
  is layered by circle of confusion, from Gaussian blur up to disc-shaped bokeh. Motion blur takes four sub-frame
  samples across a 180° shutter. The finish is bloom at three radii, a soft anamorphic streak, ACES tone mapping,
  a vignette and grain.
- **Seamless loop**: every motion (inflow, sweep, camera sway, twinkle, the threat's path) is periodic in 8 s.
- **Type and HUD** ([`typeset.py`](typeset.py)): set at 2× in Space Grotesk and Consolas. The overline runs
  blue → violet → red, a light sweep crosses the name, the tags light up in turn, and a tracking bracket follows the
  threat (`T1059.001`, from detection to containment).

```bash
python build.py               # -> ../banner-purple-team.avif (+ .webp fallback, + still .png)
python build.py --still 4.6   # -> out/still.png (one frame at t = 4.6 s)
python build.py --avatar      # -> ../avatar.png
python cards.py               # -> ../wins.png
```

Edit the `SPEC` in [`build.py`](build.py) to change the text. Requires `numpy`, `scipy` and `pillow` (with AVIF
support). Fonts are read from `.fonts/` (SpaceGrotesk.ttf, consola.ttf, consolab.ttf), which is kept out of git.
