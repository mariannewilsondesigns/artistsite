#!/usr/bin/env python3
"""Copy all 01 (hero) images to a desktop folder with formatted filenames."""

import json
import os
import shutil
import re

# Paths
BASE_DIR = "/Users/marywilson/Desktop/artistsite"
DEST_DIR = "/Users/marywilson/Desktop/hero-images"

# Load works data
with open(os.path.join(BASE_DIR, "data/works.json"), "r") as f:
    data = json.load(f)

# Create destination folder
os.makedirs(DEST_DIR, exist_ok=True)

works = data["works"]

for work in works:
    title = work["title"]
    
    # Format dimensions: "79 × 106 cm" -> "79cm x 106cm"
    dims = work["dimensions"]
    dims = re.sub(r'(\d+)\s*×\s*(\d+)\s*cm', r'\1cm x \2cm', dims)
    
    medium = work["medium"]
    price = work["price"]
    
    # Build filename: "Title 79cm x 106cm Medium $2600.jpg"
    filename = f"{title} {dims} {medium} ${price}.jpg"
    
    # Get the 01.jpg source path
    source_path = os.path.join(BASE_DIR, work["images"][0])
    
    if not os.path.exists(source_path):
        print(f"⚠️  MISSING: {source_path}")
        continue
    
    dest_path = os.path.join(DEST_DIR, filename)
    
    # Check if destination already exists
    if os.path.exists(dest_path):
        print(f"⏭️  EXISTS: {filename}")
        continue
    
    shutil.copy2(source_path, dest_path)
    print(f"✅ COPIED: {filename}")

print(f"\n🎉 Done! {len(os.listdir(DEST_DIR))} images in {DEST_DIR}")
