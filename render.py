#!/usr/bin/env python3
"""Render the front page for a news-image daily bounty.

Reads stories.json next to this file (lead, grid, also, markers, dateline)
and draws a dense, legible newspaper front page at 1024x1024 with a
dotted world map built from Natural Earth country outlines
(countries-110m TopoJSON, decoded and rasterised here at build time).

The entry program (main.ts) only copies the finished entry.png, so the
image bytes are fixed and both grader runs write identical output.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (18, 18, 18)
RED = (178, 28, 28)
NAVY = (30, 58, 95)
SLATE = (51, 65, 85)
GREY = (90, 90, 90)
RULE = (18, 18, 18)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)     # noqa: E731
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s)    # noqa: E731
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)         # noqa: E731
SANS = lambda s: font("LiberationSans-Regular.ttf", s)       # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------- world map ----------------
# Equirectangular crop: lon -180..180, lat -55..83 (138 degrees tall).
LAT_TOP, LAT_BOT = 83.0, -55.0


def decode_topojson(path):
    """Return a list of polygons; each is a list of (lon, lat) rings."""
    with open(path) as fh:
        topo = json.load(fh)
    arcs = topo["arcs"]
    tr = topo["transform"]
    sx, sy = tr["scale"]
    tx, ty = tr["translate"]
    pts = []
    for arc in arcs:
        x, y = 0, 0
        out = []
        for dx, dy in arc:
            x += dx
            y += dy
            out.append((x * sx + tx, y * sy + ty))
        pts.append(out)
    polys = []
    geoms = topo["objects"]["countries"]["geometries"]
    for g in geoms:
        # Antarctica adds only a fringe of dots at the map's bottom edge.
        if (g.get("properties") or {}).get("name") == "Antarctica":
            continue
        t = g["type"]
        arc_lists = g["arcs"]
        if t == "Polygon":
            rings = [arc_lists]
        elif t == "MultiPolygon":
            rings = arc_lists
        else:
            continue
        for poly in rings:
            decoded = []
            for ring in poly:
                ring_pts = []
                for ai in ring:
                    seg = pts[ai] if ai >= 0 else list(reversed(pts[~ai]))
                    ring_pts.extend(seg)
                decoded.append(ring_pts)
            polys.append(decoded)
    return polys


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * h
    return x, y


def draw_map(draw, polys, x0, y0, w, h, markers):
    # Land mask at panel resolution, then dotted sampling.
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for poly in polys:
        for ring in poly:
            xy = [lonlat_to_xy(lon, lat, 0, 0, w, h) for lon, lat in ring]
            md.polygon(xy, fill=255)
    step = 5
    r = 1.7
    px = mask.load()
    for gy in range(2, h - 1, step):
        for gx in range(2, w - 1, step):
            if px[gx, gy]:
                draw.ellipse([x0 + gx - r, y0 + gy - r,
                              x0 + gx + r, y0 + gy + r], fill=SLATE)
    # Graticule removed: a lone equator line read as a stray mark at
    # this scale; the dotted continents carry the map on their own.
    # Numbered story markers.
    for m in markers:
        mx, my = lonlat_to_xy(m["lon"], m["lat"], x0, y0, w, h)
        draw.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=RED,
                     outline=(255, 255, 255), width=2)
        lx, ly = mx + m.get("dx", 9), my + m.get("dy", -7)
        draw.text((lx, ly), str(m["n"]), font=SANS_B(13), fill=RED)


# ---------------- front page ----------------

def render(data, topo_path, out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    right = W - mx

    # Masthead
    d.rectangle([mx, 22, right, 27], fill=RULE)
    title = data["masthead"]
    tf = SERIF_B(60)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    d.line([(mx, 104), (right, 104)], fill=RULE, width=2)
    d.text((mx, 112), data["dateline"], font=SANS_B(16), fill=INK)
    tag = data["tagline"]
    tw = d.textlength(tag, font=SANS_B(16))
    d.text((right - tw, 112), tag, font=SANS_B(16), fill=RED)
    d.line([(mx, 136), (right, 136)], fill=RULE, width=1)

    # Lead story
    y = 148
    d.text((mx, y), data["lead"]["kicker"], font=SANS_B(14), fill=RED)
    y += 22
    y = draw_wrapped(d, mx, y, data["lead"]["headline"], SERIF_B(37),
                     right - mx, leading=42, max_lines=2)
    y += 4
    y = draw_wrapped(d, mx, y, data["lead"]["deck"], SANS(16),
                     right - mx, leading=21, max_lines=2)
    y += 10
    d.line([(mx, y), (right, y)], fill=RULE, width=1)
    y += 12

    # Middle band: map (left) + three medium stories (right)
    band_y = y
    map_w, map_h = 524, 190
    d.text((mx, band_y), "WHERE THE DAY HAPPENED",
           font=SANS_B(14), fill=INK)
    d.text((mx + 218, band_y), "— numbered places in today's stories",
           font=SANS(13), fill=GREY)
    polys = decode_topojson(topo_path)
    draw_map(d, polys, mx, band_y + 22, map_w, map_h, data["markers"])
    key_y = band_y + 22 + map_h + 6
    key = "  ·  ".join(f"{m['n']} {m['label']}" for m in data["markers"])
    draw_wrapped(d, mx, key_y, key, SANS(11), map_w, leading=14, max_lines=2)

    # Right column: three medium stories
    rx, rw = 584, right - 584
    ry = band_y
    for s in data["column"]:
        d.text((rx, ry), s["kicker"], font=SANS_B(12), fill=RED)
        ry += 17
        ry = draw_wrapped(d, rx, ry, s["headline"], SERIF_B(19), rw,
                          leading=22, max_lines=2)
        ry = draw_wrapped(d, rx, ry, s["deck"], SANS(13), rw,
                          leading=16, max_lines=2)
        ry += 6
        d.line([(rx, ry), (right, ry)], fill=(200, 195, 185), width=1)
        ry += 10
    band_bottom = max(key_y + 28, ry)
    y = band_bottom + 2
    d.line([(mx, y), (right, y)], fill=RULE, width=1)
    y += 10

    # Grid: 3 columns x 2 rows
    cols = 3
    cw = (right - mx - 2 * 24) // cols
    gy = y
    for i, s in enumerate(data["grid"]):
        col = i % cols
        row = i // cols
        x = mx + col * (cw + 24)
        yy = gy + row * 96
        d.text((x, yy), s["kicker"], font=SANS_B(12), fill=RED)
        yy += 17
        yy = draw_wrapped(d, x, yy, s["headline"], SERIF_B(18), cw,
                          leading=21, max_lines=2)
        draw_wrapped(d, x, yy, s["deck"], SANS(12), cw, leading=15,
                     max_lines=2)
    y = gy + 2 * 96 + 4
    d.line([(mx, y), (right, y)], fill=RULE, width=1)
    y += 10

    # Also today: 3 columns of compact one-liners
    d.text((mx, y), "ALSO TODAY", font=SANS_B(14), fill=INK)
    y += 22
    ay = y
    per_col = math.ceil(len(data["also"]) / 3)
    for col in range(3):
        x = mx + col * (cw + 24)
        yy = ay
        for s in data["also"][col * per_col:(col + 1) * per_col]:
            yy = draw_wrapped(d, x, yy, s, SERIF_B(13), cw, leading=15,
                              max_lines=2)
            yy += 5
    y = ay + per_col * 35 + 6
    d.line([(mx, y), (right, y)], fill=RULE, width=1)
    y += 8
    d.text((mx, y), data["footer"], font=SANS(11), fill=GREY)

    img.save(out_path, "PNG", optimize=True)
    size = os.path.getsize(out_path)
    print(f"wrote {out_path}: {img.size}, {size} bytes")
    if size > 1_048_576:
        img.save(out_path, "JPEG", quality=88, optimize=True)
        print(f"over 1 MiB as PNG; saved JPEG: {os.path.getsize(out_path)} bytes")


if __name__ == "__main__":
    with open(os.path.join(HERE, "stories.json")) as fh:
        data = json.load(fh)
    topo = sys.argv[1] if len(sys.argv) > 1 else "/tmp/countries-110m.json"
    render(data, topo, os.path.join(HERE, "entry.png"))
