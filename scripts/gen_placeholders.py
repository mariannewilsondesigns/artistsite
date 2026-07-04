"""
Generates placeholder imagery so the site previews fully before real
photography is dropped in. Every generated file is watermarked "ADD IMAGE"
so nobody accidentally ships a placeholder to print.
Run: python3 scripts/gen_placeholders.py
"""
import json, os, re, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "works.json")
IMG_WORKS = os.path.join(ROOT, "images", "works")
IMG_SITE = os.path.join(ROOT, "images", "site")

PAPER = (250, 248, 241)
INK = (29, 27, 22)
CHART = (220, 255, 79)
CHART_DEEP = (122, 140, 0)
PLUM = (44, 27, 51)
PLUM_LIGHT = (74, 48, 84)
STONE = (231, 226, 214)

PALETTES = [
    (PLUM, CHART, STONE),
    (STONE, PLUM, CHART),
    (CHART, PLUM, PAPER),
    (PLUM_LIGHT, STONE, CHART),
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def get_font(size, italic=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf" if italic else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def abstract_bg(w, h, seed, bg, fg, fg2):
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(seed)
    # soft diagonal bands
    for i in range(6):
        x0 = rnd.uniform(-0.3, 1.1) * w
        y0 = rnd.uniform(-0.3, 1.1) * h
        r = rnd.uniform(0.25, 0.55) * max(w, h)
        color = fg if i % 2 == 0 else fg2
        alpha = rnd.randint(35, 90)
        draw.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=color + (alpha,))
    img = img.filter(ImageFilter.GaussianBlur(radius=w * 0.03))
    # fine grain line texture on top
    draw2 = ImageDraw.Draw(img, "RGBA")
    for i in range(0, h, 6):
        draw2.line([(0, i), (w, i)], fill=(0, 0, 0, 4))
    return img

def watermark(img, title, plate, subtitle="ADD IMAGE"):
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")
    # center card
    pad = int(w * 0.08)
    box = [pad, h // 2 - int(h * 0.09), w - pad, h // 2 + int(h * 0.09)]
    draw.rectangle(box, fill=(250, 248, 241, 235), outline=INK + (255,), width=2)
    f1 = get_font(int(w * 0.045))
    f2 = get_font(int(w * 0.028), italic=True)
    tw = draw.textlength(subtitle, font=f1)
    draw.text((w / 2 - tw / 2, h / 2 - int(h * 0.055)), subtitle, font=f1, fill=INK)
    label = f"Plate {plate} — {title}"
    tw2 = draw.textlength(label, font=f2)
    if tw2 > (box[2] - box[0]) - 40:
        label = f"Plate {plate}"
        tw2 = draw.textlength(label, font=f2)
    draw.text((w / 2 - tw2 / 2, h / 2 + int(h * 0.01)), label, font=f2, fill=INK)
    return img

def make_work_image(slug, title, plate, idx, seed):
    w, h = 1600, 2000
    palette = PALETTES[seed % len(PALETTES)]
    bg, fg, fg2 = palette
    img = abstract_bg(w, h, seed * 10 + idx, bg, fg, fg2)
    img = watermark(img, title, plate)
    out_dir = os.path.join(IMG_WORKS, slug)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{idx:02d}.jpg")
    img.save(path, quality=87)
    return f"images/works/{slug}/{idx:02d}.jpg"

def make_site_image(name, w, h, seed, label):
    palette = PALETTES[seed % len(PALETTES)]
    bg, fg, fg2 = palette
    img = abstract_bg(w, h, seed, bg, fg, fg2)
    img = watermark(img, "", "", subtitle=label)
    os.makedirs(IMG_SITE, exist_ok=True)
    path = os.path.join(IMG_SITE, name)
    img.save(path, quality=88)

def main():
    with open(DATA) as f:
        data = json.load(f)

    for i, work in enumerate(data["works"], start=1):
        slug = slugify(work["title"])
        plate = f"{work['id']:02d}"
        work["slug"] = slug
        work["plate"] = plate
        images = []
        for idx in range(1, 4):
            rel = make_work_image(slug, work["title"], plate, idx, work["id"])
            images.append(rel)
        work["images"] = images

    with open(DATA, "w") as f:
        json.dump(data, f, indent=2)

    make_site_image("splash.jpg", 2400, 1500, 1, "ADD SPLASH IMAGE")
    make_site_image("hero.jpg", 2400, 1000, 2, "ADD WORKS HERO IMAGE")
    make_site_image("artist.jpg", 1400, 1800, 3, "ADD ARTIST PORTRAIT")
    make_site_image("about-texture.jpg", 1400, 1800, 4, "ADD STUDIO IMAGE")
    print("Placeholder imagery generated.")

if __name__ == "__main__":
    main()
