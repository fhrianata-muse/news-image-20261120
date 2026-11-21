#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261120.

"Sum up 20 November's world news in one image" — a one-page newspaper
front page for Friday 20 November 2026, drawn programmatically with PIL
so every word stays crisp (no AI-image garbled text) and the output is
byte-for-byte deterministic.

Stories (all first reported on 20 November 2026, verified against
Reuters/CNN, IMD, UKMTO and UN reporting before drawing):
  LEAD  Russia's biggest bombardment of the year hits Kyiv overnight:
        ~110 missiles and ~400 drones, three Dnipro bridges damaged,
        power cut — hours after the Shenzhen trilateral summit.
  1     Trump, Xi and Putin issue a joint peace declaration in Shenzhen;
        Chancellor Merz rejects a "new Yalta" settled without Europe.
  2     World Court (ICJ): Myanmar committed genocide against the
        Rohingya — the first time the court held a state responsible.
  3     AI sell-off: S&P 500 -3.7% into correction, Nikkei -5.06%.
  4     Cyclone Akvan landfall near Gopalpur, Odisha: gusts 90 km/h,
        300,000+ evacuated, no major damage in first reports.
  5     Tanker struck in the Strait of Hormuz (UKMTO warning); Russian
        missiles land in Poland — NATO calls it a grave violation.
  6     UK and EU sign Brussels deals: food trade, carbon markets,
        youth mobility.
  Briefs: magnitude 6.7 earthquake in central Peru; BepiColombo reaches
        Mercury after eight years; Los Angeles jury convicts the
        Palisades Fire arsonist; Haitian forces kill 34 gang suspects;
        World Children's Day.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
INK = (20, 24, 38)
NAVY = (15, 42, 82)
RED = (163, 18, 32)
GOLD = (176, 124, 16)
SKY = (16, 28, 58)
RIVER = (38, 84, 124)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.12, align="left"):
    """Draw wrapped text; returns the y just below the block."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        if align == "center":
            w = draw.textlength(line, font=fnt)
            draw.text((x + (max_w - w) / 2, y), line, font=fnt, fill=fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def fit_font(draw, text, path, size, max_w):
    """Shrink a font until the single line fits max_w pixels."""
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def panel(draw, box, kicker, headline, sub, accent):
    """One news panel: accent rule, kicker, serif headline, sans sub."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, outline=INK, width=2)
    draw.rectangle((x0, y0, x1, y0 + 8), fill=accent)
    cx = x0 + 16
    draw.text((cx, y0 + 18), kicker, font=font(SANS_B, 18), fill=accent)
    y = text_block(draw, (cx, y0 + 44), headline, font(SERIF_B, 25),
                   INK, x1 - cx - 14, leading=1.08)
    text_block(draw, (cx, y + 6), sub, font(SANS, 18), (52, 56, 66),
               x1 - cx - 14, leading=1.14)


def draw_kyiv(draw, box):
    """Lead illustration: Kyiv at night, the Dnipro, three bridges."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    # stars
    for sx, sy in [(30, 18), (90, 40), (150, 14), (230, 30), (310, 20),
                   (60, 66), (200, 58), (350, 44), (120, 88), (280, 80)]:
        draw.ellipse((x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3),
                     fill=(210, 216, 235))
    # skyline silhouettes
    base = y1 - 92
    for bx, bw, bh in [(8, 34, 62), (48, 26, 88), (80, 40, 54), (126, 24, 96),
                       (156, 36, 66), (250, 30, 78), (286, 44, 58), (336, 26, 84),
                       (366, 30, 62)]:
        draw.rectangle((x0 + bx, base - bh, x0 + bx + bw, base), fill=(8, 12, 26))
    # lit windows
    for wx, wy in [(56, 30), (64, 52), (134, 22), (140, 48), (262, 36),
                   (300, 26), (344, 30), (96, 40), (168, 44), (316, 52)]:
        draw.rectangle((x0 + wx, base - 60 + wy, x0 + wx + 4, base - 56 + wy),
                       fill=(250, 197, 92))
    # missile trails arcing down (kept inside the illustration box)
    for tx, ty, ex in [(60, 8, 118), (170, 4, 216), (286, 10, 322)]:
        draw.arc((x0 + tx, y0 + ty, x0 + ex + 62, y0 + ty + 140),
                 start=300, end=35, fill=(255, 120, 90), width=3)
        draw.ellipse((x0 + ex - 4, y0 + ty + 92, x0 + ex + 4, y0 + ty + 100),
                     fill=(255, 176, 66))
    # explosion star over the middle bridge
    cx, cy = x0 + 205, base - 6
    for dx, dy in [(0, -16), (11, -11), (16, 0), (11, 11), (0, 16),
                   (-11, 11), (-16, 0), (-11, -11)]:
        draw.line((cx, cy, cx + dx, cy + dy), fill=(255, 140, 40), width=4)
    draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=(255, 196, 64))
    # river
    draw.rectangle((x0, base, x1, y1), fill=RIVER)
    for ry in (14, 34, 56, 76):
        draw.line((x0 + 12, base + ry, x1 - 12, base + ry),
                  fill=(86, 132, 178), width=2)
    # three bridges: left intact, middle broken, right intact
    deck = base + 8
    for bx0, bx1, broken in [(18, 128, False), (150, 262, True), (284, 392, False)]:
        draw.rectangle((x0 + bx0, deck, x0 + bx1, deck + 7), fill=(228, 232, 240))
        draw.line((x0 + bx0 + 8, deck + 26, x0 + bx0 + 8, deck),
                  fill=(228, 232, 240), width=4)
        draw.line((x0 + bx1 - 8, deck + 26, x0 + bx1 - 8, deck),
                  fill=(228, 232, 240), width=4)
        if broken:
            mid = (bx0 + bx1) // 2
            draw.rectangle((x0 + mid - 12, deck - 2, x0 + mid + 12, deck + 10),
                           fill=RIVER)
            draw.line((x0 + mid - 12, deck + 2, x0 + mid + 2, deck + 16),
                      fill=(228, 232, 240), width=5)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # page margin

    # ---- masthead ------------------------------------------------------
    centered(d, W / 2, 18, "THE DAY'S WORLD NEWS IN ONE IMAGE",
             font(SANS_B, 21), RED)
    title = "THE WORLD IN ONE DAY"
    centered(d, W / 2, 46, title,
             fit_font(d, title, SERIF_B, 84, W - 2 * m), INK)
    d.line((m, 146, W - m, 146), fill=INK, width=3)
    d.rectangle((m, 154, W - m, 206), fill=RED)
    centered(d, W / 2, 162, "FRIDAY 20 NOVEMBER 2026", font(SANS_B, 40), WHITE)

    # ---- lead story: Kyiv ----------------------------------------------
    lx0, ly0, lx1, ly1 = m, 220, W - m, 512
    d.rectangle((lx0, ly0, lx1, ly1), outline=INK, width=3)
    draw_kyiv(d, (lx0 + 10, ly0 + 10, lx0 + 420, ly1 - 10))
    tx = lx0 + 442
    d.text((tx, ly0 + 16), "EUROPE — WAR", font=font(SANS_B, 21), fill=RED)
    y = text_block(d, (tx, ly0 + 46),
                   "RUSSIA'S BIGGEST BOMBARDMENT OF THE YEAR SLAMS KYIV",
                   font(SERIF_B, 38), INK, lx1 - tx - 16, leading=1.1)
    y = text_block(d, (tx, y + 8),
                   "110 missiles and 400 drones overnight. Three Dnipro "
                   "bridges damaged and power cut — hours after peace "
                   "talks in Shenzhen.",
                   font(SANS, 20), (52, 56, 66), lx1 - tx - 16, leading=1.14)
    # stat chips
    cx = tx
    for label in ("110 MISSILES", "400 DRONES", "3 BRIDGES HIT"):
        f = font(SANS_B, 19)
        w = d.textlength(label, font=f) + 22
        d.rectangle((cx, ly1 - 42, cx + w, ly1 - 12), fill=NAVY)
        d.text((cx + 11, ly1 - 36), label, font=f, fill=WHITE)
        cx += w + 10

    # ---- six panels, two rows of three ---------------------------------
    panels = [
        ("ASIA — DIPLOMACY", NAVY,
         "TRUMP, XI & PUTIN SIGN PEACE DECLARATION",
         "Historic summit of the three powers in Shenzhen. Merz: no "
         "new Yalta without Europe."),
        ("JUSTICE — THE HAGUE", GOLD,
         "COURT: MYANMAR COMMITTED GENOCIDE",
         "First ruling holding a state responsible for genocide, "
         "against the Rohingya."),
        ("ECONOMY — GLOBAL", RED,
         "AI SELL-OFF SINKS WORLD MARKETS",
         "S&P 500 falls 3.7% into correction; Tokyo's Nikkei drops "
         "5.1% as AI costs bite."),
        ("INDIA — DISASTER", (10, 110, 130),
         "CYCLONE AKVAN MAKES LANDFALL IN INDIA",
         "Hits Gopalpur, Odisha, gusting 90 km/h. 300,000 evacuated; "
         "no major damage reported."),
        ("ENERGY — NATO", (90, 60, 140),
         "TANKER HIT IN HORMUZ; MISSILES IN POLAND",
         "NATO calls the missiles in Poland a grave violation of its "
         "airspace."),
        ("EUROPE — BRUSSELS", (24, 110, 60),
         "UK & EU SIGN TRADE AND YOUTH DEALS",
         "Summit agrees food trade, carbon markets and youth mobility "
         "for 18 to 31 year olds."),
    ]
    gap = 14
    pw = (W - 2 * m - 2 * gap) // 3
    rows = [(524, 732), (738, 946)]
    for i, (kicker, accent, head, sub) in enumerate(panels):
        r, c = divmod(i, 3)
        x0 = m + c * (pw + gap)
        y0, y1 = rows[r]
        panel(d, (x0, y0, x0 + pw, y1), kicker, head, sub, accent)

    # ---- briefs ticker ---------------------------------------------------
    d.rectangle((0, 954, W, H), fill=INK)
    brief1 = ("IN BRIEF — PERU EARTHQUAKE MAGNITUDE 6.7  •  BEPICOLOMBO "
              "REACHES MERCURY AFTER 8 YEARS")
    brief2 = ("PALISADES FIRE ARSONIST CONVICTED  •  HAITI: 34 GANG "
              "SUSPECTS KILLED  •  WORLD CHILDREN'S DAY")
    centered(d, W / 2, 964, brief1,
             fit_font(d, brief1, SANS_B, 19, W - 32), WHITE)
    centered(d, W / 2, 992, brief2,
             fit_font(d, brief2, SANS_B, 19, W - 32), (214, 200, 160))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out}: {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    build()
