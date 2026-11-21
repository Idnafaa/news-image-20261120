"""Render the v3 front page for news-image-20261120.

A clean, hero-led broadsheet: 31 stories from 19-20 Nov 2026 (all verified
in the v1/v2 records). Drawn with PIL only; deterministic output.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
CW = W - 2 * MARGIN  # content width = 976

PAPER = (246, 240, 226)
INK = (24, 24, 28)
NAVY = (18, 38, 84)
RED = (178, 34, 34)
GREY = (92, 88, 80)
RULE = (60, 58, 54)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def gradient(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


# ---------------------------------------------------------------- scenes

def scene_shenzhen(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (38, 58, 120), (232, 150, 92))
    # rising sun
    cx, cy, r = (x0 + x1) // 2, y1 - 66, 40
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 205, 110))
    # skyline silhouettes
    base = y1
    towers = [(0, 70, 60), (58, 105, 52), (108, 62, 66), (172, 118, 48),
              (218, 84, 58), (274, 128, 54), (326, 76, 62), (386, 110, 50),
              (434, 66, 60), (492, 96, 56), (546, 120, 52), (596, 72, 64),
              (658, 104, 50), (706, 80, 58), (762, 124, 54), (814, 68, 62),
              (874, 98, 52), (924, 78, 52)]
    for dx, hgt, wid in towers:
        draw.rectangle([x0 + dx, base - hgt, x0 + dx + wid, base], fill=(16, 22, 44))
    # three flagpoles
    poles = [(x0 + 190, "us"), (cx, "cn"), (x1 - 190, "ru")]
    for px, kind in poles:
        draw.line([(px, y0 + 26), (px, base)], fill=(240, 240, 240), width=3)
        fw, fh = 84, 48
        fx, fy = px + 3, y0 + 26
        if kind == "us":
            for i in range(7):
                col = (178, 34, 52) if i % 2 == 0 else (245, 245, 245)
                draw.rectangle([fx, fy + i * fh // 7, fx + fw, fy + (i + 1) * fh // 7], fill=col)
            draw.rectangle([fx, fy, fx + 36, fy + 26], fill=(20, 40, 110))
            for r_ in range(3):
                for c_ in range(4):
                    draw.ellipse([fx + 4 + c_ * 8, fy + 4 + r_ * 8, fx + 8 + c_ * 8, fy + 8 + r_ * 8],
                                 fill=(255, 255, 255))
        elif kind == "cn":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(200, 30, 30))
            draw.ellipse([fx + 7, fy + 7, fx + 21, fy + 21], fill=(250, 210, 60))
            for sx, sy in [(28, 6), (32, 14), (32, 22), (28, 30)]:
                draw.ellipse([fx + sx, fy + sy, fx + sx + 6, fy + sy + 6], fill=(250, 210, 60))
        else:
            draw.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(245, 245, 245))
            draw.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(30, 70, 160))
            draw.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(190, 30, 40))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def scene_gta(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (52, 40, 110), (238, 120, 80))
    cx, cy, r = x0 + (x1 - x0) // 2, y1 - 30, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(252, 190, 90))
    base = y1
    for dx, hgt, wid in [(8, 44, 34), (46, 62, 30), (80, 38, 36), (190, 52, 32),
                         (226, 66, 30), (260, 42, 34)]:
        draw.rectangle([x0 + dx, base - hgt, x0 + dx + wid, base], fill=(20, 18, 40))
    # palms
    for px in (x0 + 130, x0 + 162):
        top_x, top_y = px + 8, base - 42
        draw.line([(px, base), (top_x, top_y)], fill=(20, 18, 40), width=4)
        for ang in (-55, -28, 0, 28, 55):
            ex = top_x + int(24 * math.sin(math.radians(ang)))
            ey = top_y - int(10 * math.cos(math.radians(ang))) + 6
            mx = top_x + int(13 * math.sin(math.radians(ang)))
            my = top_y - int(11 * math.cos(math.radians(ang)))
            draw.line([(top_x, top_y), (mx, my), (ex, ey)], fill=(20, 18, 40), width=3)
    big = font(SERIF_B, 44)
    draw.text((x1 - 78, y0 + 8), "VI", font=big, fill=(250, 240, 220))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def scene_ipo(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 30, 70))
    base = y1 - 12
    heights = [22, 34, 48, 66]
    bw = 46
    for i, hgt in enumerate(heights):
        bx = x0 + 26 + i * (bw + 18)
        col = (240, 140, 60) if i == 3 else (90, 130, 200)
        draw.rectangle([bx, base - hgt, bx + bw, base], fill=col)
    pts = [(x0 + 30, base - 26), (x0 + 96, base - 38), (x0 + 162, base - 50), (x0 + 228, base - 68)]
    draw.line(pts, fill=(120, 230, 150), width=4)
    draw.polygon([(x0 + 228, base - 68), (x0 + 212, base - 66), (x0 + 222, base - 54)],
                 fill=(120, 230, 150))
    draw.text((x0 + 42, y0 + 6), "$97.17", font=font(SANS_B, 20), fill=(250, 240, 220))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def scene_scales(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(22, 40, 86))
    cx = (x0 + x1) // 2
    top = y0 + 8
    gold = (232, 196, 110)
    draw.line([(cx, top), (cx, y1 - 8)], fill=gold, width=4)
    draw.line([(cx - 88, top + 4), (cx + 88, top + 4)], fill=gold, width=4)
    draw.ellipse([cx - 6, top - 3, cx + 6, top + 9], fill=gold)
    for sx in (cx - 88, cx + 88):
        draw.line([(sx, top + 4), (sx - 24, top + 24)], fill=gold, width=2)
        draw.line([(sx, top + 4), (sx + 24, top + 24)], fill=gold, width=2)
        draw.chord([sx - 28, top + 18, sx + 28, top + 40], 0, 180, fill=gold)
    draw.rectangle([cx - 24, y1 - 8, cx + 24, y1 - 2], fill=gold)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def scene_cyclone(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (30, 70, 110), (120, 170, 200))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    for r in (30, 21, 12):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(245, 250, 255), width=5)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(245, 250, 255))
    for i in range(6):
        rx = x0 + 18 + i * 48
        draw.line([(rx, y1 - 26), (rx - 8, y1 - 8)], fill=(200, 225, 245), width=3)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def scene_kyiv(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (14, 20, 52), (60, 60, 110))
    base = y1
    for dx, hgt, wid in [(10, 40, 36), (52, 58, 30), (88, 34, 38), (200, 48, 32),
                         (238, 62, 30), (272, 40, 36)]:
        draw.rectangle([x0 + dx, base - hgt, x0 + dx + wid, base], fill=(8, 10, 26))
    # bridge
    draw.line([(x0 + 120, base - 22), (x0 + 210, base - 22)], fill=(200, 210, 230), width=3)
    draw.line([(x0 + 150, base - 52), (x0 + 150, base - 22)], fill=(200, 210, 230), width=3)
    draw.line([(x0 + 120, base - 22), (x0 + 150, base - 52)], fill=(200, 210, 230), width=2)
    draw.line([(x0 + 210, base - 22), (x0 + 150, base - 52)], fill=(200, 210, 230), width=2)
    # missile arcs + burst
    draw.arc([x0 + 170, y0 - 30, x0 + 300, y0 + 70], 200, 320, fill=(250, 160, 70), width=3)
    bx, by = x0 + 196, y0 + 44
    for ang in range(0, 360, 45):
        ex = bx + int(16 * math.cos(math.radians(ang)))
        ey = by + int(16 * math.sin(math.radians(ang)))
        draw.line([(bx, by), (ex, ey)], fill=(252, 190, 90), width=3)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def scene_ship(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (170, 205, 225), (240, 235, 210))
    sea = y1 - 10
    draw.rectangle([x0, sea, x1, y1], fill=(40, 90, 150))
    hull_y = sea - 8
    draw.polygon([(x0 + 40, hull_y), (x1 - 40, hull_y), (x1 - 66, sea + 2), (x0 + 66, sea + 2)],
                 fill=(30, 40, 60))
    cols = [(200, 60, 50), (50, 130, 80), (60, 90, 180), (230, 160, 50), (140, 80, 160)]
    for i in range(5):
        bx = x0 + 62 + i * 44
        draw.rectangle([bx, hull_y - 11, bx + 40, hull_y], fill=cols[i])
        draw.rectangle([bx, hull_y - 22, bx + 40, hull_y - 11], fill=cols[(i + 2) % 5])
    draw.rectangle([x1 - 92, hull_y - 24, x1 - 58, hull_y], fill=(245, 245, 245))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- content

FIGURES = [
    ("$2.36bn", "GTA VI sales so far (est.)"),
    ("24.6M", "copies sold by Thursday eve"),
    ("$97.17", "Anthropic (ANT) first close"),
    ("300,000", "evacuated ahead of Akvan"),
]

CARDS = [
    ("VICE CITY, EVERYWHERE", "GTA VI smashes every launch record",
     "Sensor Tower: 24.6M copies, ~$2.36bn by Thursday evening — nearly 3x GTA V's 2013 debut.",
     scene_gta),
    ("NASDAQ, NEW YORK", "Anthropic's $2 trillion debut",
     "ANT closes at $97.17, up 17% on the $83 IPO price. The $81.3bn raise is the biggest IPO ever.",
     scene_ipo),
    ("THE HAGUE", "UN court: Myanmar committed genocide",
     "First time the ICJ holds a state responsible: 9-6 on the 2017 Rohingya campaign.",
     scene_scales),
    ("ODISHA, INDIA", "Cyclone Akvan makes landfall today",
     "Crosses near Gopalpur by noon, 90-100 km/h. Over 300,000 evacuated; 69 trains cancelled.",
     scene_cyclone),
    ("KYIV", "Missiles hit three Kyiv bridges",
     "Ballistic barrage overnight kills five; fire in Obolonskyi. Putin invites EU leaders to Moscow.",
     scene_kyiv),
    ("SEOUL", "Korea's exports pass $1 trillion",
     "South Korea's annual exports top $1 trillion for the first time.",
     scene_ship),
]

BRIEFS = [
    "Iran widens Gulf attacks; tanker burns off Hormuz.",
    "Taiwan unveils five measures as stocks slide 5,248 points.",
    "'Fossil fuels' vanish from COP31 draft text.",
    "Israel completes Yellow Line operation in Gaza.",
    "Houthi missile damages Saudi PIF tower in Riyadh.",
    "UK and EU hold rare summit; youth scheme for 100,000.",
    "Takaichi dodges \"Taiwan contingency\" question at APEC.",
    "Trump posthumously pardons baseball legend Pete Rose.",
    "Genoa airport shut 4 hours after unidentified drones.",
    "Fire in 18-storey French block; one dead, 15 injured.",
    "Migrant boat sinks off Senegal; dozens missing.",
    "France, Germany, UK discuss possible meeting with Russia.",
    "California targets Nvidia in China AI-chip probe.",
    "IEA: data-centre power use could double by 2030.",
    "India-Israel deal to upgrade Barak missiles.",
    "Cricket: Nicholls 113* as NZ reach 243/5 v India.",
    "Modi opens FICCI centenary convention in New Delhi.",
    "Oil flat as Hormuz disruption offsets oversupply fears.",
    "APEC adopts declaration; Xi pledges $20m; Vietnam hosts 2027.",
    "Putin: no talks after Kerch bridge attacks; promises response.",
    "Trump warns APEC: strict AI rules would stifle development.",
    "BBC in besieged Taiz: \"I tell my son it's just fireworks.\"",
    "Nasdaq fell 2.3%; Alphabet -3.9%, Amazon -3.9%.",
    "White House fires national cyber director after outages.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x = MARGIN

    # masthead
    eyebrow = font(SANS_B, 13)
    d.text((x, 14), "THE DAY IN ONE PICTURE · 31 STORIES · ONE PAGE", font=eyebrow, fill=RED)
    mast = font(SERIF_B, 54)
    d.text((x, 30), "THE WORLD IN ONE DAY", font=mast, fill=INK)
    dateline = font(SANS_B, 16)
    d.text((x, 92), "FRIDAY, 20 NOVEMBER 2026", font=dateline, fill=NAVY)
    d.line([(x, 116), (x + CW, 116)], fill=RULE, width=3)

    summary = font(SERIF, 17)
    d.text((x, 126),
           "Three rivals sign for peace in Shenzhen, GTA VI breaks every record, Anthropic lands a $2 trillion debut.",
           font=summary, fill=INK)

    # figures strip
    fy = 156
    d.line([(x, fy), (x + CW, fy)], fill=RULE, width=1)
    colw = CW // 4
    num_f = font(SERIF_B, 30)
    lab_f = font(SANS, 11)
    for i, (num, lab) in enumerate(FIGURES):
        cx0 = x + i * colw
        d.text((cx0 + 8, fy + 6), num, font=num_f, fill=RED if i % 2 == 0 else NAVY)
        d.text((cx0 + 8, fy + 42), lab, font=lab_f, fill=GREY)
        if i:
            d.line([(cx0, fy + 4), (cx0, fy + 58)], fill=RULE, width=1)
    d.line([(x, fy + 64), (x + CW, fy + 64)], fill=RULE, width=1)

    # hero
    hy = fy + 76
    scene_shenzhen(d, (x, hy, x + CW, hy + 140))
    badge = font(SANS_B, 15)
    d.ellipse([x + 8, hy + 8, x + 36, hy + 36], fill=RED)
    d.text((x + 17, hy + 13), "1", font=badge, fill=(255, 255, 255))
    kick = font(SANS_B, 12)
    d.text((x, hy + 148), "SHENZHEN, CHINA", font=kick, fill=RED)
    hero_h = font(SERIF_B, 30)
    d.text((x, hy + 164), "Three rivals sign a 'peace declaration'", font=hero_h, fill=INK)
    hero_s = font(SANS, 14)
    hero_lines = wrap(d, "Trump, Xi and Putin end the first three-way summit: \"a nuclear war cannot be won and must never be fought\" — no word on Ukraine or Iran. Trump: \"bigger than Yalta\".",
                      hero_s, CW)
    y = draw_lines(d, x, hy + 204, hero_lines[:2], hero_s, INK, 17)

    # feature cards, 2 rows x 3
    card_w = (CW - 24) // 3
    card_h = 152
    scene_h = 48
    kick_f = font(SANS_B, 10)
    head_f = font(SERIF_B, 18)
    sum_f = font(SANS, 12)
    cy = y + 18
    for row in range(2):
        for col in range(3):
            idx = row * 3 + col
            kicker, head, summ, scene = CARDS[idx]
            cx0 = x + col * (card_w + 12)
            scene(d, (cx0, cy, cx0 + card_w, cy + scene_h))
            n = idx + 2
            d.ellipse([cx0 + 6, cy + 6, cx0 + 30, cy + 30], fill=RED)
            d.text((cx0 + 12 if n < 10 else cx0 + 9, cy + 10), str(n), font=font(SANS_B, 13),
                   fill=(255, 255, 255))
            ty = cy + scene_h + 6
            d.text((cx0, ty), kicker, font=kick_f, fill=RED)
            ty += 14
            ty = draw_lines(d, cx0, ty, wrap(d, head, head_f, card_w)[:2], head_f, INK, 20)
            draw_lines(d, cx0, ty, wrap(d, summ, sum_f, card_w)[:3], sum_f, INK, 14)
        cy += card_h + 8

    # briefs
    by = cy + 2
    d.text((x, by), "ALSO ON THE DAY", font=font(SANS_B, 15), fill=RED)
    by += 22
    brief_f = font(SANS, 12)
    num_f2 = font(SANS_B, 12)
    colw2 = (CW - 24) // 2
    rows = (len(BRIEFS) + 1) // 2
    line_h = 13
    for i, brief in enumerate(BRIEFS):
        col = 0 if i < rows else 1
        r = i if col == 0 else i - rows
        bx = x + col * (colw2 + 24)
        yy = by + r * line_h
        d.text((bx, yy), f"{i + 8}.", font=num_f2, fill=RED)
        d.text((bx + 26, yy), brief, font=brief_f, fill=INK)

    footer_y = by + rows * line_h + 8
    d.line([(x, footer_y), (x + CW, footer_y)], fill=RULE, width=1)
    foot = font(SANS, 10)
    d.text((x, footer_y + 4),
           "Every story above was reported on 19-20 November 2026. Older items (EU loan, 18 Nov; Australia sanctions, 17 Nov) are left out.",
           font=foot, fill=GREY)
    d.text((x, footer_y + 17),
           "Sources: Reuters · AP · BBC · The Guardian · IMD · Nasdaq. Sensor Tower estimates are third-party; Take-Two has published no official figure.",
           font=foot, fill=GREY)

    img.save("entry.png", "PNG", optimize=True)


if __name__ == "__main__":
    main()
