"""Regenerates assets/og-image.png (1200x630). Needs Pillow; fonts are instanced from the shipped variable fonts."""
import math, sys, pathlib
from PIL import Image, ImageDraw, ImageFont
root = pathlib.Path(__file__).resolve().parent.parent
serif = sys.argv[1] if len(sys.argv) > 1 else "fraunces_static.ttf"
sans = sys.argv[2] if len(sys.argv) > 2 else "instr_static.ttf"
W, H = 1200, 630
im = Image.new("RGB", (W, H), "#0a0f2e")
d = ImageDraw.Draw(im, "RGBA")
# soft glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
g.ellipse((700, -300, 1500, 400), fill=(27, 37, 102, 200)); g.ellipse((-300, 400, 400, 900), fill=(17, 24, 70, 220))
im.paste(glow, (0, 0), glow); d = ImageDraw.Draw(im, "RGBA")
# stitched lattice
def dash(p, q, on=3, off=6, col=(241, 234, 217, 40)):
    L = math.dist(p, q); n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        d.line([(p[0] + (q[0] - p[0]) * a, p[1] + (q[1] - p[1]) * a), (p[0] + (q[0] - p[0]) * b, p[1] + (q[1] - p[1]) * b)], fill=col, width=1)
S = 56
for gx in range(-1, W // S + 2):
    for gy in range(-1, H // S + 2):
        cx, cy = gx * S + S // 2, gy * S + S // 2
        for r in (26, 13):
            pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
            for i in range(4): dash(pts[i], pts[(i + 1) % 4])
# mark
d.polygon([(1030, 170), (1100, 240), (1030, 310), (960, 240)], fill=(122, 147, 255, 255))
d.ellipse((1018, 228, 1042, 252), fill=(255, 180, 84, 255))
F = lambda p, s: ImageFont.truetype(str(p), s)
d.text((80, 190), "Ink & Equity", font=F(serif, 150), fill="#f1ead9")
d.text((84, 372), "Advocates and legal consultants, Lucknow", font=F(sans, 40), fill="#b8b6c9")
d.text((84, 500), "ieqlaw.com", font=F(sans, 30), fill="#7a93ff")
im.save(root / "assets" / "og-image.png", optimize=True)
print("og-image.png written")
