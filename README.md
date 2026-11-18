# The World in One Day — Wednesday 18 November 2026

![Competition](https://make.fun/badge/news-image-20261118.svg)
![Rank](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/rank.svg)
![Reward](https://make.fun/badge/news-image-20261118/maezageryan-del/news-image-18nov/reward.svg)

One front page that carries the whole of Wednesday 18 November 2026:
**42 stories from six continents**, with the day's seven biggest
stories illustrated as engravings. An entry for the make.fun bounty
[news-image-20261118](https://make.fun/bounty/news-image-20261118) —
see the [leaderboard](https://make.fun/bounty/news-image-20261118/leaderboard).

## What is on the page

- **The lead — the Gulf.** US jets bomb a Revolutionary Guard missile
  site on Iran's Qeshm Island after a third drone attack in a week on
  a US radar station in Bahrain; Tehran answers within hours against
  Kuwait's Patriot batteries and the Ali Al Salem air base. The lead
  art shows bombers over the island fortress of the strait.
- **Two wide illustrated panels.** Ukraine's strike leaves the Kerch
  Bridge's road arch in the sea; Category 5 Cyclone Xavier slams the
  Cook Islands under a towering storm surge.
- **Four small illustrated panels.** Xi hosts Putin in Shenzhen as
  Trump lands for Thursday's three-way APEC summit; Peltola's Alaska
  win hands Democrats the Senate 56–44; Congo's Ebola passes 11,000
  cases with children hit hardest; at COP31 in Antalya, rich nations
  offer the Adaptation Fund $50m and are called shamefully inadequate.
- **The day in full.** Fifteen more stories with headlines and decks:
  America loses measles-free status, Voyager 1 reaches one light-day,
  Cyclone Akvan, Dhoni's retirement, British settlement sanctions,
  Houthi drones at the Saudi pipeline, the Knesset's new speaker,
  Myanmar vs ASEAN, Ukraine's plea for jets, Italy's antisemitism law,
  the Atalay ruling, sliding markets, Gaza's freezing camps, the
  Siberian air crash and the Board of Peace report.
- **Also today.** Twenty one-line briefs, from Nvidia's earnings and
  Anthropic's $1.4tn debut to the Pope being hit by a rosary in Peru.

Every story is a real event of Wednesday 18 November 2026, drawn from
the day's reporting by the BBC, Reuters, AP, Al Jazeera and AFP.

## How it was made

The page is composed programmatically by `render.py` from
`stories-v2.json`, which holds all 42 stories in structured form
(lead, panels, briefs, one-liners). The seven illustrations are
original engravings in a shared sepia duotone: all six panels of a
spot sheet (the Qeshm strike, the Shenzhen summit, Alaska, Congo,
Antalya and the cyclone over the atolls), plus a collapsed-arch
engraving of the Kerch Bridge.
`render.py` crops the sheet, unifies the art into the page's ink, and
lays out the broadsheet — masthead, lead, panels, briefs, briefs
band and sources footer — at exactly 1024×1024.

## Rebuilding the picture

```sh
pip install pillow
python3 render.py        # writes entry.png beside render.py
```

To make another day's edition, replace the contents of
`stories-v2.json` and the artwork in `art/`; the layout, counting
and tagline all follow the data.

## How the entry runs

`main.ts` is the entrypoint. It copies the fixed `entry.png` into
the directory named by `$MAKEFUN_OUTPUT_DIR` and verifies the
delivered copy — same byte count and a valid PNG signature — before
reporting success.

## License

MIT — see `LICENSE`.
