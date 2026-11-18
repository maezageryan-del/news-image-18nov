#!/usr/bin/env python3
"""Draw "The World in One Day" — a one-page newspaper for one day.

The page is a single 1024x1024 image.  Every word on it comes from
stories.json, which sits beside this script; this file only knows
about layout, typography and geography.

Usage:
    python3 render.py <countries-110m.json>

The argument is a Natural Earth countries file in TopoJSON format
(the 110 m resolution set).  Its shapes become the dotted world map
in the middle band of the page.  The finished page is written to
entry.png in the current directory.
"""

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas

SIZE = 1024
MARGIN = 46
PAGE_W = SIZE - 2 * MARGIN

INK = (24, 22, 20)
PAPER = (250, 247, 240)
FAINT = (110, 102, 92)
ACCENT = (158, 32, 28)
RULE = (24, 22, 20)

HERE = Path(__file__).resolve().parent
DATA_FILE = HERE / "stories.json"
OUT_FILE = Path.cwd() / "entry.png"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def font(size, bold=False):
    """Best available TrueType font at `size`, else Pillow's bitmap."""
    for path in FONT_BOLD_CANDIDATES if bold else FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Split `text` into lines that fit `width` pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)
    return y + fnt.size + 6


def paragraph(draw, x, y, text, fnt, width, leading=1.25, fill=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


# ---------------------------------------------------------------- topojson

def decode_arcs(topo):
    """Expand TopoJSON arcs (delta encoded, optionally transformed)."""
    transform = topo.get("transform")
    scale = transform["scale"] if transform else (1.0, 1.0)
    translate = transform["translate"] if transform else (0.0, 0.0)
    decoded = []
    for arc in topo["arcs"]:
        x = y = 0
        points = []
        for dx, dy in arc:
            x += dx
            y += dy
            points.append((x * scale[0] + translate[0],
                           y * scale[1] + translate[1]))
        decoded.append(points)
    return decoded


def stitch(arcs, indexes):
    """Join the arcs named by `indexes` into one ring of points."""
    ring = []
    for idx in indexes:
        arc = arcs[idx] if idx >= 0 else list(reversed(arcs[~idx]))
        ring.extend(arc if not ring else arc[1:])
    return ring


def country_rings(topo):
    """All polygon rings (lon/lat) of every geometry in the file."""
    arcs = decode_arcs(topo)
    rings = []
    for obj in topo["objects"].values():
        geoms = obj["geometries"] if obj["type"] == "GeometryCollection" \
            else [obj]
        for geom in geoms:
            polys = geom["arcs"]
            if geom["type"] == "Polygon":
                polys = [polys]
            for poly in polys:
                for ring_indexes in poly:
                    rings.append(stitch(arcs, ring_indexes))
    return rings


def inside(lon, lat, ring):
    """Ray-casting point-in-polygon test for one ring."""
    hit = False
    px, py = ring[-1]
    for x, y in ring:
        if (y > lat) != (py > lat):
            cross = (px - x) * (lat - y) / (py - y) + x
            if lon < cross:
                hit = not hit
        px, py = x, y
    return hit


# ---------------------------------------------------------------- the map

def draw_map(draw, rings, markers, box):
    """A dotted equirectangular world with numbered story markers."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def project(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * w,
                y0 + (90.0 - lat) / 180.0 * h)

    boxes = []
    for ring in rings:
        lons = [p[0] for p in ring]
        lats = [p[1] for p in ring]
        boxes.append((min(lons), min(lats), max(lons), max(lats)))

    step = 5
    dot = 1.6
    gy = y0 + step // 2
    while gy < y1:
        lat = 90.0 - (gy - y0) / h * 180.0
        gx = x0 + step // 2
        while gx < x1:
            lon = (gx - x0) / w * 360.0 - 180.0
            for ring, (lo0, la0, lo1, la1) in zip(rings, boxes):
                if lo0 <= lon <= lo1 and la0 <= lat <= la1 and \
                        inside(lon, lat, ring):
                    draw.ellipse([gx - dot, gy - dot, gx + dot, gy + dot],
                                 fill=(168, 158, 142))
                    break
            gx += step
        gy += step

    draw.rectangle(box, outline=RULE, width=1)

    label_font = font(15, bold=True)
    num_font = font(16, bold=True)
    for m in markers:
        cx, cy = project(m["lon"], m["lat"])
        r = 13
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT)
        label = str(m["n"])
        draw.text((cx - draw.textlength(label, font=num_font) / 2,
                   cy - num_font.size / 2 - 1),
                  label, font=num_font, fill=(255, 255, 255))
        # Place the name beside its disc, but keep it inside the map:
        # a label that would spill past either edge is pulled back.
        lx = cx + m["dx"]
        text_w = draw.textlength(m["label"], font=label_font)
        lx = max(x0 + 2, min(lx, x1 - text_w - 2))
        ly = max(y0 + 2, min(cy + m["dy"], y1 - label_font.size - 2))
        draw.text((lx, ly), m["label"], font=label_font, fill=INK)


# ---------------------------------------------------------------- sections

def story_block(draw, x, y, width, item, head_size, deck_size):
    """One kicker/headline/deck story; returns the y below it."""
    draw.text((x, y), item["kicker"], font=font(15, bold=True), fill=ACCENT)
    y += 22
    y = paragraph(draw, x, y, item["headline"], font(head_size, bold=True),
                  width, leading=1.12)
    y += 2
    y = paragraph(draw, x, y, item["deck"], font(deck_size), width,
                  leading=1.25, fill=(52, 48, 44))
    return y


def build_page(data, rings):
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    cx = SIZE // 2

    # Masthead ------------------------------------------------------------
    y = 30
    y = centred(draw, cx, y, data["masthead"], font(64, bold=True))
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=RULE, width=3)
    y += 10
    left = data["dateline"]
    right = data["tagline"]
    small = font(17, bold=True)
    draw.text((MARGIN, y), left, font=small, fill=INK)
    draw.text((SIZE - MARGIN - draw.textlength(right, font=small), y),
              right, font=small, fill=INK)
    y += 30
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=RULE, width=1)
    y += 18

    # Lead ----------------------------------------------------------------
    lead = data["lead"]
    draw.text((MARGIN, y), lead["kicker"], font=font(17, bold=True),
              fill=ACCENT)
    y += 26
    y = paragraph(draw, MARGIN, y, lead["headline"], font(47, bold=True),
                  PAGE_W, leading=1.08)
    y += 4
    y = paragraph(draw, MARGIN, y, lead["deck"], font(20), PAGE_W,
                  leading=1.3, fill=(52, 48, 44))
    y += 16

    # Map band ------------------------------------------------------------
    map_h = 218
    draw_map(draw, rings, data["markers"], (MARGIN, y, SIZE - MARGIN,
                                            y + map_h))
    y += map_h + 20

    # Three columns ---------------------------------------------------------
    gap = 26
    col_w = (PAGE_W - 2 * gap) // 3
    col_bottom = y
    for i, item in enumerate(data["column"]):
        x = MARGIN + i * (col_w + gap)
        if i:
            draw.line([x - gap // 2, y, x - gap // 2, y + 168],
                      fill=(196, 188, 172), width=1)
        col_bottom = max(col_bottom,
                         story_block(draw, x, y, col_w, item, 21, 15))
    y = col_bottom + 14
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=RULE, width=1)
    y += 14

    # Six-story grid --------------------------------------------------------
    for row in range(2):
        cell_bottom = y
        for col in range(3):
            item = data["grid"][row * 3 + col]
            x = MARGIN + col * (col_w + gap)
            cell_bottom = max(cell_bottom,
                              story_block(draw, x, y, col_w, item, 18, 14))
        y = cell_bottom + 12
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=RULE, width=1)
    y += 12

    # Also today ------------------------------------------------------------
    draw.text((MARGIN, y), "ALSO TODAY", font=font(16, bold=True),
              fill=ACCENT)
    y += 24
    brief = font(13)
    per_col = math.ceil(len(data["also"]) / 3)
    for col in range(3):
        x = MARGIN + col * (col_w + gap)
        yy = y
        for item in data["also"][col * per_col:(col + 1) * per_col]:
            yy = paragraph(draw, x, yy, "· " + item, brief, col_w,
                           leading=1.2, fill=(52, 48, 44))
            yy += 3
    y = SIZE - MARGIN - 26

    # Footer ----------------------------------------------------------------
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=RULE, width=1)
    centred(draw, cx, y + 8, data["footer"], font(13), fill=FAINT)

    return img


def main(argv):
    if len(argv) != 2:
        print("usage: render.py <countries-110m.json>", file=sys.stderr)
        return 2
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    topo = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    page = build_page(data, country_rings(topo))
    page.save(OUT_FILE)
    print(f"wrote {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
