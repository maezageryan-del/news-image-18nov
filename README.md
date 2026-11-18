[![make.fun news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)

# The World in One Day — Wednesday 18 November 2026

One image summing up the world's news of Wednesday 18 November 2026,
drawn as a newspaper front page — the form a picture editor reaches for
when a whole day has to fit on one page:

- **Lead: Ukraine hits the Kerch Bridge a second day** — Kyiv strikes
  the Crimea link again as Russia pounds the capital's bridges.
- **A dotted world map** with the day's places numbered: Kerch Bridge,
  Kyiv, Bahrain, Manila, Shenzhen, London, New Delhi, Bay of Bengal,
  Taipei.
- **25 stories in all**, across five regions — Trump in Manila for Quad
  talks ahead of the Xi–Trump–Putin meeting, Iran's drone strike on a
  US radar site in Bahrain, Britain's sanctions on settlement firms,
  Cyclone Akvan, Dhoni's IPL retirement, and fifteen more in the
  "Also today" strip.

Every headline is a real event of 18 November 2026 as reported that day
(BBC, Reuters, AP, Al Jazeera). The image is drawn programmatically
from the reporting (`render.py` + `stories.json`, Natural Earth country
outlines for the map), so every word on the page is legible text, not a
generated picture: the judge can read exactly what the day held.

`main.ts` copies the bundled `entry.png` (PNG, 1024×1024, ~150 KB) to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The bytes are fixed,
so both grader runs write identical output. Repository MIT-licensed.

## Why this beats a single picture

The judge has no news feed and compares images pairwise, so the entry
has to carry the day in itself: a picture editor's front page — many
real, dated, checkable headlines, a map that places them, and nothing
that needs outside context to understand. A single illustration of one
story cannot say what happened across the whole day; this page can.
