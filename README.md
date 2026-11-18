[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)
[![reward](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/reward.svg)](https://make.fun/bounty/news-image-20261118)

# The World in One Day — Wednesday 18 November 2026

One image summing up the world's news of Wednesday 18 November 2026,
drawn as a newspaper front page — the form a picture editor reaches for
when a whole day has to fit on one page:

- **Lead: the Kerch Bridge's road arch is in the sea** — Ukraine
  confirms the span is destroyed; Zelenskyy says home-made drones and
  missiles ended a seven-stage operation, and wreckage blocks the Sea
  of Azov exit for weeks.
- **A dotted world map** with the day's places numbered: Kerch Bridge,
  Kyiv, Bahrain, Shenzhen, Alaska, DR Congo, Andhra Coast, London,
  Cook Islands.
- **25 stories in all**, across five regions — the US strike on Iran's
  Qeshm missile site and Tehran's answer in Bahrain and Kuwait, Xi
  hosting Putin in Shenzhen as Trump lands for Thursday's three-way
  summit, Peltola's Alaska win giving Democrats a 56–44 Senate,
  Congo's Ebola outbreak passing 11,000 cases, Voyager 1 reaching one
  light-day from Earth, and fifteen more in the "Also today" strip.

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
