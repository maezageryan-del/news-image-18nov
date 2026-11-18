#!/usr/bin/env python3
"""
render.py — compose the v2 front page for "The World in One Day",
Wednesday 18 November 2026 (make.fun bounty news-image-20261118).

Reads stories-v2.json (the day's news, 42 stories) and the engraved
artwork in art/, and writes a single 1024x1024 front page to
entry.png beside this file.

    python3 render.py

Artwork handling: the six spot illustrations live on one generated
sheet (art/spots-grid.png, 3 columns x 2 rows); this script crops the
cells out, converts every piece to a shared sepia duotone so the page
reads as one printed sheet, and lays the page out like a broadsheet:
masthead, illustrated lead, two wide illustrated panels, four small
illustrated panels, a 15-item news briefs block and a 20-line
"Also today" band.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "stories-v2.json")
ART = os.path.join(HERE, "art")
OUT = os.path.join(HERE, "entry.png")

PAGE = 1024
MARGIN = 34
RIGHT = PAGE - MARGIN
WIDTH = RIGHT - MARGIN

PAPER = (244, 236, 218)
INK = (30, 22, 14)
ACCENT = (142, 44, 30)
FAINT = (112, 96, 74)
RULE = (58, 44, 30)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    """Greedy word wrap; returns a list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, maxw, max_lines, sizes, path):
    """First (font, lines) at the largest size that fits max_lines."""
    for size in sizes:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, maxw)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(path, sizes[-1])
    return fnt, wrap(draw, text, fnt, maxw)


def tracked(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with letter tracking; returns the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x - tracking


def tracked_center(draw, cx, y, text, fnt, fill, tracking=3):
    total = sum(draw.textlength(c, font=fnt) for c in text) + tracking * (len(text) - 1)
    tracked(draw, (cx - total / 2, y), text, fnt, fill, tracking)
    return total


def block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, y, x0=MARGIN, x1=RIGHT, fill=RULE, w=1):
    draw.rectangle([x0, y, x1, y + w - 1], fill=fill)


# ---------------------------------------------------------------- art

def cover(img, w, h, y_bias=0.5):
    """Scale img to cover (w, h) and centre-crop (y_bias: 0 top, 1 bottom)."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    img = img.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    x = (img.size[0] - w) // 2
    y = int((img.size[1] - h) * y_bias)
    return img.crop((x, y, x + w, y + h))


def duotone(img, w, h, y_bias=0.5):
    """Unify a piece of art into the page's sepia ink duotone."""
    img = cover(img.convert("RGB"), w, h, y_bias)
    grey = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    return ImageOps.colorize(grey, black=(36, 26, 16), mid=(148, 126, 96),
                             white=(247, 239, 221))


def load_art():
    sheet = Image.open(os.path.join(ART, "spots-grid.png"))
    sw, sh = sheet.size
    cw, ch = sw // 3, sh // 2
    inset = 14

    def cell(col, row):
        return sheet.crop((col * cw + inset, row * ch + inset,
                           (col + 1) * cw - inset, (row + 1) * ch - inset))

    bridge = Image.open(os.path.join(ART, "kerch-bridge.png"))
    bridge = bridge.crop((0, 0, bridge.size[0], int(bridge.size[1] * 0.90)))
    return {
        "qeshm": cell(0, 0),
        "apec": cell(1, 0),
        "alaska": cell(2, 0),
        "ebola": cell(0, 1),
        "cop31": cell(1, 1),
        "cyclone": cell(2, 1),
        "bridge": bridge,
    }


# ---------------------------------------------------------------- page

def main():
    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)
    art = load_art()

    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)

    total = (1 + len(data["panels_big"]) + len(data["panels_small"])
             + len(data["briefs"]) + len(data["also"]))

    # ---- masthead -------------------------------------------------
    hline(draw, 26, w=1)
    f_date = font(SANS_B, 13)
    draw.text((MARGIN, 34), data["dateline"], font=f_date, fill=INK)
    ed = data["edition"]
    draw.text((RIGHT - draw.textlength(ed, font=f_date), 34), ed,
              font=f_date, fill=INK)
    f_title = font(SERIF_B, 58)
    title = data["masthead"]
    draw.text(((PAGE - draw.textlength(title, font=f_title)) / 2, 48),
              title, font=f_title, fill=INK)
    tagline = "%d STORIES · SIX CONTINENTS · ONE PAGE" % total
    tracked_center(draw, PAGE / 2, 118, tagline, font(SANS_B, 13), ACCENT)
    hline(draw, 138, w=3)
    hline(draw, 144, w=1)

    # ---- lead ------------------------------------------------------
    lead = data["lead"]
    y = 156
    tracked(draw, (MARGIN, y), lead["kicker"], font(SANS_B, 13), ACCENT)
    y += 20
    f_head, lines = fit(draw, lead["headline"], WIDTH, 2,
                        (40, 37, 34, 31), SERIF_B)
    y = block(draw, MARGIN, y, lines, f_head, INK, int(f_head.size * 1.12))
    y += 8
    art_w, art_h = 444, 140
    page.paste(duotone(art[lead["art"]], art_w, art_h), (MARGIN, y))
    draw.rectangle([MARGIN, y, MARGIN + art_w - 1, y + art_h - 1],
                   outline=RULE, width=1)
    cap = wrap(draw, lead["caption"], font(SERIF_I, 11), art_w)
    block(draw, MARGIN, y + art_h + 5, cap, font(SERIF_I, 11), FAINT, 13)
    deck_x = MARGIN + art_w + 18
    deck_lines = wrap(draw, lead["deck"], font(SERIF, 15), RIGHT - deck_x)
    block(draw, deck_x, y, deck_lines, font(SERIF, 15), INK, 21)
    lead_bottom = max(y + art_h + 5 + 13 * len(cap),
                      y + 21 * len(deck_lines)) + 6
    hline(draw, lead_bottom, w=1)

    # ---- two wide illustrated panels -------------------------------
    y = lead_bottom + 12
    pw = (WIDTH - 16) // 2
    row1_end = y
    for i, panel in enumerate(data["panels_big"]):
        x = MARGIN + i * (pw + 16)
        page.paste(duotone(art[panel["art"]], pw, 76, y_bias=0.42), (x, y))
        draw.rectangle([x, y, x + pw - 1, y + 75], outline=RULE, width=1)
        py = y + 82
        tracked(draw, (x, py), panel["kicker"], font(SANS_B, 10), ACCENT,
                tracking=2)
        py += 15
        f_ph, plines = fit(draw, panel["headline"], pw, 2, (19, 17, 16),
                           SERIF_B)
        py = block(draw, x, py, plines, f_ph, INK, int(f_ph.size * 1.12))
        dlines = wrap(draw, panel["deck"], font(SERIF, 11), pw)
        py = block(draw, x, py + 1, dlines[:2], font(SERIF, 11), INK, 13)
        row1_end = max(row1_end, py)
    row1_bottom = row1_end + 10
    hline(draw, row1_bottom, w=1)

    # ---- four small illustrated panels ------------------------------
    y = row1_bottom + 10
    qw = (WIDTH - 3 * 12) // 4
    row2_end = y
    for i, panel in enumerate(data["panels_small"]):
        x = MARGIN + i * (qw + 12)
        page.paste(duotone(art[panel["art"]], qw, 44, y_bias=0.40), (x, y))
        draw.rectangle([x, y, x + qw - 1, y + 43], outline=RULE, width=1)
        py = y + 49
        tracked(draw, (x, py), panel["kicker"], font(SANS_B, 9), ACCENT,
                tracking=2)
        py += 13
        f_ph, plines = fit(draw, panel["headline"], qw, 2, (14, 13, 12),
                           SERIF_B)
        py = block(draw, x, py, plines, f_ph, INK, int(f_ph.size * 1.14))
        dlines = wrap(draw, panel["deck"], font(SERIF, 10), qw)
        py = block(draw, x, py + 1, dlines[:1], font(SERIF, 10), INK, 12)
        row2_end = max(row2_end, py)
    row2_bottom = row2_end + 8
    hline(draw, row2_bottom, w=1)

    # ---- the day in full: briefs ------------------------------------
    y = row2_bottom + 9
    tracked(draw, (MARGIN, y), "THE DAY IN FULL", font(SANS_B, 12), ACCENT)
    y += 19
    bw = (WIDTH - 2 * 14) // 3
    for idx, brief in enumerate(data["briefs"]):
        col, row = idx % 3, idx // 3
        x = MARGIN + col * (bw + 14)
        by = y + row * 30
        f_bh, blines = fit(draw, brief["headline"], bw, 1, (12, 11, 10),
                           SERIF_B)
        block(draw, x, by, blines[:1], f_bh, INK, 14)
        dlines = wrap(draw, brief["deck"], font(SERIF, 10), bw)
        block(draw, x, by + 14, dlines[:1], font(SERIF, 10), INK, 12)
    briefs_bottom = y + 5 * 30 + 2
    hline(draw, briefs_bottom, w=1)

    # ---- also today --------------------------------------------------
    y = briefs_bottom + 8
    tracked(draw, (MARGIN, y), "ALSO TODAY", font(SANS_B, 11), ACCENT)
    y += 16
    aw = (WIDTH - 3 * 12) // 4
    f_also = font(SERIF, 10)
    for idx, item in enumerate(data["also"]):
        col, row = idx % 4, idx // 4
        x = MARGIN + col * (aw + 12)
        line = item
        while draw.textlength(line, font=f_also) > aw and len(line) > 8:
            line = line[:-1]
        if line != item:
            line = line.rstrip(" .,;:") + "…"
        draw.text((x, y + row * 12), line, font=f_also, fill=INK)
    also_bottom = y + 5 * 12 + 3
    hline(draw, also_bottom, w=1)

    # ---- footer -------------------------------------------------------
    foot = data["footer"]
    f_foot = font(SERIF_I, 10)
    draw.text(((PAGE - draw.textlength(foot, font=f_foot)) / 2,
               also_bottom + 7), foot, font=f_foot, fill=FAINT)

    page.save(OUT)
    print("wrote %s (%d stories, bottom at %d)" % (OUT, total, also_bottom + 22))
    return 0


if __name__ == "__main__":
    sys.exit(main())
