"""Render entry.png: "The World in One Day — Friday, 20 November 2026".

A dense broadsheet front page (1024x1024) drawn with PIL from world news
reported on 19-20 November 2026 (Reuters, AP, BBC, Guardian, IMD, Nasdaq).
Run once at build time; main.py just copies the resulting entry.png.
Deterministic: same code, same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 22                      # page margin
CW = W - 2 * M              # content width (980)
PAPER = (247, 243, 231)
CARD = (255, 253, 247)
INK = (26, 26, 26)
NAVY = (20, 38, 76)
RED = (176, 42, 30)
GOLD = (168, 128, 26)
TEAL = (16, 104, 104)
GRAY = (96, 92, 84)
MAPLAND = (120, 158, 205)

FD = "/usr/share/fonts/truetype/noto/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SERIF = "NotoSerif-Regular.ttf"
SERIF_IT = "NotoSerif-Italic.ttf"
SANS_B = "NotoSans-Bold.ttf"
SANS = "NotoSans-Regular.ttf"
COND_B = "NotoSans-CondensedBold.ttf"
COND = "NotoSans-Condensed.ttf"


def wrap(d, text, font, maxw):
    """Greedy word wrap; returns list of lines fitting maxw pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def badge(d, cx, cy, r, num):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=PAPER, width=2)
    f = F(SANS_B, 13 if num < 10 else 11)
    d.text((cx, cy - 1), str(num), font=f, fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- stories
# Every fact below was reported 19-20 Nov 2026 and cross-checked in at
# least two sources (Reuters/AP/BBC/Guardian/IMD/Nasdaq/Sensor Tower).
# region is only used for the region-count bar.

HEROES = [
    dict(num=1, region="ASIA-PACIFIC", scene="summit", place="SHENZHEN, CHINA",
         head="Three rivals sign a \u2018peace declaration\u2019",
         body="Trump, Xi and Putin end the first-ever US\u2013China\u2013Russia summit: "
              "\u201ca nuclear war cannot be won and must never be fought\u201d \u2014 but no word on "
              "the Ukraine or Iran wars. Trump calls it \u201cbigger than Yalta\u201d."),
    dict(num=2, region="AMERICAS", scene="gta", place="VICE CITY, EVERYWHERE",
         head="GTA VI smashes every launch record",
         body="Sensor Tower estimates 24.6 million copies and about $2.36 billion by "
              "Thursday evening (Reuters) \u2014 nearly three times GTA V\u2019s record 2013 "
              "debut. Analysts expect $3 billion by year-end."),
    dict(num=3, region="AMERICAS", scene="anthropic", place="NASDAQ, NEW YORK",
         head="Anthropic\u2019s $2 trillion debut",
         body="ANT closes at $97.17, up 17% on the $83 IPO price after opening at "
              "$111.50. The $81.3 billion raise is the biggest IPO ever; the firm was "
              "briefly valued near $2 trillion."),
]

CARDS = [
    dict(num=4, region="ASIA-PACIFIC", scene="icj", place="THE HAGUE",
         head="UN court: Myanmar committed genocide",
         body="First time the ICJ holds a state responsible: 9\u20136 on the 2017 Rohingya campaign."),
    dict(num=5, region="ASIA-PACIFIC", scene="cyclone", place="ODISHA, INDIA",
         head="Cyclone Akvan makes landfall today",
         body="Crosses near Gopalpur by noon, 90\u2013100 km/h. Over 300,000 evacuated; 69 trains cancelled."),
    dict(num=6, region="EUROPE", scene="kyiv", place="KYIV",
         head="Missiles hit Kyiv as peace talk grows",
         body="Ballistic missiles overnight; fire in Obolonskyi. Putin invites EU leaders to Moscow."),
    dict(num=7, region="MIDDLE EAST", scene="tanker", place="STRAIT OF HORMUZ",
         head="Iran widens attacks; tanker burns",
         body="Tanker ablaze after mine strike off Hormuz; Houthis claim hits on Saudi targets."),
    dict(num=8, region="ASIA-PACIFIC", scene="taiwan", place="TAIPEI",
         head="Taiwan acts to steady sliding stocks",
         body="Five measures unveiled; short-selling limits start today after a 5,248-point slide."),
    dict(num=9, region="ASIA-PACIFIC", scene="korea", place="SEOUL",
         head="Korea\u2019s exports pass $1 trillion",
         body="South Korea\u2019s annual exports top $1 trillion for the first time."),
    dict(num=10, region="WORLD", scene="cop", place="COP31, T\u00dcRKIYE",
         head="\u2018Fossil fuels\u2019 vanish from draft",
         body="The words are dropped from the latest COP31 text; AI pledge snubbed by US tech."),
    dict(num=11, region="MIDDLE EAST", scene="gaza", place="GAZA",
         head="Israel completes Yellow Line operation",
         body="IDF ends operation beyond the Yellow Line; strike hits Hezbollah site in Lebanon."),
]

BRIEFS = [
    (12, "ASIA-PACIFIC", "Takaichi dodges \u2018Taiwan contingency\u2019 question at APEC."),
    (13, "AMERICAS", "Trump posthumously pardons baseball legend Pete Rose."),
    (14, "AMERICAS", "Fiona the hippo dies after swallowing a hat in Cincinnati."),
    (15, "EUROPE", "Genoa airport shut 4 hours after unidentified drones."),
    (16, "EUROPE", "Fire in 18-storey French block: one dead, 15 injured."),
    (17, "AFRICA", "Migrant boat sinks off Senegal; dozens missing."),
    (18, "EUROPE", "France, Germany, UK discuss possible meeting with Russia."),
    (19, "AMERICAS", "California targets Nvidia in China AI-chip probe."),
    (20, "WORLD", "IEA: data-centre power use could double by 2030."),
    (21, "ASIA-PACIFIC", "Fire at Yunus ancestral home in Bangladesh; arson suspected."),
    (22, "ASIA-PACIFIC", "India\u2013Israel \u20b91,976 crore deal to upgrade Barak missiles."),
    (23, "ASIA-PACIFIC", "Cricket: Nicholls 113* as NZ reach 243/5 v India, Wellington."),
    (24, "ASIA-PACIFIC", "Modi opens FICCI centenary convention in New Delhi."),
    (25, "WORLD", "Oil flat as Hormuz disruption offsets oversupply fears."),
    (26, "ASIA-PACIFIC", "TSMC, Samsung halt some chip shipments to China (US curbs)."),
    (27, "ASIA-PACIFIC", "APEC adopts declaration; Xi pledges $20m; Vietnam hosts 2027."),
    (28, "EUROPE", "Putin: no talks after Kerch bridge attacks; promises response."),
    (29, "AMERICAS", "Trump warns APEC: strict AI rules would stifle development."),
    (30, "MIDDLE EAST", "BBC in besieged Taiz: \u201cI tell my son it\u2019s just fireworks.\u201d"),
    (31, "AMERICAS", "Anthropic offering closes today; indexes add ANT next month."),
    (32, "WORLD", "Shenzhen text: UN reform, fuel supplies, ICC limits."),
    (33, "AMERICAS", "Nasdaq fell 2.3%; Alphabet \u22123%, Amazon \u22123.9%."),
    (34, "EUROPE", "US envoy: Russia not ruling out NATO-like Ukraine guarantees."),
    (35, "ASIA-PACIFIC", "Thursday rally: Sensex +1.21%, Nifty +1.14%."),
    (36, "ASIA-PACIFIC", "57th IFFI adds animation section, five films."),
    (37, "ASIA-PACIFIC", "India beat Malaysia in Hong Kong Open badminton."),
    (38, "AMERICAS", "GTA VI Netflix trailer drove sixfold pre-order jump."),
]

FIGURES = [
    ("$2.36bn", "GTA VI day-one sales (est.)"),
    ("24.6M", "copies sold by Thursday eve"),
    ("$97.17", "Anthropic (ANT) first close"),
    ("$81.3bn", "raised \u2014 biggest IPO ever"),
    ("300,000", "evacuated ahead of Akvan"),
    ("$1tn", "South Korea\u2019s annual exports"),
]

# story number -> (x fraction, y fraction) on the stylised world map
PINS = {
    1: (0.790, 0.44), 2: (0.200, 0.46), 3: (0.250, 0.34), 4: (0.452, 0.20),
    5: (0.700, 0.48), 6: (0.548, 0.20), 7: (0.628, 0.46), 8: (0.805, 0.40),
    9: (0.820, 0.31), 10: (0.562, 0.34), 11: (0.578, 0.44), 15: (0.478, 0.32),
    17: (0.420, 0.54), 23: (0.940, 0.84),
}


# ----------------------------------------------------------------- scenes
# Small flat illustrations drawn with PIL primitives. Each takes the draw
# object and a box (x0, y0, x1, y1) and paints inside it.

def _sky(d, b, top, bottom):
    x0, y0, x1, y1 = b
    steps = 24
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.rectangle([x0, y0 + (y1 - y0) * i / steps, x1, y0 + (y1 - y0) * (i + 1) / steps + 1], fill=c)


def scene_summit(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (196, 214, 235), (240, 232, 205))
    # skyline
    base = y0 + h * 0.72
    for i, (fx, fh) in enumerate([(0.02, .34), (.12, .48), (.24, .30), (.66, .44), (.78, .32), (.88, .50)]):
        bx = x0 + w * fx
        d.rectangle([bx, base - h * fh, bx + w * 0.09, base], fill=(70, 88, 120))
    d.rectangle([x0, base, x1, y1], fill=(120, 130, 140))
    # three flags on poles
    flags = [((178, 34, 52), "us"), ((200, 30, 30), "cn"), ((240, 240, 240), "ru")]
    for i, (col, kind) in enumerate(flags):
        px = x0 + w * (0.34 + 0.16 * i)
        d.line([px, base, px, y0 + h * 0.16], fill=(40, 40, 40), width=3)
        fw, fh = w * 0.13, h * 0.20
        fy = y0 + h * 0.16
        if kind == "us":
            for s in range(5):
                d.rectangle([px, fy + fh * s / 5, px + fw, fy + fh * (s + 1) / 5],
                            fill=(178, 34, 52) if s % 2 == 0 else (245, 245, 245))
            d.rectangle([px, fy, px + fw * 0.45, fy + fh * 0.55], fill=(40, 50, 130))
        elif kind == "cn":
            d.rectangle([px, fy, px + fw, fy + fh], fill=col)
            cx, cy = px + fw * 0.28, fy + fh * 0.30
            d.regular_polygon((cx, cy, fh * 0.16), 5, fill=(250, 210, 60))
        else:
            d.rectangle([px, fy, px + fw, fy + fh / 3], fill=(245, 245, 245))
            d.rectangle([px, fy + fh / 3, px + fw, fy + 2 * fh / 3], fill=(40, 70, 170))
            d.rectangle([px, fy + 2 * fh / 3, px + fw, fy + fh], fill=(200, 40, 40))
    # conference table
    d.rectangle([x0 + w * 0.30, y0 + h * 0.60, x0 + w * 0.70, y0 + h * 0.70], fill=(90, 60, 35))
    d.rectangle([x0 + w * 0.30, y0 + h * 0.70, x0 + w * 0.70, y0 + h * 0.74], fill=(70, 45, 25))


def scene_gta(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (38, 22, 74), (222, 84, 110))
    d.ellipse([x0 + w * 0.62, y0 + h * 0.08, x0 + w * 0.86, y0 + h * 0.08 + w * 0.24], fill=(255, 196, 86))
    base = y0 + h * 0.78
    for fx, fh in [(0.03, .40), (.13, .55), (.25, .34), (.36, .48), (.78, .42), (.88, .56)]:
        bx = x0 + w * fx
        d.rectangle([bx, base - h * fh, bx + w * 0.09, base], fill=(24, 16, 44))
        for wy in range(3):
            for wx in range(2):
                d.rectangle([bx + 3 + wx * w * 0.035, base - h * fh + 4 + wy * h * 0.11,
                             bx + 6 + wx * w * 0.035, base - h * fh + 8 + wy * h * 0.11], fill=(255, 220, 130))
    d.rectangle([x0, base, x1, y1], fill=(16, 10, 30))
    # palm tree
    px = x0 + w * 0.55
    d.line([px, base, px + w * 0.03, y0 + h * 0.30], fill=(12, 8, 24), width=5)
    for ang in (-2.6, -1.9, -1.2, -0.5, 0.1):
        import math
        ex = px + w * 0.03 + math.cos(ang) * w * 0.11
        ey = y0 + h * 0.30 + math.sin(ang) * h * 0.10 + h * 0.05
        d.line([px + w * 0.03, y0 + h * 0.30, ex, ey], fill=(12, 8, 24), width=4)
    # car silhouette
    cx0, cy0 = x0 + w * 0.08, y0 + h * 0.80
    d.polygon([(cx0, cy0 + h * 0.10), (cx0 + w * 0.06, cy0 + h * 0.02), (cx0 + w * 0.20, cy0),
               (cx0 + w * 0.30, cy0 + h * 0.03), (cx0 + w * 0.36, cy0 + h * 0.10)], fill=(10, 6, 20))
    for wx in (0.07, 0.28):
        d.ellipse([cx0 + w * wx, cy0 + h * 0.08, cx0 + w * wx + h * 0.09, cy0 + h * 0.08 + h * 0.09], fill=(200, 200, 210))
    f = F(SERIF_BLACK, int(h * 0.52))
    d.text((x0 + w * 0.97, y0 + h * 0.52), "VI", font=f, fill=(255, 240, 200), anchor="rm",
           stroke_width=2, stroke_fill=(20, 10, 40))


def scene_anthropic(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(16, 22, 48))
    base = y0 + h * 0.82
    heights = [0.22, 0.34, 0.48, 0.66, 0.88]
    for i, fh in enumerate(heights):
        bx = x0 + w * (0.10 + 0.155 * i)
        d.rectangle([bx, base - h * fh, bx + w * 0.11, base],
                    fill=(240, 150, 60) if i == 4 else (90, 140, 220))
    d.line([x0 + w * 0.06, base, x1 - w * 0.04, base], fill=(230, 230, 230), width=2)
    import math
    ax0, ay0 = x0 + w * 0.08, y0 + h * 0.62
    ax1, ay1 = x0 + w * 0.90, y0 + h * 0.10
    d.line([ax0, ay0, ax1, ay1], fill=(120, 230, 140), width=4)
    d.polygon([(ax1, ay1), (ax1 - w * 0.09, ay1 + h * 0.03), (ax1 - w * 0.02, ay1 + h * 0.12)], fill=(120, 230, 140))
    f = F(SANS_B, int(h * 0.20))
    d.text((x0 + w * 0.30, y0 + h * 0.05), "$97.17", font=f, fill=(255, 255, 255))


def scene_icj(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(232, 226, 208))
    cx = x0 + w / 2
    top = y0 + h * 0.14
    d.ellipse([cx - w * 0.05, top, cx + w * 0.05, top + w * 0.10], fill=GOLD)
    d.line([cx, top + w * 0.08, cx, y0 + h * 0.78], fill=(60, 55, 40), width=max(3, int(w * 0.03)))
    beam_y = y0 + h * 0.28
    d.line([x0 + w * 0.14, beam_y, x1 - w * 0.14, beam_y], fill=(60, 55, 40), width=max(3, int(w * 0.03)))
    for sx in (x0 + w * 0.14, x1 - w * 0.14):
        pan_y = y0 + h * 0.52
        d.line([sx, beam_y, sx - w * 0.09, pan_y], fill=(60, 55, 40), width=2)
        d.line([sx, beam_y, sx + w * 0.09, pan_y], fill=(60, 55, 40), width=2)
        d.pieslice([sx - w * 0.11, pan_y - h * 0.06, sx + w * 0.11, pan_y + h * 0.10], 0, 180, fill=GOLD)
    d.rectangle([cx - w * 0.16, y0 + h * 0.78, cx + w * 0.16, y0 + h * 0.84], fill=(60, 55, 40))
    d.rectangle([x0, y0 + h * 0.84, x1, y1], fill=(200, 192, 168))


def scene_cyclone(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (70, 90, 120), (150, 170, 190))
    cx, cy = x0 + w * 0.42, y0 + h * 0.44
    for i in range(4):
        r = w * (0.08 + 0.075 * i)
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], start=200 + i * 50, end=520 + i * 50,
              fill=(240, 245, 250), width=max(3, int(w * 0.035)))
    d.ellipse([cx - w * 0.045, cy - w * 0.036, cx + w * 0.045, cy + w * 0.036], fill=(240, 245, 250))
    for i in range(6):
        rx = x0 + w * (0.62 + 0.055 * i)
        d.line([rx, y0 + h * 0.15, rx - w * 0.04, y0 + h * 0.45], fill=(210, 225, 240), width=3)
    wy = y0 + h * 0.80
    d.rectangle([x0, wy, x1, y1], fill=(30, 80, 130))
    for i in range(4):
        wx = x0 + w * (0.08 + 0.24 * i)
        d.arc([wx, wy - h * 0.03, wx + w * 0.18, wy + h * 0.07], 180, 360, fill=(220, 235, 245), width=3)


def scene_kyiv(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (30, 34, 58), (90, 80, 90))
    base = y0 + h * 0.85
    for fx, fh in [(0.04, .45), (.16, .60), (.30, .38), (.44, .55), (.58, .42), (.72, .58), (.86, .46)]:
        bx = x0 + w * fx
        d.rectangle([bx, base - h * fh, bx + w * 0.10, base], fill=(18, 20, 34))
    d.rectangle([x0, base, x1, y1], fill=(12, 12, 22))
    # explosion starburst
    import math
    ex, ey = x0 + w * 0.52, y0 + h * 0.30
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        r = w * (0.16 if i % 2 == 0 else 0.07)
        pts.append((ex + math.cos(ang) * r, ey + math.sin(ang) * r * 0.8))
    d.polygon(pts, fill=(255, 170, 60))
    d.ellipse([ex - w * 0.045, ey - w * 0.04, ex + w * 0.045, ey + w * 0.04], fill=(255, 230, 160))
    d.line([x0 + w * 0.78, y0 + h * 0.06, ex + w * 0.06, ey - h * 0.04], fill=(255, 210, 120), width=3)


def scene_tanker(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (120, 150, 180), (210, 200, 180))
    wy = y0 + h * 0.72
    d.rectangle([x0, wy, x1, y1], fill=(24, 70, 110))
    hull_y = y0 + h * 0.58
    d.polygon([(x0 + w * 0.08, hull_y), (x0 + w * 0.92, hull_y), (x0 + w * 0.84, wy), (x0 + w * 0.16, wy)],
              fill=(30, 34, 44))
    d.rectangle([x0 + w * 0.12, hull_y - h * 0.16, x0 + w * 0.24, hull_y], fill=(200, 60, 40))
    d.rectangle([x0 + w * 0.26, hull_y - h * 0.13, x0 + w * 0.38, hull_y], fill=(60, 110, 170))
    d.rectangle([x0 + w * 0.40, hull_y - h * 0.16, x0 + w * 0.52, hull_y], fill=(200, 150, 40))
    d.rectangle([x0 + w * 0.78, hull_y - h * 0.22, x0 + w * 0.88, hull_y], fill=(235, 235, 235))
    # flame
    fx, fy = x0 + w * 0.62, hull_y - h * 0.10
    d.polygon([(fx, fy), (fx + w * 0.05, fy - h * 0.30), (fx + w * 0.10, fy)], fill=(240, 110, 30))
    d.polygon([(fx + w * 0.025, fy), (fx + w * 0.05, fy - h * 0.18), (fx + w * 0.075, fy)], fill=(255, 200, 70))
    d.ellipse([fx + w * 0.01, fy - h * 0.42, fx + w * 0.10, fy - h * 0.30], fill=(90, 90, 95))


def scene_taiwan(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    d.rectangle(b, fill=(250, 248, 240))
    pts = [(x0 + w * 0.08, y0 + h * 0.18), (x0 + w * 0.30, y0 + h * 0.34),
           (x0 + w * 0.48, y0 + h * 0.30), (x0 + w * 0.66, y0 + h * 0.55),
           (x0 + w * 0.92, y0 + h * 0.72)]
    d.line(pts, fill=RED, width=max(3, int(w * 0.035)), joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - w * 0.10, pts[-1][1] - h * 0.02),
               (pts[-1][0] - w * 0.03, pts[-1][1] - h * 0.12)], fill=RED)
    for i in range(4):
        gy = y0 + h * (0.2 + 0.18 * i)
        d.line([x0 + w * 0.05, gy, x1 - w * 0.05, gy], fill=(215, 210, 195), width=1)
    # shield
    sx, sy = x0 + w * 0.20, y0 + h * 0.58
    sw, sh = w * 0.20, h * 0.34
    d.polygon([(sx, sy), (sx + sw, sy), (sx + sw, sy + sh * 0.55), (sx + sw / 2, sy + sh), (sx, sy + sh * 0.55)],
              fill=NAVY)
    d.line([(sx + sw * 0.25, sy + sh * 0.42), (sx + sw * 0.45, sy + sh * 0.62), (sx + sw * 0.78, sy + sh * 0.28)],
           fill=(255, 255, 255), width=max(3, int(w * 0.03)), joint="curve")


def scene_korea(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (170, 205, 235), (235, 240, 245))
    wy = y0 + h * 0.70
    d.rectangle([x0, wy, x1, y1], fill=(30, 90, 140))
    hull_y = y0 + h * 0.54
    d.polygon([(x0 + w * 0.06, hull_y), (x0 + w * 0.94, hull_y), (x0 + w * 0.86, wy), (x0 + w * 0.14, wy)],
              fill=(24, 60, 90))
    cols = [(200, 60, 40), (60, 130, 190), (240, 170, 50), (80, 170, 90), (200, 60, 40), (60, 130, 190)]
    for i, c in enumerate(cols):
        bx = x0 + w * (0.12 + 0.115 * i)
        d.rectangle([bx, hull_y - h * 0.20, bx + w * 0.10, hull_y], fill=c)
        if i % 2 == 0:
            d.rectangle([bx, hull_y - h * 0.34, bx + w * 0.10, hull_y - h * 0.20], fill=cols[(i + 2) % 6])
    d.rectangle([x0 + w * 0.82, hull_y - h * 0.30, x0 + w * 0.90, hull_y], fill=(240, 240, 240))
    f = F(SERIF_BOLD, int(h * 0.24))
    d.text((x0 + w * 0.05, y0 + h * 0.02), "$1tn", font=f, fill=NAVY)


def scene_cop(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (150, 200, 230), (230, 245, 220))
    d.ellipse([x0 + w * 0.68, y0 + h * 0.08, x0 + w * 0.90, y0 + h * 0.08 + w * 0.22], fill=(255, 205, 80))
    # leaf
    import math
    cx, cy = x0 + w * 0.40, y0 + h * 0.52
    pts = []
    for t in range(0, 181, 15):
        a = math.radians(t)
        pts.append((cx + math.cos(a) * w * 0.26, cy - math.sin(a) * h * 0.30))
    for t in range(180, -1, -15):
        a = math.radians(t)
        pts.append((cx + math.cos(a) * w * 0.26, cy + math.sin(a) * h * 0.16))
    d.polygon(pts, fill=(40, 140, 70))
    d.line([cx - w * 0.26, cy, cx + w * 0.26, cy - h * 0.02], fill=(230, 245, 220), width=max(2, int(w * 0.02)))
    d.line([cx - w * 0.26, cy, cx - w * 0.34, cy + h * 0.20], fill=(40, 140, 70), width=max(3, int(w * 0.03)))
    d.rectangle([x0, y0 + h * 0.86, x1, y1], fill=(90, 160, 80))


def scene_gaza(d, b):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    _sky(d, b, (235, 215, 180), (250, 240, 215))
    # broken wall
    wy = y0 + h * 0.62
    d.rectangle([x0 + w * 0.06, wy, x0 + w * 0.42, y1], fill=(150, 140, 125))
    d.rectangle([x0 + w * 0.55, wy + h * 0.10, x1 - w * 0.06, y1], fill=(150, 140, 125))
    d.polygon([(x0 + w * 0.42, wy), (x0 + w * 0.48, wy + h * 0.12), (x0 + w * 0.44, y1), (x0 + w * 0.42, y1)],
              fill=(130, 120, 105))
    for i in range(3):
        d.line([x0 + w * 0.06, wy + h * (0.10 + 0.09 * i), x0 + w * 0.42, wy + h * (0.10 + 0.09 * i)],
               fill=(120, 110, 95), width=2)
    # dove
    dx, dy = x0 + w * 0.44, y0 + h * 0.22
    d.ellipse([dx, dy, dx + w * 0.28, dy + h * 0.20], fill=(255, 255, 255))
    d.ellipse([dx + w * 0.22, dy - h * 0.08, dx + w * 0.34, dy + h * 0.05], fill=(255, 255, 255))
    d.polygon([(dx + w * 0.03, dy + h * 0.05), (dx - w * 0.11, dy - h * 0.06), (dx + w * 0.03, dy + h * 0.14)],
              fill=(240, 240, 240))
    d.line([dx + w * 0.32, dy - h * 0.01, dx + w * 0.40, dy + h * 0.02], fill=(240, 160, 40), width=3)
    d.ellipse([dx + w * 0.34, dy + h * 0.03, dx + w * 0.42, dy + h * 0.10], outline=(60, 140, 70), width=3)


SCENES = {
    "summit": scene_summit, "gta": scene_gta, "anthropic": scene_anthropic,
    "icj": scene_icj, "cyclone": scene_cyclone, "kyiv": scene_kyiv,
    "tanker": scene_tanker, "taiwan": scene_taiwan, "korea": scene_korea,
    "cop": scene_cop, "gaza": scene_gaza,
}


# ----------------------------------------------------------------- layout

def hero_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 5], fill=RED)
    scene_h = 108
    SCENES[s["scene"]](d, (x + 2, y + 5, x + w - 2, y + 5 + scene_h))
    badge(d, x + 16, y + 20, 13, s["num"])
    ty = y + 5 + scene_h + 8
    d.text((x + 10, ty), s["place"], font=F(SANS_B, 10), fill=RED)
    ty += 15
    hl = wrap(d, s["head"], F(SERIF_BOLD, 20), w - 20)[:3]
    ty = draw_lines(d, x + 10, ty, hl, F(SERIF_BOLD, 20), INK, 24)
    ty += 3
    bl = wrap(d, s["body"], F(SANS, 11), w - 20)[:6]
    draw_lines(d, x + 10, ty, bl, F(SANS, 11), (40, 40, 40), 14)


def small_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=1)
    d.rectangle([x, y, x + w, y + 3], fill=NAVY)
    sb = (x + 5, y + 8, x + 69, y + h - 6)
    SCENES[s["scene"]](d, sb)
    badge(d, x + 12, y + 13, 10, s["num"])
    tx = x + 75
    tw = w - 82
    ty = y + 7
    d.text((tx, ty), s["place"], font=F(SANS_B, 8), fill=RED)
    ty += 12
    hl = wrap(d, s["head"], F(SERIF_BOLD, 13), tw)[:2]
    ty = draw_lines(d, tx, ty, hl, F(SERIF_BOLD, 13), INK, 16)
    ty += 1
    bl = wrap(d, s["body"], F(COND, 11), tw)[:4]
    draw_lines(d, tx, ty, bl, F(COND, 11), (45, 45, 45), 13)


def world_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 12, y + 7), "WHERE IT HAPPENED", font=F(SERIF_BOLD, 15), fill=(255, 255, 255))
    # stylised continents as blobs (fractions of the panel)
    land = [
        [(0.03, .18), (.10, .08), (.20, .07), (.27, .16), (.25, .32), (.20, .40), (.14, .36), (.08, .38), (.04, .30)],   # N America
        [(0.20, .48), (.27, .46), (.30, .58), (.26, .78), (.22, .88), (.19, .68), (.18, .55)],                          # S America
        [(0.44, .12), (.52, .08), (.56, .18), (.52, .28), (.46, .28), (.43, .20)],                                       # Europe
        [(0.45, .36), (.54, .34), (.58, .46), (.55, .68), (.49, .76), (.45, .55)],                                       # Africa
        [(0.56, .10), (.72, .06), (.85, .13), (.86, .27), (.78, .37), (.70, .48), (.64, .42), (.58, .28)],               # Asia
        [(0.80, .60), (.90, .58), (.92, .70), (.86, .78), (.80, .72)],                                                   # Australia
    ]
    def my(fy):
        return y + 26 + (0.5 + (fy - 0.45) * 1.25) * (h - 34)

    for poly in land:
        pts = [(x + fx * w, my(fy)) for fx, fy in poly]
        d.polygon(pts, fill=MAPLAND)
    for num, (fx, fy) in PINS.items():
        px, py = x + fx * w, my(fy)
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 1), str(num), font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([M, 16, W - M, 16], fill=INK, width=3)
    d.line([M, 21, W - M, 21], fill=INK, width=1)
    d.text((W / 2, 30), "THE WORLD IN ONE DAY", font=F(SERIF_BLACK, 57), fill=INK, anchor="ma")
    d.text((W / 2, 92), "F R I D A Y ,  2 0  N O V E M B E R  2 0 2 6   \u00b7   A L L  T H E  D A Y \u2019 S  N E W S  O N  O N E  P A G E",
           font=F(SANS_B, 13), fill=NAVY, anchor="ma")
    d.line([M, 112, W - M, 112], fill=INK, width=1)
    d.line([M, 115, W - M, 115], fill=INK, width=3)

    # region bar (counts computed from the story data)
    counts = {}
    for s in HEROES + CARDS:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for _, reg, _ in BRIEFS:
        counts[reg] = counts.get(reg, 0) + 1
    order = ["ASIA-PACIFIC", "AMERICAS", "EUROPE", "MIDDLE EAST", "AFRICA", "WORLD"]
    bar = "   \u00b7   ".join(f"{r} {counts.get(r, 0)}" for r in order)
    d.rectangle([M, 122, W - M, 144], fill=NAVY)
    d.text((W / 2, 133), bar, font=F(SANS_B, 12), fill=(255, 255, 255), anchor="mm")

    # figures strip
    fy = 152
    cell_w = CW / len(FIGURES)
    for i, (num, lab) in enumerate(FIGURES):
        cx = M + cell_w * i
        if i:
            d.line([cx, fy + 2, cx, fy + 44], fill=(200, 192, 168), width=1)
        d.text((cx + cell_w / 2, fy), num, font=F(SERIF_BOLD, 26),
               fill=RED if i % 2 == 0 else NAVY, anchor="ma")
        lw = wrap(d, lab, F(SANS, 9), cell_w - 12)[:2]
        ly = fy + 32
        for ln in lw:
            d.text((cx + cell_w / 2, ly), ln, font=F(SANS, 9), fill=GRAY, anchor="ma")
            ly += 11
    d.line([M, 204, W - M, 204], fill=INK, width=1)

    # heroes
    hy, hh = 206, 242
    hw = (CW - 20) / 3
    for i, s in enumerate(HEROES):
        hero_card(d, M + i * (hw + 10), hy, hw, hh, s)

    # small cards, 4 x 2
    cy0 = hy + hh + 8
    ch = 98
    cw4 = (CW - 30) / 4
    for i, s in enumerate(CARDS):
        r, c = divmod(i, 4)
        small_card(d, M + c * (cw4 + 10), cy0 + r * (ch + 8), cw4, ch, s)

    # world map
    my = cy0 + 2 * ch + 14
    world_map(d, M, my, CW, 124)

    # briefs
    by = my + 124 + 8
    d.text((M, by), "ALSO ON THE DAY", font=F(SERIF_BOLD, 17), fill=RED)
    d.line([M + 196, by + 9, W - M, by + 9], fill=INK, width=1)
    by += 24
    cols = 3
    col_w = (CW - (cols - 1) * 14) / cols
    per = (len(BRIEFS) + cols - 1) // cols
    for ci in range(cols):
        x = M + ci * (col_w + 14)
        y = by
        for num, _reg, txt in BRIEFS[ci * per:(ci + 1) * per]:
            d.text((x, y), f"{num}.", font=F(COND_B, 10), fill=RED)
            lines = wrap(d, txt, F(COND, 10), col_w - 22)
            y = draw_lines(d, x + 22, y, lines, F(COND, 10), INK, 11)
            y += 2

    # footer
    fy2 = H - 40
    d.line([M, fy2 - 6, W - M, fy2 - 6], fill=INK, width=1)
    d.text((M, fy2), "DATE CHECK: every story above was reported on 19\u201320 November 2026. "
                     "Older items (EU \u20ac45bn Ukraine loan, 18 Nov; Australia sanctions, 17 Nov) are left out.",
           font=F(SANS, 9), fill=GRAY)
    d.text((M, fy2 + 13), "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 The Guardian \u00b7 IMD \u00b7 Nasdaq \u00b7 Sensor Tower estimates \u00b7 ICJ. "
                          "GTA VI sales are third-party estimates; Take-Two has published no official figure.",
           font=F(SANS, 9), fill=GRAY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
