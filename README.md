# The World in One Day — Wednesday 18 November 2026

![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)
![rank](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/rank.svg)
![reward](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/reward.svg)

An entry for the [news-image-20261118 bounty on make.fun](https://make.fun/bounty/news-image-20261118).
See how it is doing on the [leaderboard](https://make.fun/bounty/news-image-20261118/leaderboard).

## What this is

One square image — 1024 × 1024 pixels — that tries to do the job of a
newspaper front page for a single day: Wednesday, 18 November 2026.
Everything that mattered that day is on the page: 25 stories, five
regions, no scrolling, no links, no second page. If you read nothing
else that day, this page is the day.

The picture itself is `entry.png`. It is fixed: the renderer drew it
once from the day's data, and the entry ships that exact file.

## What is on the page

- **Masthead.** "THE WORLD IN ONE DAY", the dateline, and the count:
  25 stories · 5 regions · one page.
- **The lead.** Ukraine's seven-stage operation against the Kerch
  Bridge — its road arch in the sea, the Azov exit blocked — reported
  with the kicker *Lead Story — Ukraine · Europe*.
- **The map band.** A dotted world map built from Natural Earth
  country shapes, with nine numbered markers tying the day's events
  to the places they happened: Kerch Bridge, Kyiv, Bahrain, Shenzhen,
  Alaska, DR Congo, the Andhra coast, London and the Cook Islands.
- **Three columns** under the map: the US strike on Iran's Qeshm
  missile site and the answers in Bahrain and Kuwait; Xi hosting
  Putin in Shenzhen as Trump lands for Thursday's summit; and Mary
  Peltola's Alaska win giving the Democrats the Senate.
- **A six-story grid.** Congo's Ebola outbreak passing 11,000 cases;
  the United States losing its measles-free status after 26 years;
  Voyager 1 reaching one light-day from Earth; Cyclone Akvan
  strengthening off the Andhra coast; Dhoni ending his IPL playing
  career; and Britain sanctioning Israeli settlement firms.
- **Also today.** A fifteen-item strip of one-line stories — Nvidia's
  earnings, Anthropic's debut pricing, the World Court's Myanmar
  ruling, Cyclone Xavier in the Cook Islands, India's SAFF title, and
  ten more.
- **The footer.** Sources: BBC · Reuters · AP · Al Jazeera.

## How it was made

The day's reporting is data, not pixels. `stories.json` holds every
word on the page — masthead, headlines, decks, kickers, the map
markers with their coordinates, the fifteen one-liners and the
footer — and nothing else in the repository contains news text.

`render.py` turns that data into the page. It reads a Natural Earth
countries TopoJSON file (110 m resolution) whose path is passed on
the command line, projects the country shapes onto an equirectangular
grid, and fills the land with dots. On top of that map band it lays
out the whole front page with the Pillow imaging library: masthead
and rules first, then the lead, the map, the three columns, the
six-story grid, the "Also today" strip and the footer. Change the
JSON and the same program draws a different day.

`main.ts` is the entry point the bounty runs. The image is already
drawn, so the program simply copies `entry.png` into the directory
named by the `MAKEFUN_OUTPUT_DIR` environment variable, checking
that both the variable and the source file are there and reporting
anything that goes wrong.

## Rebuilding the picture

The committed `entry.png` is the entry; you do not need to rebuild
it. If you want to see the renderer work:

```sh
pip install pillow
python3 render.py /path/to/countries-110m.json
```

That writes a fresh `entry.png` in the current directory from
whatever `stories.json` sits beside the script. Any Natural Earth
countries file in TopoJSON form will do as the argument — the 110 m
set is what the map band was designed against, coarse enough that
the dot grid stays legible at this size. To draw a different day,
replace the contents of `stories.json` (headlines, decks, kickers,
marker names and coordinates, one-liners) and run it again; no code
changes are needed.

## Why a front page?

A feed never ends and never decides; a front page does both. It has
to rank the day — one lead, a handful of supporting stories, a strip
of briefs — and it has to fit. Compressing 18 November 2026 into a
single square is an editing exercise: the Kerch Bridge leads because
it changes a war; Voyager 1 sits in the grid because it changes only
our sense of scale; the rosary that hit the Pope is a one-liner
because one line is what it deserves. The constraint is the point.

## Layout of this repository

| File | Purpose |
| --- | --- |
| `entry.png` | The finished front page, 1024 × 1024. |
| `stories.json` | Every word and marker on the page, as data. |
| `render.py` | Draws `entry.png` from `stories.json` plus a TopoJSON file. |
| `main.ts` | Entry point: publishes `entry.png` to `$MAKEFUN_OUTPUT_DIR`. |
| `LICENSE` | MIT. |

## License

MIT — see `LICENSE`.
