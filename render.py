"""Render the news-image-20261120 v2 front page into entry.png.

"THE WORLD IN ONE DAY — FRIDAY, 20 NOVEMBER 2026": a dense broadsheet
poster, 1024x1024, drawn entirely with PIL primitives (no photos, no
network). 45 stories: 3 heroes, 10 illustrated cards, 32 briefs, plus a
region bar, a figures strip, a world-map panel with numbered pins, a
DATE CHECK box and a sources footer. Stories are drawn from news first
reported 19-20 Nov 2026 and cross-checked across two or more sources
(Reuters, AP, BBC, The Guardian, IMD, Nasdaq, Sensor Tower estimates).

Deterministic: fixed layout, no randomness; re-running reproduces the
identical PNG bytes.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (28, 28, 30)
NAVY = (27, 42, 74)
NAVY_DEEP = (18, 30, 56)
RED = (178, 34, 34)
RED_BRIGHT = (205, 48, 48)
GOLD = (201, 150, 39)
GREY = (96, 96, 100)
LIGHT_LINE = (205, 198, 184)
SKY_TOP = (44, 62, 110)
SKY_BOT = (222, 158, 96)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_MASTHEAD = font(SERIF_B, 56)
F_DATELINE = font(SANS_B, 15)
F_REGION = font(SANS_B, 13)
F_FIG_NUM = font(SERIF_B, 27)
F_FIG_CAP = font(SANS, 10)
F_KICKER = font(SANS_B, 10)
F_HERO_HEAD = font(SERIF_B, 21)
F_HERO_BODY = font(SANS, 11)
F_CARD_HEAD = font(SERIF_B, 13)
F_CARD_BODY = font(SANS, 9.5)
F_SECTION = font(SERIF_B, 17)
F_BRIEF = font(SANS, 10.5)
F_BRIEF_NUM = font(SANS_B, 10.5)
F_FOOT = font(SANS, 9.5)
F_MAP_TITLE = font(SANS_B, 13)
F_PIN = font(SANS_B, 9)
F_BADGE = font(SANS_B, 11)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def badge(draw, cx, cy, num, r=11):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED_BRIGHT,
                 outline=(255, 255, 255), width=2)
    t = str(num)
    tw = draw.textlength(t, font=F_BADGE)
    draw.text((cx - tw / 2, cy - 8), t, font=F_BADGE, fill=(255, 255, 255))


def vgrad(img, box, top, bot):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


# ---------------------------------------------------------------- scenes

def scene_flags(d, box):
    """Three flags (US, China, Russia) over a skyline — Shenzhen summit."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # skyline
    heights = [0.42, 0.62, 0.5, 0.78, 0.55, 0.7, 0.46, 0.6, 0.52]
    bw = w / len(heights)
    for i, hf in enumerate(heights):
        bx = x0 + i * bw
        d.rectangle([bx + 2, y1 - h * hf, bx + bw - 2, y1], fill=(58, 74, 112))
    # flag poles + flags
    flags = [
        ((178, 34, 34), (255, 255, 255), (27, 42, 74)),   # US-ish
        ((205, 48, 48), (240, 200, 40), (205, 48, 48)),   # China
        ((255, 255, 255), (50, 90, 180), (205, 48, 48)),  # Russia
    ]
    for i, (c1, c2, c3) in enumerate(flags):
        px = x0 + w * (0.22 + 0.28 * i)
        top = y0 + 6
        d.line([(px, top), (px, y1 - 4)], fill=(230, 230, 230), width=2)
        fw, fh = 34, 21
        d.rectangle([px, top, px + fw, top + fh], fill=c1)
        if i == 0:
            for s in range(3):
                d.rectangle([px, top + s * 7, px + fw, top + s * 7 + 3],
                            fill=(255, 255, 255))
            d.rectangle([px, top, px + 14, top + 11], fill=c3)
        elif i == 1:
            d.ellipse([px + 3, top + 3, px + 10, top + 10], fill=c2)
        else:
            d.rectangle([px, top + 7, px + fw, top + 14], fill=c2)
            d.rectangle([px, top + 14, px + fw, top + fh], fill=c3)


def scene_gta(d, box):
    """Sunset palms and a giant VI — GTA VI launch."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # sun
    sx, sy, sr = x0 + w * 0.30, y0 + h * 0.52, h * 0.30
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(246, 196, 92))
    # palms
    for px, ph in ((x0 + w * 0.12, 0.95), (x0 + w * 0.52, 0.8)):
        base = y1
        top_y = y1 - h * ph
        d.line([(px, base), (px + 6, top_y)], fill=(20, 24, 40), width=4)
        for ang in (-2.6, -2.0, -1.4, -0.8, -0.3):
            ex = px + 6 + math.cos(ang) * 26
            ey = top_y + math.sin(ang) * 14 + 8
            d.line([(px + 6, top_y), (ex, ey)], fill=(20, 24, 40), width=3)
    # ground line
    d.rectangle([x0, y1 - 6, x1, y1], fill=(20, 24, 40))
    # VI
    f = font(SERIF_B, 64)
    d.text((x1 - 96, y0 + 14), "VI", font=f, fill=(255, 255, 255))


def scene_chart(d, box, label="$97.17"):
    """Rising bars with an arrow — Anthropic IPO."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    bars = [0.25, 0.38, 0.5, 0.66, 0.95]
    bw = w / (len(bars) + 1)
    for i, bf in enumerate(bars):
        bx = x0 + bw * (i + 0.4)
        col = (232, 126, 44) if i == len(bars) - 1 else (86, 132, 205)
        d.rectangle([bx, y1 - 8 - h * bf * 0.78, bx + bw * 0.62, y1 - 8],
                    fill=col)
    d.line([(x0 + 8, y1 - 8), (x1 - 8, y1 - 8)], fill=(200, 210, 230), width=2)
    ax0, ay0 = x0 + bw * 0.6, y1 - 8 - h * 0.28
    ax1, ay1 = x0 + bw * 4.9, y1 - 8 - h * 0.82
    d.line([(ax0, ay0), (ax1, ay1)], fill=(120, 220, 150), width=3)
    d.polygon([(ax1, ay1), (ax1 - 12, ay1 + 2), (ax1 - 3, ay1 + 10)],
              fill=(120, 220, 150))
    f = font(SANS_B, 20)
    d.text((x0 + 36, y0 + 8), label, font=f, fill=(255, 255, 255))


def scene_scales(d, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    top = y0 + 5
    d.line([(cx, top), (cx, y1 - 6)], fill=GOLD, width=3)
    d.line([(cx - 26, top + 6), (cx + 26, top + 6)], fill=GOLD, width=3)
    for sgn in (-1, 1):
        px = cx + sgn * 26
        d.line([(px, top + 6), (px - 9, top + 22)], fill=GOLD, width=2)
        d.line([(px, top + 6), (px + 9, top + 22)], fill=GOLD, width=2)
        d.arc([px - 11, top + 16, px + 11, top + 30], 0, 180, fill=GOLD,
              width=3)
    d.rectangle([cx - 14, y1 - 7, cx + 14, y1 - 3], fill=GOLD)


def scene_cyclone(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for r, a0 in ((20, 20), (14, 140), (8, 260)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 300,
              fill=(120, 190, 235), width=4)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))


def scene_bridge(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    deck = y1 - 10
    d.line([(x0 + 4, deck), (x1 - 4, deck)], fill=(200, 205, 215), width=4)
    for fx in (0.25, 0.55, 0.85):
        px = x0 + w * fx
        d.line([(px, deck), (px, y0 + 6)], fill=(200, 205, 215), width=3)
        d.line([(px, y0 + 8), (px - w * 0.18, deck)], fill=(140, 150, 170),
               width=1)
        d.line([(px, y0 + 8), (px + w * 0.18, deck)], fill=(140, 150, 170),
               width=1)
    # blast star
    bx, by = x0 + w * 0.55, y0 + 10
    for ang in range(0, 360, 45):
        ex = bx + math.cos(math.radians(ang)) * 9
        ey = by + math.sin(math.radians(ang)) * 9
        d.line([(bx, by), (ex, ey)], fill=(245, 170, 60), width=2)


def scene_tanker(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    hull_y = y1 - 12
    d.polygon([(x0 + 6, hull_y), (x1 - 14, hull_y), (x1 - 22, y1 - 4),
               (x0 + 14, y1 - 4)], fill=(40, 44, 54))
    d.rectangle([x0 + 12, hull_y - 8, x1 - 30, hull_y], fill=(120, 60, 40))
    d.rectangle([x1 - 30, hull_y - 16, x1 - 20, hull_y], fill=(220, 220, 220))
    # flame
    fx = x0 + w * 0.45
    d.polygon([(fx - 7, hull_y - 8), (fx, hull_y - 26), (fx + 7, hull_y - 8)],
              fill=(240, 120, 40))
    d.polygon([(fx - 4, hull_y - 8), (fx, hull_y - 18), (fx + 4, hull_y - 8)],
              fill=(250, 200, 80))
    # waves
    for i in range(4):
        wx = x0 + 8 + i * (w / 4)
        d.arc([wx, y1 - 8, wx + 22, y1 + 2], 180, 360, fill=(90, 150, 210),
              width=2)


def scene_downchart(d, box):
    x0, y0, x1, y1 = box
    pts = [(x0 + 6, y0 + 8), (x0 + 26, y0 + 16), (x0 + 44, y0 + 13),
           (x0 + 62, y0 + 26), (x1 - 8, y1 - 8)]
    d.line(pts, fill=(235, 90, 90), width=3)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 11, ey - 1), (ex - 2, ey - 9)],
              fill=(235, 90, 90))


def scene_ship(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    hull_y = y1 - 10
    d.polygon([(x0 + 4, hull_y), (x1 - 8, hull_y), (x1 - 16, y1 - 3),
               (x0 + 12, y1 - 3)], fill=(30, 60, 90))
    cols = [(205, 48, 48), (86, 132, 205), (60, 160, 90), (232, 160, 44)]
    for i, c in enumerate(cols):
        bx = x0 + 10 + i * 16
        d.rectangle([bx, hull_y - 10, bx + 14, hull_y], fill=c)
        if i % 2 == 0:
            d.rectangle([bx, hull_y - 19, bx + 14, hull_y - 10],
                        fill=cols[(i + 1) % 4])
    d.rectangle([x1 - 26, hull_y - 22, x1 - 16, hull_y], fill=(230, 230, 230))


def scene_leaf(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.polygon([(cx - 16, cy + 12), (cx - 4, cy - 14), (cx + 16, cy - 12),
               (cx + 6, cy + 10)], fill=(70, 170, 90))
    d.line([(cx - 14, cy + 12), (cx + 12, cy - 10)], fill=(30, 110, 55),
           width=2)
    d.line([(cx - 14, cy + 12), (cx - 18, cy + 18)], fill=(30, 110, 55),
           width=2)


def scene_yellowline(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    for i in range(5):
        bx = x0 + 8 + i * (w / 5)
        d.rectangle([bx, y1 - 16, bx + w / 5 - 4, y1 - 12], fill=(240, 200, 40))
    # flag
    px = x0 + w * 0.62
    d.line([(px, y0 + 6), (px, y1 - 14)], fill=(230, 230, 230), width=2)
    d.rectangle([px, y0 + 6, px + 20, y0 + 15], fill=(86, 132, 205))
    d.rectangle([px, y0 + 15, px + 20, y0 + 18], fill=(255, 255, 255))


def scene_tower(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tx = x0 + w * 0.55
    d.rectangle([tx, y0 + 4, tx + 16, y1 - 4], fill=(150, 165, 190))
    for wy in range(int(y0 + 9), int(y1 - 8), 7):
        d.rectangle([tx + 3, wy, tx + 6, wy + 3], fill=(240, 220, 140))
        d.rectangle([tx + 10, wy, tx + 13, wy + 3], fill=(240, 220, 140))
    # missile trail
    d.line([(x0 + 6, y1 - 6), (tx + 2, y0 + 12)], fill=(240, 180, 90), width=2)
    d.ellipse([tx - 3, y0 + 6, tx + 7, y0 + 16], fill=(245, 150, 60))


def scene_handshake(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # circle of stars (EU) + simple handshake glyph
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        sx = cx + math.cos(ang) * 17
        sy = cy + math.sin(ang) * 13
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(240, 200, 40))
    d.line([(cx - 10, cy + 2), (cx + 2, cy + 8), (cx + 11, cy - 1)],
           fill=(240, 240, 240), width=3)


# ---------------------------------------------------------------- map

CONTINENTS = [
    # (points as fractions of map box) rough continent silhouettes
    [(0.02, 0.26), (0.08, 0.08), (0.18, 0.04), (0.26, 0.10), (0.28, 0.24),
     (0.24, 0.38), (0.18, 0.48), (0.12, 0.44), (0.05, 0.38)],          # N America
    [(0.19, 0.52), (0.27, 0.50), (0.30, 0.62), (0.27, 0.86), (0.23, 0.94),
     (0.20, 0.68)],                                                    # S America
    [(0.43, 0.16), (0.50, 0.06), (0.57, 0.12), (0.56, 0.26), (0.49, 0.32),
     (0.43, 0.26)],                                                    # Europe
    [(0.44, 0.38), (0.56, 0.34), (0.61, 0.48), (0.57, 0.72), (0.50, 0.82),
     (0.45, 0.58)],                                                    # Africa
    [(0.58, 0.10), (0.72, 0.04), (0.88, 0.08), (0.94, 0.20), (0.88, 0.36),
     (0.79, 0.44), (0.70, 0.52), (0.63, 0.42), (0.58, 0.26)],          # Asia
    [(0.79, 0.60), (0.90, 0.58), (0.94, 0.72), (0.87, 0.84), (0.79, 0.74)],
    # Australia
]

# pin positions (story number -> (fx, fy) in map box), spread apart
PINS = {
    1: (0.838, 0.32),   # Shenzhen
    3: (0.238, 0.26),   # New York / Nasdaq
    4: (0.458, 0.18),   # The Hague
    5: (0.698, 0.44),   # Odisha, India
    6: (0.548, 0.14),   # Kyiv
    7: (0.628, 0.40),   # Hormuz
    8: (0.872, 0.46),   # Taipei
    9: (0.852, 0.22),   # Seoul
    11: (0.562, 0.38),  # Gaza
    12: (0.598, 0.46),  # Riyadh
    13: (0.490, 0.30),  # Brussels
    19: (0.448, 0.52),  # Senegal
    25: (0.928, 0.86),  # Wellington
}


def draw_map(img, box):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    d.rectangle(box, fill=NAVY_DEEP)
    d.text((x0 + 12, y0 + 8), "WHERE IT HAPPENED", font=F_MAP_TITLE,
           fill=(255, 255, 255))
    mx0, my0 = x0 + 10, y0 + 30
    mw, mh = (x1 - x0) - 20, (y1 - y0) - 38
    for poly in CONTINENTS:
        pts = [(mx0 + fx * mw, my0 + fy * mh) for fx, fy in poly]
        d.polygon(pts, fill=(74, 110, 160))
    for num, (fx, fy) in PINS.items():
        cx, cy = mx0 + fx * mw, my0 + fy * mh
        r = 8
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED_BRIGHT,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=F_PIN)
        d.text((cx - tw / 2, cy - 6), t, font=F_PIN, fill=(255, 255, 255))


# ---------------------------------------------------------------- content

FIGURES = [
    ("$2.36bn", "GTA VI sales so far (est.)"),
    ("24.6M", "copies sold by Thursday eve"),
    ("$97.17", "Anthropic (ANT) first close"),
    ("$81.3bn", "raised — biggest IPO ever"),
    ("300,000", "evacuated ahead of Akvan"),
    ("$1tn", "South Korea's annual exports"),
]

REGIONS = "ASIA-PACIFIC 15 · AMERICAS 12 · EUROPE 7 · MIDDLE EAST 4 · AFRICA 1 · WORLD 6"

HEROES = [
    dict(num=1, kicker="SHENZHEN, CHINA", scene="flags",
         head="Three rivals sign a 'peace declaration'",
         body="Trump, Xi and Putin end the first three-way summit: "
              "“a nuclear war cannot be won and must never be fought” "
              "— no word on Ukraine or Iran. Trump: “bigger than "
              "Yalta”."),
    dict(num=2, kicker="VICE CITY, EVERYWHERE", scene="gta",
         head="GTA VI smashes every launch record",
         body="Sensor Tower estimates 24.6M copies and about $2.36bn "
              "by Thursday evening (Reuters) — nearly 3x GTA V's 2013 "
              "debut. Analysts expect $3bn by year-end."),
    dict(num=3, kicker="NASDAQ, NEW YORK", scene="chart",
         head="Anthropic's $2 trillion debut",
         body="ANT closes at $97.17, up 17% on the $83 IPO price after "
              "opening at $111.50. The $81.3 billion raise is the "
              "biggest IPO ever; the firm was briefly valued near "
              "$2 trillion."),
]

CARDS = [
    dict(num=4, kicker="THE HAGUE", scene="scales",
         head="UN court: Myanmar committed genocide",
         body="First time the ICJ holds a state responsible: 9–6 on the "
              "2017 Rohingya campaign."),
    dict(num=5, kicker="ODISHA, INDIA", scene="cyclone",
         head="Cyclone Akvan makes landfall today",
         body="Crosses near Gopalpur by noon, 90–100 km/h. Over 300,000 "
              "evacuated; 69 trains cancelled."),
    dict(num=6, kicker="KYIV", scene="bridge",
         head="Missiles hit three Kyiv bridges",
         body="Ballistic barrage overnight kills five; fire in "
              "Obolonskyi. Putin invites EU leaders to Moscow."),
    dict(num=7, kicker="STRAIT OF HORMUZ", scene="tanker",
         head="Iran widens attacks; tanker burns",
         body="Tanker ablaze after mine strike off Hormuz; Houthis claim "
              "hits on Saudi targets."),
    dict(num=8, kicker="TAIPEI", scene="downchart",
         head="Taiwan acts to steady sliding stocks",
         body="Five measures unveiled; short-selling limits start today "
              "after a 5,248-point slide."),
    dict(num=9, kicker="SEOUL", scene="ship",
         head="Korea's exports pass $1 trillion",
         body="South Korea's annual exports top $1 trillion for the "
              "first time."),
    dict(num=10, kicker="COP31, TÜRKIYE", scene="leaf",
         head="'Fossil fuels' vanish from draft",
         body="The words are dropped from the latest COP31 text; AI "
              "pledge snubbed by US tech."),
    dict(num=11, kicker="GAZA", scene="yellowline",
         head="Israel completes Yellow Line operation",
         body="IDF ends operation beyond the Yellow Line; strike hits "
              "Hezbollah site in Lebanon."),
    dict(num=12, kicker="RIYADH", scene="tower",
         head="Houthi missile hits Riyadh tower",
         body="Missile damages the Saudi wealth-fund tower in the "
              "capital's financial district."),
    dict(num=13, kicker="BRUSSELS", scene="handshake",
         head="UK and EU hold rare summit",
         body="Burnham meets Costa and von der Leyen; youth scheme for "
              "100,000 each way on the table."),
]

BRIEFS = [
    (14, "Takaichi dodges “Taiwan contingency” question at APEC."),
    (15, "Trump posthumously pardons baseball legend Pete Rose."),
    (16, "Fiona the hippo dies after swallowing a hat in Cincinnati."),
    (17, "Genoa airport shut 4 hours after unidentified drones."),
    (18, "Fire in 18-storey French block; one dead, 15 injured."),
    (19, "Migrant boat sinks off Senegal; dozens missing."),
    (20, "France, Germany, UK discuss possible meeting with Russia."),
    (21, "California targets Nvidia in China AI-chip probe."),
    (22, "IEA: data-centre power use could double by 2030."),
    (23, "Fire at Yunus ancestral home in Bangladesh; arson suspected."),
    (24, "India–Israel ₹1,976 crore deal to upgrade Barak missiles."),
    (25, "Cricket: Nicholls 113* as NZ reach 243/5 v India, Wellington."),
    (26, "Modi opens FICCI centenary convention in New Delhi."),
    (27, "Oil flat as Hormuz disruption offsets oversupply fears."),
    (28, "TSMC, Samsung halt some chip shipments to China (US curbs)."),
    (29, "APEC adopts declaration; Xi pledges $20m; Vietnam hosts 2027."),
    (30, "Putin: no talks after Kerch bridge attacks; promises response."),
    (31, "Trump warns APEC: strict AI rules would stifle development."),
    (32, "BBC in besieged Taiz: “I tell my son it's just fireworks.”"),
    (33, "Anthropic offering closes today; indexes add ANT next month."),
    (34, "Shenzhen text: UN reform, fuel supplies, ICC limits."),
    (35, "Nasdaq fell 2.3%; Alphabet -3.9%, Amazon -3.9%."),
    (36, "US envoy: Russia not ruling out NATO-like Ukraine guarantees."),
    (37, "Thursday rally: Sensex +1.21%, Nifty +1.14%."),
    (38, "57th IFFI adds animation section, five films."),
    (39, "India beat Malaysia in Hong Kong Open badminton."),
    (40, "GTA VI Netflix trailer drove sixfold pre-order jump."),
    (41, "White House fires national cyber director after outages."),
    (42, "A week of outages hits banks, flights and Apple; no link found."),
    (43, "Bukele to formalise bid for third term in El Salvador."),
    (44, "Pakistani man jailed 27 years over Iran-backed plot to kill Trump."),
    (45, "Meta rethinks 2030 climate goals as AI data centres grow."),
]

SCENES = {
    "flags": scene_flags, "gta": scene_gta, "chart": scene_chart,
    "scales": scene_scales, "cyclone": scene_cyclone, "bridge": scene_bridge,
    "tanker": scene_tanker, "downchart": scene_downchart, "ship": scene_ship,
    "leaf": scene_leaf, "yellowline": scene_yellowline, "tower": scene_tower,
    "handshake": scene_handshake,
}

SCENE_BG = {
    "flags": (SKY_TOP, SKY_BOT), "gta": ((38, 30, 78), (214, 110, 92)),
    "chart": ((16, 26, 52), (16, 26, 52)),
    "scales": ((30, 44, 84), (30, 44, 84)),
    "cyclone": ((18, 40, 74), (18, 40, 74)),
    "bridge": ((24, 30, 48), (24, 30, 48)),
    "tanker": ((30, 70, 110), (30, 70, 110)),
    "downchart": ((250, 244, 232), (250, 244, 232)),
    "ship": ((96, 150, 200), (140, 190, 225)),
    "leaf": ((225, 242, 218), (225, 242, 218)),
    "yellowline": ((52, 58, 70), (52, 58, 70)),
    "tower": ((40, 52, 84), (40, 52, 84)),
    "handshake": ((24, 40, 90), (24, 40, 90)),
}


def render_scene(img, name, box):
    top, bot = SCENE_BG[name]
    if top == bot:
        ImageDraw.Draw(img).rectangle(box, fill=top)
    else:
        vgrad(img, box, top, bot)
    SCENES[name](ImageDraw.Draw(img), box)


# ---------------------------------------------------------------- layout

def hero_card(img, d, x, y, w, h, story):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    scene_h = int(h * 0.42)
    render_scene(img, story["scene"], (x + 2, y + 2, x + w - 2, y + scene_h))
    badge(d, x + 16, y + 16, story["num"])
    ty = y + scene_h + 8
    d.text((x + 10, ty), story["kicker"], font=F_KICKER, fill=RED)
    ty += 15
    for ln in wrap(d, story["head"], F_HERO_HEAD, w - 20):
        d.text((x + 10, ty), ln, font=F_HERO_HEAD, fill=INK)
        ty += 22
    ty += 2
    for ln in wrap(d, story["body"], F_HERO_BODY, w - 20):
        d.text((x + 10, ty), ln, font=F_HERO_BODY, fill=(52, 52, 56))
        ty += 13


def small_card(img, d, x, y, w, h, story):
    d.rectangle([x, y, x + w, y + h], outline=(120, 116, 108), width=1)
    scene_h = 40
    render_scene(img, story["scene"], (x + 1, y + 1, x + w - 1, y + scene_h))
    badge(d, x + 12, y + 12, story["num"], r=10)
    ty = y + scene_h + 4
    d.text((x + 7, ty), story["kicker"], font=font(SANS_B, 8.5), fill=RED)
    ty += 11
    for ln in wrap(d, story["head"], F_CARD_HEAD, w - 14):
        d.text((x + 7, ty), ln, font=F_CARD_HEAD, fill=INK)
        ty += 14
    ty += 1
    for ln in wrap(d, story["body"], F_CARD_BODY, w - 14):
        d.text((x + 7, ty), ln, font=F_CARD_BODY, fill=(60, 60, 64))
        ty += 11


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_MASTHEAD)
    d.text(((W - tw) / 2, y), title, font=F_MASTHEAD, fill=INK)
    y += 56
    dl = "FRIDAY, 20 NOVEMBER 2026 · ALL THE DAY'S NEWS ON ONE PAGE"
    tw = d.textlength(dl, font=F_DATELINE)
    d.text(((W - tw) / 2, y), dl, font=F_DATELINE, fill=(60, 60, 64))
    y += 20
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 4

    # Region bar
    d.rectangle([MARGIN, y, W - MARGIN, y + 22], fill=NAVY)
    tw = d.textlength(REGIONS, font=F_REGION)
    d.text(((W - tw) / 2, y + 4), REGIONS, font=F_REGION,
           fill=(255, 255, 255))
    y += 28

    # Figures strip
    fig_y = y
    fw = CONTENT_W / len(FIGURES)
    for i, (num, cap) in enumerate(FIGURES):
        fx = MARGIN + i * fw
        if i:
            d.line([(fx, fig_y + 4), (fx, fig_y + 46)], fill=LIGHT_LINE,
                   width=1)
        nw = d.textlength(num, font=F_FIG_NUM)
        d.text((fx + (fw - nw) / 2, fig_y), num, font=F_FIG_NUM,
               fill=RED if i % 2 == 0 else NAVY)
        cw = d.textlength(cap, font=F_FIG_CAP)
        d.text((fx + (fw - cw) / 2, fig_y + 30), cap, font=F_FIG_CAP,
               fill=GREY)
    y += 46
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=LIGHT_LINE, width=1)
    y += 7

    # Heroes
    gap = 10
    hw = (CONTENT_W - 2 * gap) / 3
    hh = 212
    for i, story in enumerate(HEROES):
        hero_card(img, d, MARGIN + i * (hw + gap), y, hw, hh, story)
    y += hh + 8

    # Small cards: 5 x 2
    cw2 = (CONTENT_W - 4 * gap) / 5
    ch2 = 120
    for i, story in enumerate(CARDS):
        cx = MARGIN + (i % 5) * (cw2 + gap)
        cy = y + (i // 5) * (ch2 + gap)
        small_card(img, d, cx, cy, cw2, ch2, story)
    y += 2 * ch2 + gap + 8

    # Map
    map_h = 86
    draw_map(img, (MARGIN, y, W - MARGIN, y + map_h))
    y += map_h + 8

    # Briefs
    d.text((MARGIN, y), "ALSO ON THE DAY", font=F_SECTION, fill=RED)
    y += 20
    cols = 3
    col_w = (CONTENT_W - (cols - 1) * 14) / cols
    per_col = math.ceil(len(BRIEFS) / cols)
    brief_top = y
    max_y = brief_top
    for c in range(cols):
        cy = brief_top
        for num, text in BRIEFS[c * per_col:(c + 1) * per_col]:
            label = f"{num}."
            d.text((MARGIN + c * (col_w + 14), cy), label,
                   font=F_BRIEF_NUM, fill=RED)
            lines = wrap(d, text, F_BRIEF, col_w - 26)
            for ln in lines:
                d.text((MARGIN + c * (col_w + 14) + 26, cy), ln,
                       font=F_BRIEF, fill=(40, 40, 44))
                cy += 12
            cy += 2
        max_y = max(max_y, cy)
    y = max_y + 5

    # Footer
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=LIGHT_LINE, width=1)
    y += 5
    foot1 = ("DATE CHECK: every story above was reported on 19–20 November "
             "2026. Older items (EU €45bn Ukraine loan, 18 Nov; Australia "
             "sanctions, 17 Nov) are left out.")
    foot2 = ("Sources: Reuters · AP · BBC · The Guardian · IMD · Nasdaq · "
             "Sensor Tower estimates · ICJ. GTA VI sales are third-party "
             "estimates; Take-Two has published no official figure.")
    for ln in wrap(d, foot1, F_FOOT, CONTENT_W):
        d.text((MARGIN, y), ln, font=F_FOOT, fill=GREY)
        y += 11
    for ln in wrap(d, foot2, F_FOOT, CONTENT_W):
        d.text((MARGIN, y), ln, font=F_FOOT, fill=GREY)
        y += 11

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}: {os.path.getsize(out)} bytes, bottom y={y}")


if __name__ == "__main__":
    main()
