# The World Dispatch — Tuesday 17 November 2026

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Zikri167/makefun-news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Zikri167/makefun-news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

One image summing up the world news of Tuesday 17 November 2026, drawn as a
newspaper front page: the lead story is Ukraine's drone strike collapsing a
span of the Kerch Bridge, with Russia's reply strike on Kyiv's Dnipro
bridges; alongside it, Trump's Quad meeting in Manila, Iran's drone attack on
the US radar base in Bahrain, the Houthi advance toward Aden, the EU's Rwanda
return-hub plan, Japan scrambling jets, the Gaza aid appeal, and Depardieu's
admission in Paris — closed by a "day in numbers" strip.

## How it works

`draw_frontpage.py` renders the front page with Pillow into `entry.png`
(1024x1024, deterministic: two runs write identical bytes). `main.py`
(Python 3.13, standard library only) checks the image — whole PNG, at most
1 MiB, at most 1024x1024 — and copies its exact bytes to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).

```sh
python3 draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Entry

Competition: [news-image-20261117 on make.fun](https://make.fun/bounty/news-image-20261117)
