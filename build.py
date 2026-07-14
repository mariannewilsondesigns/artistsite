"""
Rebuilds the entire static site from data/works.json.
Run this any time you edit data/works.json (new titles, images, descriptions).
    python3 build.py
"""
import json, os, itertools
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")
DATA_FILE = os.path.join(ROOT, "data", "works.json")

def build_medium_groups(works):
    """Group works by medium_group, preserving original JSON order."""
    groups = {}
    for k, g in itertools.groupby(works, key=lambda w: w.get("medium_group", "")):
        groups[k] = list(g)
    ordered = []
    seen = set()
    for w in works:
        g = w.get("medium_group", "")
        if g not in seen:
            seen.add(g)
            ordered.append((g, groups[g]))
    return ordered

def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    works = data["works"]
    artist = data["artist"]
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=False)

    medium_groups = build_medium_groups(works)

    # --- index.html (splash) ---
    env.get_template("index.html").stream(root="", artist=artist).dump(
        os.path.join(ROOT, "index.html"))

    # --- works.html (grid) ---
    env.get_template("works.html").stream(
        root="", artist=artist, works=works, medium_groups=medium_groups
    ).dump(os.path.join(ROOT, "works.html"))

    # --- about.html ---
    env.get_template("about.html").stream(root="", artist=artist).dump(
        os.path.join(ROOT, "about.html"))

    # --- alphabetical ordering for default (fallback) prev/next ---
    alpha_works = sorted(works, key=lambda w: w["title"].lower())
    an = len(alpha_works)
    alpha_lookup = {w["slug"]: i for i, w in enumerate(alpha_works)}

    # --- works/{slug}.html (one per artwork, prev/next within medium group) ---
    os.makedirs(os.path.join(ROOT, "works"), exist_ok=True)
    for grp_name, grp_works in medium_groups:
        gn = len(grp_works)
        for i, w in enumerate(grp_works):
            prev_w = grp_works[i - 1]
            next_w = grp_works[(i + 1) % gn]
            # also compute alphabetical fallback prev/next across all works
            ai = alpha_lookup[w["slug"]]
            prev_alpha = alpha_works[(ai - 1 + an) % an]
            next_alpha = alpha_works[(ai + 1) % an]
            alpha_entries = [{"slug": aw["slug"], "title": aw["title"]} for aw in alpha_works]
            env.get_template("work.html").stream(
                root="../", artist=artist, w=w, prev=prev_w, next=next_w,
                prev_alpha=prev_alpha, next_alpha=next_alpha,
                alpha_entries=alpha_entries, total=gn
            ).dump(os.path.join(ROOT, "works", w["slug"] + ".html"))

    n = len(works)
    print(f"Built {n} artwork pages across {len(medium_groups)} media + index, works, about.")

if __name__ == "__main__":
    main()
