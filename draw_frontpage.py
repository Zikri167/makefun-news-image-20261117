#!/usr/bin/env python3
"""Draw the front page for Tuesday 17 November 2026 (1024x1024 PNG).

Dev tool for the make.fun news-image-20261117 entry, version 2. It renders
the whole front page with Pillow: masthead, lead story with a taller and
more dramatic drawn illustration of the damaged Kerch Bridge, a sidebar of
three stories, a four-column grid, and a "The day in numbers" strip, inside
a thin outer frame. The entry program (main.py) only copies the rendered
entry.png; it never runs this script.

Run:  python3 draw_frontpage.py            (writes entry.png next to it)
Check: python3 draw_frontpage.py --twice  (renders twice, compares sha256)
"""
import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (244, 239, 230)      # warm newsprint off-white
INK = (26, 26, 26)           # deep charcoal
ACCENT = (184, 51, 42)       # muted crimson
SEA = (185, 203, 214)        # pale steel blue for the water
SMOKE = (154, 165, 168)      # pale grey smoke
RULE = (26, 26, 26)
FAINT = (120, 116, 108)      # grey for kickers' rules

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, w, kicker, headline, body, head_size=24, body_size=18,
          head_font=SERIF_B, gap=6):
    """One story block: red kicker, serif headline, sans body. Returns end y."""
    f_kick = font(SANS_B, 15)
    f_head = font(head_font, head_size)
    f_body = font(SANS, body_size)
    draw.text((x, y), kicker, font=f_kick, fill=ACCENT)
    y += 20
    for line in wrap(draw, headline, f_head, w):
        draw.text((x, y), line, font=f_head, fill=INK)
        y += head_size + 2
    y += gap
    for line in wrap(draw, body, f_body, w):
        draw.text((x, y), line, font=f_body, fill=INK)
        y += body_size + 4
    return y


def draw_bridge(draw, x0, y0, w, h):
    """Flat vector-style drawing of the damaged Kerch Bridge.

    Taller and more dramatic than v1: two arches (left intact, right broken
    at the gap), a wide collapsed span plunging into the water with debris,
    layered smoke plumes, and wave lines. All positions scale with h.
    """
    # frame
    draw.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], outline=INK, width=2)
    # sea across the lower part
    sea_y = y0 + int(h * 0.62)
    draw.rectangle([x0 + 2, sea_y, x0 + w - 3, y0 + h - 3], fill=SEA)
    draw.line([x0 + 2, sea_y, x0 + w - 3, sea_y], fill=INK, width=2)
    deck_y = y0 + int(h * 0.40)
    deck_h = 12
    gap_x0, gap_x1 = x0 + int(w * 0.44), x0 + int(w * 0.58)
    # intact deck left and right of the gap
    draw.rectangle([x0 + 2, deck_y, gap_x0, deck_y + deck_h], fill=INK)
    draw.rectangle([gap_x1, deck_y, x0 + w - 3, deck_y + deck_h], fill=INK)
    # piers under the intact deck, plus one tilted pier at the gap edge
    for px in (x0 + 60, x0 + 180, x0 + 440, x0 + 545):
        draw.rectangle([px, deck_y + deck_h, px + 12, sea_y], fill=INK)
    draw.polygon([(gap_x0 - 16, deck_y + deck_h), (gap_x0 - 4, deck_y + deck_h),
                  (gap_x0 + 18, sea_y), (gap_x0 + 4, sea_y)], fill=INK)
    # left arch, intact, above the left deck section
    ax0, ax1 = x0 + 30, x0 + 240
    apex = deck_y - int(h * 0.30)
    draw.line([ax0, deck_y, (ax0 + ax1) // 2, apex], fill=INK, width=4)
    draw.line([(ax0 + ax1) // 2, apex, ax1, deck_y], fill=INK, width=4)
    for t in (0.25, 0.5, 0.75):
        tx = int(ax0 + (ax1 - ax0) * t)
        ty = int(deck_y - (deck_y - apex) * (1 - abs(t - 0.5) * 2))
        draw.line([tx, ty, tx, deck_y], fill=INK, width=2)
    # right arch, bigger and broken: the rising half, ending jagged
    bx0, bx1 = x0 + int(w * 0.60), x0 + int(w * 0.97)
    bapex = deck_y - int(h * 0.30)
    draw.line([bx0, deck_y, (bx0 + bx1) // 2, bapex], fill=INK, width=4)
    draw.line([(bx0 + bx1) // 2, bapex, bx1 - 14, deck_y - 6], fill=INK,
              width=4)
    draw.line([bx1 - 14, deck_y - 6, bx1 - 4, deck_y + 4], fill=INK, width=3)
    # collapsed span: one long beam slanting down-left into the water,
    # one beam dangling down from the right edge of the gap
    draw.polygon([(gap_x0 - 6, deck_y + deck_h), (gap_x0 + 24, deck_y + deck_h),
                  (gap_x0 - 30, sea_y + int(h * 0.24)),
                  (gap_x0 - 62, sea_y + int(h * 0.28))], fill=INK)
    draw.polygon([(gap_x1 + 6, deck_y + deck_h), (gap_x1 - 20, deck_y + deck_h),
                  (gap_x1 - 32, sea_y + int(h * 0.16)),
                  (gap_x1 - 6, sea_y + int(h * 0.18))], fill=INK)
    # debris chunks floating in the water
    for dx, dyf, s in ((gap_x0 + 70, 0.08, 18),
                       (gap_x0 - 100, 0.14, 13),
                       (gap_x1 + 50, 0.20, 11)):
        dy = sea_y + int(dyf * h)
        draw.polygon([(dx, dy), (dx + s, dy + 4), (dx + s - 4, dy + 9),
                      (dx - 4, dy + 6)], fill=INK)
    # one tilted deck fragment drifting left of the wreckage
    fx, fy = gap_x0 - 130, sea_y + int(h * 0.10)
    draw.polygon([(fx, fy), (fx + 26, fy - 6), (fx + 30, fy + 2),
                  (fx + 4, fy + 8)], fill=INK)
    # wave lines around the wreckage
    for wyf, wx0, wx1 in ((0.05, gap_x0 - 90, gap_x0 + 30),
                          (0.11, gap_x0 - 60, gap_x0 + 80),
                          (0.17, gap_x1 - 40, gap_x1 + 110),
                          (0.23, x0 + 30, x0 + 200)):
        wy = sea_y + int(wyf * h)
        draw.line([wx0, wy, wx1, wy], fill=INK, width=2)
    # smoke plume rising from the gap: stacked puffs, each smaller and
    # higher, with a thin outline so they read as separate puffs; a small
    # flame at the base. Tops are clamped so no puff ever leaves the frame.
    cx = (gap_x0 + gap_x1) // 2
    # small flame at the base of the plume
    fx0, fy0 = cx - 4, deck_y + deck_h
    draw.polygon([(fx0 - 7, fy0), (fx0, fy0 - 16), (fx0 + 7, fy0),
                  (fx0 + 3, fy0 - 6), (fx0 - 3, fy0 - 6)], fill=ACCENT)
    plume = [(-6, -10, 18), (6, -36, 15), (-10, -58, 12), (4, -76, 9),
             (24, -22, 10), (-26, -30, 9)]
    for ox, oy, r in plume:
        top = deck_y + oy - r
        if top < y0 + 2:
            oy += (y0 + 2) - top
        draw.ellipse([cx + ox - r, deck_y + oy - r, cx + ox + r,
                      deck_y + oy + r], fill=SMOKE, outline=(96, 102, 105),
                     width=1)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx, mx2 = 32, 992  # content margins
    # thin outer frame around the whole page
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=3)

    # ---- masthead ----
    f_title = font(SERIF_B, 62)
    d.text((W // 2, 44), "THE WORLD DISPATCH", font=f_title, fill=INK,
           anchor="ma")
    d.line([mx, 122, mx2, 122], fill=RULE, width=2)
    f_date = font(SANS_B, 21)
    d.text((W // 2, 130), "TUESDAY 17 NOVEMBER 2026  |  WORLD EDITION",
           font=f_date, fill=INK, anchor="ma")
    d.line([mx, 160, mx2, 160], fill=RULE, width=3)
    d.line([mx, 166, mx2, 166], fill=RULE, width=1)

    # ---- lead story (left, two thirds) ----
    lx, lw = 32, 624
    y = 186
    f_kick = font(SANS_B, 19)
    d.text((lx, y), "UKRAINE WAR", font=f_kick, fill=ACCENT)
    y += 30
    f_lead = font(SERIF_B, 48)
    for line in wrap(d, "Ukraine drone strike collapses Kerch Bridge span",
                     f_lead, lw):
        d.text((lx, y), line, font=f_lead, fill=INK)
        y += 54
    y += 4
    f_stand = font(SANS, 20)
    for line in wrap(d, "Road traffic halted after a span fell into the sea. "
                        "Russia struck Kyiv's Dnipro bridges in reply.",
                     f_stand, lw):
        d.text((lx, y), line, font=f_stand, fill=INK)
        y += 26
    # illustration fills the rest of the lead block (dynamic height so the
    # headline wrap can never collide with it)
    ill_y = y + 8
    ill_h = 556 - ill_y
    if ill_h < 100:
        raise ValueError(f"lead illustration too short: {ill_h}px")
    draw_bridge(d, lx, ill_y, lw, ill_h)

    # ---- right sidebar (three stories) ----
    sx, sw = 680, 312
    y = 186
    y = block(d, sx, y, sw, "ASIA", "Trump meets Quad leaders in Manila",
              "About 1,500 protesters rallied; he meets Xi and Putin "
              "Thursday.", head_size=23, body_size=16)
    d.line([sx, y + 8, sx + sw, y + 8], fill=FAINT, width=1)
    y += 20
    y = block(d, sx, y, sw, "MIDDLE EAST", "Iran drones target US radar "
              "in Bahrain",
              "Bahrain intercepted the third attack in five days; no "
              "casualties.", head_size=23, body_size=16)
    d.line([sx, y + 8, sx + sw, y + 8], fill=FAINT, width=1)
    y += 20
    block(d, sx, y, sw, "YEMEN", "Houthi fighters advance toward Aden",
          "Government forces retreated toward Aden; Saudi commander "
          "replaced.", head_size=23, body_size=16)

    # ---- divider + secondary grid (four columns) ----
    d.line([mx, 578, mx2, 578], fill=RULE, width=2)
    cols = [
        ("EUROPE", "Five EU states plan Rwanda return hub",
         "A 2027 pilot targets about 100 rejected asylum seekers."),
        ("ASIA", "Japan scrambles jets over airspace breach",
         "Two suspected Russian aircraft violated Japanese airspace."),
        ("GAZA", "Four nations urge Israel to open Gaza",
         "UK, Australia, Canada and Italy call the aid situation "
         "catastrophic."),
        ("FRANCE", "Depardieu admits sexual assault in Paris",
         "The French actor dropped his appeal in a Paris court."),
    ]
    cw, gutter = 222, 24
    for i, (kick, head, body) in enumerate(cols):
        cx = mx + i * (cw + gutter)
        if i:
            d.line([cx - gutter // 2, 596, cx - gutter // 2, 830],
                   fill=FAINT, width=1)
        block(d, cx, 596, cw, kick, head, body, head_size=24, body_size=17)

    # ---- bottom strip: the day in numbers ----
    d.line([mx, 852, mx2, 852], fill=ACCENT, width=4)
    f_strip = font(SANS_B, 20)
    d.text((W // 2, 864), "THE DAY IN NUMBERS", font=f_strip, fill=INK,
           anchor="ma")
    nums = [
        ("1,500", "Protesters at the\nManila ASEAN summit"),
        ("3", "Drone attacks on the\nBahrain base in 5 days"),
        ("5", "EU states planning\na Rwanda return hub"),
        ("4", "Oil tankers hit near\nHormuz in 24 hours"),
    ]
    bw = 240
    f_num = font(SERIF_B, 50)
    f_lab = font(SANS, 16)
    for i, (num, lab) in enumerate(nums):
        bx = mx + i * bw
        d.text((bx + bw // 2, 898), num, font=f_num, fill=ACCENT,
               anchor="ma")
        ly = 954
        for line in lab.split("\n"):
            d.text((bx + bw // 2, ly), line, font=f_lab, fill=INK,
                   anchor="ma")
            ly += 20
    return img


def main():
    out = Path(__file__).with_name("entry.png")
    img = render()
    img.save(out, format="PNG")
    data = out.read_bytes()
    print(f"wrote {out} {len(data)} bytes sha256="
          f"{hashlib.sha256(data).hexdigest()}")
    if "--twice" in sys.argv:
        img2 = render()
        buf2 = Path("/tmp/entry2.png")
        img2.save(buf2, format="PNG")
        same = buf2.read_bytes() == data
        print(f"second render byte-identical: {same}")
        return 0 if same else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
