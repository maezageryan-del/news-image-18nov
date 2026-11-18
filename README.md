[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)
[![reward](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/reward.svg)](https://make.fun/bounty/news-image-20261118)

# The World in One Day — Wednesday 18 November 2026

A single square image that carries the whole of one day's world news:
Wednesday 18 November 2026, set out as the front page of a newspaper.
Rather than illustrating one event, the page works the way a picture
editor works — it decides what the day was, and puts all of it where a
reader can take it in at a glance.

## What is on the page

- **The lead story.** The road arch of the Kerch Bridge is in the sea.
  Ukraine confirms the span is destroyed; President Zelenskyy credits
  home-made drones and missiles with finishing a seven-stage
  operation, and the wreckage blocks the Sea of Azov exit for weeks.
- **A dotted world map.** Continents drawn from Natural Earth country
  outlines carry nine numbered markers for the day's datelines: the
  Kerch Bridge, Kyiv, Bahrain, Shenzhen, Alaska, DR Congo, the Andhra
  Coast, London and the Cook Islands, with a printed key beneath.
- **Three column stories** beside the map: the US strike on Iran's
  Qeshm missile site and Tehran's retaliation in Bahrain and Kuwait;
  Xi hosting Putin in Shenzhen while Trump arrives for Thursday's
  three-way summit; and Peltola's Alaska victory, which hands the
  Democrats a 56–44 Senate.
- **A six-story grid** below: Congo's Ebola outbreak passing 11,000
  cases, the US losing its measles-free status after 26 years,
  Voyager 1 reaching one light-day from Earth, Cyclone Akvan
  strengthening off the Andhra coast, Dhoni ending his IPL playing
  career, and Britain sanctioning Israeli settlement firms.
- **An "Also today" strip** of fifteen one-liners — Nvidia's results,
  Anthropic's $1.4tn pricing test, the EU's €45bn loan for Ukraine,
  Cyclone Xavier's landfall in the Cook Islands, India's record tenth
  SAFF title over Pakistan, and more.

That is 25 stories across five regions, every one a real event of
18 November 2026 as reported that day by the BBC, Reuters, AP and
Al Jazeera.

## Anatomy of the page

Top to bottom, the layout follows a broadsheet's hierarchy:

1. **Masthead** — "THE WORLD IN ONE DAY", the dateline *Wednesday,
   18 November 2026*, and the count: 25 stories, 5 regions, one page.
2. **Lead** — the Kerch Bridge headline in the largest type on the
   page, with its deck underneath.
3. **Map band** — the dotted world map on the left under the heading
   "Where the day happened", the nine numbered markers, and the key
   (1 Kerch Bridge · 2 Kyiv · 3 Bahrain · 4 Shenzhen · 5 Alaska ·
   6 DR Congo · 7 Andhra Coast · 8 London · 9 Cook Islands); the
   three column stories run down the right of the band.
4. **Grid** — six further stories in three columns of two.
5. **Also today** — fifteen one-line stories in three compact
   columns, then the source line: BBC · Reuters · AP · Al Jazeera.

## How it was made

Nothing on the page is a generated picture. A Python script
(`render.py`) typesets the page from a structured news file
(`stories.json`) — masthead, kickers, headlines, decks, the dotted map
and its markers are all drawn programmatically, so every word is crisp,
legible text that says exactly what the reporting said. The output is
`entry.png`, a 1024×1024 PNG of about 150 KB.

The submitted program, `main.ts`, does one thing: it copies the bundled
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to
`/output`). The image bytes are fixed in the repository, so repeated
grader runs produce identical output.

To rebuild the image, run `render.py` with the path to a Natural Earth
countries-110m TopoJSON file as its only argument; it reads
`stories.json` beside it and writes `entry.png` in the same folder.
Editing the day's news means editing `stories.json` only — headlines,
decks, map markers and the "Also today" lines all live there.

## Why a front page

The judge sees no news feed and weighs images against each other, so
an entry has to contain its day by itself. One illustration can show a
single story; a front page shows the day — dated, placed on a map, and
checkable headline by headline, with nothing left to outside context.
That completeness is the point of the piece.

Repository MIT-licensed.
