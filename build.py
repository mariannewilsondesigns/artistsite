"""
Rebuilds the entire static site from data/works.json.
Run this any time you edit data/works.json (new titles, images, descriptions).
    python3 build.py
"""
import json, os
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")
DATA_FILE = os.path.join(ROOT, "data", "works.json")

def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    works = data["works"]
    artist = data["artist"]
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=False)

    # --- index.html (splash) ---
    env.get_template("index.html").stream(root="", artist=artist).dump(
        os.path.join(ROOT, "index.html"))

    # --- works.html (grid) ---
    env.get_template("works.html").stream(root="", artist=artist, works=works).dump(
        os.path.join(ROOT, "works.html"))

    # --- about.html ---
    env.get_template("about.html").stream(root="", artist=artist).dump(
        os.path.join(ROOT, "about.html"))

    # --- works/{slug}.html (one per artwork) ---
    os.makedirs(os.path.join(ROOT, "works"), exist_ok=True)
    n = len(works)
    for i, w in enumerate(works):
        prev_w = works[i - 1]
        next_w = works[(i + 1) % n]
        env.get_template("work.html").stream(
            root="../", artist=artist, w=w, prev=prev_w, next=next_w, total=n
        ).dump(os.path.join(ROOT, "works", w["slug"] + ".html"))

    print(f"Built {n} artwork pages + index, works, about.")

if __name__ == "__main__":
    main()
