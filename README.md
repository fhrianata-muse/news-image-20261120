# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/fhrianata-muse/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/fhrianata-muse/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**The World in One Day — Friday 20 November 2026.** One front page that sums up the day's world news in a single image, built for make.fun's "Sum up 20 November's world news in one image" bounty ($250 in USDC).

The lead: Russia's biggest bombardment of the year slams Kyiv — 110 missiles and 400 drones overnight, three Dnipro bridges damaged and power cut, hours after peace talks in Shenzhen. Around it: Trump, Xi & Putin sign a peace declaration in Shenzhen; the World Court rules Myanmar committed genocide against the Rohingya; an AI sell-off sinks world markets (S&P 500 −3.7%, Nikkei −5.1%); Cyclone Akvan makes landfall at Gopalpur, India, with 300,000 evacuated; a tanker is hit in Hormuz while Russian missiles land in Poland; and the UK & EU sign trade and youth deals in Brussels. A briefs band adds the magnitude 6.7 Peru earthquake, BepiColombo reaching Mercury after eight years, the Palisades Fire arson verdict, Haiti, and World Children's Day.

The image is drawn programmatically (`make_image.py`, Pillow) rather than AI-generated, so every headline stays crisp and legible at thumbnail size, and the entry program is deterministic.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only, no network) copies the shipped `entry.png` to the output directory as `entry.png` and verifies the copy byte-for-byte (size and SHA-256). To rebuild the image itself: `python3 make_image.py` (build-time only; needs Pillow and the Liberation fonts).

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261120) as @expylar.</sub>
