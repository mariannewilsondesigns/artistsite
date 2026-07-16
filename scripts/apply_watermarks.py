"""
Applies a subtle © watermark to all artwork and site images.
Run this whenever new images are added:
    python3 scripts/apply_watermarks.py

The script backs up originals to images/works-original/ and images/site-original/
on first run, then watermarks in place. Re-running re-watermarks from originals.
"""
import os, shutil, glob
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORKS_DIR   = os.path.join(ROOT, "images", "works")
SITE_DIR    = os.path.join(ROOT, "images", "site")
BACKUP_WORKS = os.path.join(ROOT, "images", "works-original")
BACKUP_SITE  = os.path.join(ROOT, "images", "site-original")

WATERMARK_TEXT = "© Marianne Wilson"

# ── helpers ──────────────────────────────────────────────────────────

def backup_then_watermark(img_path, backup_root):
    """Backup the original file once, then apply watermark in place."""
    rel = os.path.relpath(img_path, os.path.dirname(backup_root))
    backup_path = os.path.join(backup_root, rel)
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)

    if not os.path.exists(backup_path):
        shutil.copy2(img_path, backup_path)
        print(f"  ● backed up → {backup_path}")
    else:
        # restore from backup so we always watermark from the clean original
        shutil.copy2(backup_path, img_path)

    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # font size proportional to the shorter dimension (≈3% of min edge)
    font_size = max(12, int(min(w, h) * 0.035))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except Exception:
        font = ImageFont.load_default()

    # measure text
    bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # position: bottom-right with padding
    pad = int(font_size * 0.9)
    x = w - tw - pad
    y = h - th - pad

    # draw a very subtle shadow behind text for readability
    shadow_offset = 1
    draw.text((x + shadow_offset, y + shadow_offset), WATERMARK_TEXT,
              fill=(0, 0, 0, 60), font=font)
    draw.text((x, y), WATERMARK_TEXT,
              fill=(255, 255, 255, 60), font=font)

    img.save(img_path, "JPEG", quality=92)
    print(f"  ✓ watermarked → {img_path}")


def main():
    # ── artwork images ──
    patterns = [
        os.path.join(WORKS_DIR, "**", "*.jpg"),
        os.path.join(WORKS_DIR, "**", "*.jpeg"),
        os.path.join(WORKS_DIR, "**", "*.png"),
    ]
    images = []
    for pat in patterns:
        images.extend(glob.glob(pat, recursive=True))

    print(f"\nFound {len(images)} artwork images\n")

    for img_path in sorted(images):
        rel = os.path.relpath(img_path, WORKS_DIR)
        print(f"  Artwork: {rel}")
        backup_then_watermark(img_path, BACKUP_WORKS)

    # ── site images (skip svg) ──
    site_images = []
    for f in os.listdir(SITE_DIR):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            site_images.append(os.path.join(SITE_DIR, f))

    print(f"\nFound {len(site_images)} site images\n")

    for img_path in sorted(site_images):
        rel = os.path.relpath(img_path, SITE_DIR)
        print(f"  Site: {rel}")
        backup_then_watermark(img_path, BACKUP_SITE)

    print("\nDone. Originals are backed up in:")
    print(f"  {BACKUP_WORKS}")
    print(f"  {BACKUP_SITE}")


if __name__ == "__main__":
    main()
