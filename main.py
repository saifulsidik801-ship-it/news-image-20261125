#!/usr/bin/env python3
"""news-image-20261125: draw one newspaper front page summing up the world
news of Wednesday 25 November 2026, and write it to /output/entry.png.

No network, no randomness, no clock: the same run always writes the same
bytes. Pure Pillow vector drawing; every headline, figure and place below
was checked against wire reports dated Wednesday 25 November 2026.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 230)
INK = (25, 25, 25)
MUTED = (90, 86, 78)
RED = (164, 31, 36)
BLUE = (29, 78, 121)
TEAL = (15, 118, 110)
GOLD = (146, 110, 16)
PURPLE = (107, 63, 141)
SEA = (222, 233, 238)
LAND = (232, 220, 192)
LAND_LINE = (190, 172, 130)
RULE = (25, 25, 25)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

REGION_COLOR = {
    "EUROPE": BLUE,
    "MIDDLE EAST": RED,
    "ASIA": TEAL,
    "AMERICAS": PURPLE,
    "OCEANIA": (14, 116, 144),
    "GLOBAL": (90, 86, 78),
    "AFRICA": (146, 110, 16),
}

# ---------------------------------------------------------------- stories
# Every story happened, or was first reported, on Wednesday 25 Nov 2026.
HEROES = [
    dict(n=1, region="ASIA", place="SEOUL / TOKYO", tag="CONFIRMED",
         headline="Asia markets plunge as AI rally reverses",
         summary=("Kospi falls 5.3%, Taiwan 5.1% and the Nikkei 2.8% as fresh "
                  "US tariff threats hit sentiment and the tech rally fizzles. "
                  "Advantest drops 12%. \u2014 Reuters"),
         scene="markets"),
    dict(n=2, region="MIDDLE EAST", place="GAZA", tag="REPORTED",
         headline="Strike on Gaza food-aid vehicle kills three",
         summary=("An Israeli strike hits a vehicle carrying food aid, killing "
                  "three. A man is shot dead in Jabalia; three are wounded "
                  "in Khan Younis. \u2014 Al Jazeera"),
         scene="gaza"),
    dict(n=3, region="MIDDLE EAST", place="ADEN, YEMEN", tag="REPORTED",
         headline="Houthis edge closer to Aden",
         summary=("Yemen\u2019s Houthis advance as government forces pull out of "
                  "Bab al-Mandeb. Washington and Riyadh confer on the "
                  "Houthi attacks. \u2014 Al Jazeera \u00b7 Reuters"),
         scene="yemen"),
]

SECONDARIES = [
    dict(n=4, region="AMERICAS", place="WASHINGTON", icon="chart",
         headline="US inflation test due today",
         summary="Markets await US PCE data, due Wednesday, before the Fed\u2019s final meeting of 2026."),
    dict(n=5, region="AMERICAS", place="IOWA, US", icon="blast",
         headline="Army to blow up 5 tonnes of explosives",
         summary="The US Army will detonate unstable explosives in Iowa on Wednesday."),
    dict(n=6, region="ASIA", place="KABUL", icon="radio",
         headline="Shortwave school back for Afghan girls",
         summary="RFE/RL returns to shortwave with new educational radio for girls barred from school."),
    dict(n=7, region="MIDDLE EAST", place="TEHRAN", icon="flame",
         headline="Iran braces for winter gas shortages",
         summary="War damage deepens the energy crisis as rationing bites and winter closes in."),
    dict(n=8, region="ASIA", place="MANILA", icon="bus",
         headline="Transport strike runs into Wednesday",
         summary="The MANIBELA protest extends to 25 November as drivers press their demands."),
    dict(n=9, region="MIDDLE EAST", place="RIYADH", icon="coins",
         headline="Saudi 2027 budget bets on growth",
         summary="The Kingdom\u2019s 2027 budget predicts growth despite this year\u2019s challenges."),
    dict(n=10, region="ASIA", place="MANILA", icon="bank",
         headline="BSP signals gentler rate rises",
         summary="The Bangko Sentral may ease rate increases as growth cools, its governor signals."),
    dict(n=11, region="EUROPE", place="BERLIN", icon="drone",
         headline="Berlin to build Ukraine\u2019s recon drones",
         summary="Germany is set to produce Ukrainian-made reconnaissance drones for Kyiv."),
]

# (number, place, one line) -- each line must stay short enough for one row.
ALSO = [
    (12, "UN", "\u201cNo excuse for inaction\u201d on Gaza, deputy chief says"),
    (13, "London", "UK warns Ukraine suppliers of sabotage risk"),
    (14, "New Delhi", "Gandhi backs strong India\u2013Israel ties"),
    (15, "Jerusalem", "Netanyahu pushes no-Palestinian-state pacts"),
    (16, "Gaza", "Civil Defence says 85% of vehicles out of service"),
    (17, "Gaza", "NGO ban forces 37 aid groups to halt work"),
    (18, "Crimea", "Ukraine drone attack kills two; bridge targeted"),
    (19, "Gulf", "Iran says it downed US drones over Hormuz"),
    (20, "Riyadh", "US and Saudis confer on Houthi attacks"),
    (21, "Wellington", "NZ \u201cdeeply concerned\u201d over West Bank violence"),
    (22, "Manila", "Infra spending rose 14% in September"),
    (23, "Manila", "Philippines 98th of 137 in entrepreneurship"),
    (24, "Jerusalem", "Calls grow to free Palestinian student"),
    (25, "Riyadh", "New Saudi law shields women from abuse"),
    (26, "Kyiv", "Ukraine\u2019s war spreads to Africa, Al Jazeera finds"),
    (27, "Gaza", "Children struggle for insulin as supplies run short"),
    (28, "Hebron", "Restored wells bring water to the Old City"),
    (29, "New York", "Board of Peace report faults both sides"),
    (30, "Sanaa", "Court sentences five to death for \u201cspying\u201d"),
    (31, "Kuwait City", "Kuwait reports drone attacks in the Gulf"),
]

NUMBERS = [
    ("-5.3%", "KOSPI falls in Seoul"),
    ("-2.8%", "Nikkei drops in Tokyo"),
    ("3", "killed in Gaza aid strike"),
    ("5 t", "of explosives, Iowa blast"),
    ("37", "aid groups halted in Gaza"),
]

# (story number, lon, lat, dx, dy) pins for the world map; dx/dy nudge
# pins apart where several stories share one small region.
PINS = [
    (1, 127.0, 37.5, 0, 0), (2, 34.5, 31.5, -14, 6),
    (3, 45.0, 12.8, 0, 0), (5, -93.5, 42.0, 0, 0),
    (6, 69.2, 34.5, 0, 0), (7, 51.4, 35.7, 10, -10),
    (8, 121.0, 14.6, 0, 0), (9, 46.7, 24.6, 8, 8),
    (11, 13.4, 52.5, 0, 0), (13, -0.1, 51.5, 0, 0),
    (14, 77.2, 28.6, 0, 0), (15, 35.2, 31.8, 12, -8),
    (18, 34.0, 45.0, 0, 0), (21, 174.8, -41.3, 0, 0),
]


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, width):
    """Split text into lines that fit width (pixels)."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, width, lh):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def center(draw, y, text, fnt, fill, cx=W // 2):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def hline(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def badge(draw, x, y, n, d=18, bg=RED, fg=(255, 255, 255)):
    draw.ellipse([x, y, x + d, y + d], fill=bg)
    f = SANS_B(11)
    t = str(n)
    draw.text((x + d / 2 - draw.textlength(t, font=f) / 2, y + 3), t,
              font=f, fill=fg)


def tag_chip(draw, x, y, text, bg, fnt=None):
    fnt = fnt or SANS_B(10)
    w = draw.textlength(text, font=fnt) + 10
    draw.rectangle([x, y, x + w, y + 15], fill=bg)
    draw.text((x + 5, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- scenes
def scene_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 243, 246),
                outline=LAND_LINE, width=1)
    # grid
    for i in range(1, 4):
        gy = y + h * i / 4
        d.line([(x, gy), (x + w, gy)], fill=(205, 216, 222), width=1)
    # candlesticks: a brief uptick, then a slide down
    closes = [0.80, 0.86, 0.78, 0.68, 0.60, 0.50, 0.42, 0.32]
    bw = w / (len(closes) + 1)
    pts = []
    for i, c in enumerate(closes):
        cx = x + bw * (i + 0.75)
        top = y + h * (1 - c) - 14
        bot = top + 26
        col = (34, 139, 92) if i < 2 else (178, 34, 34)
        d.line([(cx, top - 6), (cx, bot + 6)], fill=col, width=2)
        d.rectangle([cx - 7, top, cx + 7, bot], fill=col)
        pts.append((cx, top + 13))
    d.line(pts, fill=RED, width=3)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
              fill=RED)
    tag_chip(d, x + 8, y + 8, "KOSPI -5.3%", RED)
    tag_chip(d, x + 8, y + 28, "NIKKEI -2.8%", (25, 25, 25))
    tag_chip(d, x + w - 118, y + h - 24, "TAIWAN -5.1%", RED)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(236, 224, 200),
                outline=LAND_LINE, width=1)
    # sea on the left, land on the right
    d.polygon([(x, y), (x + 78, y), (x + 62, y + h), (x, y + h)],
              fill=(178, 208, 222))
    d.line([(x + 78, y), (x + 62, y + h)], fill=(25, 25, 25), width=2)
    # Gaza strip: a narrow coastal strip
    d.polygon([(x + 88, y + 14), (x + 120, y + 20), (x + 134, y + h - 20),
               (x + 100, y + h - 12)], fill=(217, 201, 163),
              outline=RED, width=2)
    d.text((x + 130, y + 52), "GAZA", font=SANS_B(12), fill=RED)
    # aid truck
    tx, ty = x + 190, y + 78
    d.rectangle([tx, ty, tx + 62, ty + 26], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([tx + 62, ty + 8, tx + 84, ty + 26], fill=(255, 255, 255),
                outline=INK, width=2)
    d.text((tx + 6, ty + 7), "AID", font=SANS_B(11), fill=INK)
    for wx in (tx + 12, tx + 50, tx + 72):
        d.ellipse([wx, ty + 26, wx + 12, ty + 38], fill=INK)
    # blast star
    bx, by = x + 128, y + 30
    for k in range(8):
        import math
        a = k * math.pi / 4
        d.line([(bx, by), (bx + 16 * math.cos(a), by + 16 * math.sin(a))],
               fill=(214, 120, 20), width=3)
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(214, 120, 20))
    tag_chip(d, x + 8, y + 8, "3 KILLED", RED)


def scene_yemen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=LAND_LINE, width=1)
    # Arabia + Horn of Africa, very simplified
    d.polygon([(x + 60, y + 12), (x + 210, y + 20), (x + 250, y + 60),
               (x + 235, y + 120), (x + 180, y + 138), (x + 120, y + 110),
               (x + 80, y + 70), (x + 55, y + 40)], fill=LAND,
              outline=LAND_LINE, width=1)
    d.polygon([(x + 30, y + 118), (x + 95, y + 128), (x + 110, y + h - 4),
               (x + 40, y + h - 4)], fill=(216, 200, 164),
              outline=LAND_LINE, width=1)
    d.text((x + 96, y + 42), "YEMEN", font=SANS_B(11), fill=INK)
    d.text((x + 150, y + 96), "BAB AL-MANDEB", font=SANS_B(9), fill=BLUE)
    # dashed arrow toward Aden
    ax, ay = x + 150, y + 124
    for i in range(6):
        d.line([(ax + i * 11, ay), (ax + i * 11 + 6, ay)], fill=RED, width=3)
    d.polygon([(ax + 72, ay - 6), (ax + 72, ay + 6), (ax + 84, ay)], fill=RED)
    d.ellipse([ax + 78, ay - 16, ax + 96, ay + 2], fill=RED)
    d.text((ax + 80, ay - 14), "A", font=SANS_B(11), fill=(255, 255, 255))
    tag_chip(d, x + 8, y + 8, "60 KM FROM ADEN", RED)


SCENES = {"markets": scene_markets, "gaza": scene_gaza, "yemen": scene_yemen}


def draw_icon(d, kind, x, y, w, h, ink):
    cx, cy = x + w / 2, y + h / 2
    if kind == "chart":
        for i, bh in enumerate((8, 14, 11, 20)):
            bx = x + 10 + i * 12
            d.rectangle([bx, y + h - 8 - bh, bx + 8, y + h - 8], fill=ink)
        d.line([(x + 8, y + 10), (x + w - 10, y + h - 16)], fill=RED, width=2)
        d.polygon([(x + w - 16, y + h - 16), (x + w - 8, y + h - 16),
                   (x + w - 12, y + h - 8)], fill=RED)
    elif kind == "blast":
        import math
        for k in range(10):
            a = k * math.pi / 5
            r = 20 if k % 2 == 0 else 9
            d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
                   fill=(214, 120, 20), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    elif kind == "radio":
        d.polygon([(cx - 8, y + h - 6), (cx + 8, y + h - 6), (cx, y + 8)],
                  outline=ink, width=2)
        for r in (8, 14, 20):
            d.arc([cx - r, cy - r, cx + r, cy + r], -60, 240, fill=RED, width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    elif kind == "flame":
        d.polygon([(cx, y + 4), (cx + 11, y + 20), (cx + 7, y + 34),
                   (cx - 7, y + 34), (cx - 11, y + 20)], fill=(214, 120, 20))
        d.ellipse([cx - 5, y + 20, cx + 5, y + 32], fill=(245, 200, 60))
    elif kind == "bus":
        d.rounded_rectangle([x + 6, y + 8, x + w - 6, y + h - 12], radius=4,
                            outline=ink, width=2)
        for i in range(3):
            d.rectangle([x + 12 + i * 13, y + 14, x + 20 + i * 13, y + 22],
                        fill=ink)
        for wx in (x + 14, x + w - 24):
            d.ellipse([wx, y + h - 12, wx + 10, y + h - 2], fill=ink)
    elif kind == "coins":
        for i, yy in enumerate((y + 22, y + 15, y + 8)):
            d.ellipse([cx - 14, yy, cx + 14, yy + 10], fill=(212, 175, 55),
                      outline=(120, 90, 20), width=1)
            d.text((cx - 4, yy + 1), "$", font=SANS_B(8), fill=(120, 90, 20))
    elif kind == "bank":
        d.polygon([(cx - 20, y + 12), (cx + 20, y + 12), (cx, y + 2)],
                  fill=ink)
        for i in range(3):
            bx = cx - 16 + i * 12
            d.rectangle([bx, y + 14, bx + 4, y + 30], fill=ink)
        d.rectangle([cx - 22, y + 30, cx + 22, y + 34], fill=ink)
    elif kind == "drone":
        d.rectangle([cx - 7, cy - 5, cx + 7, cy + 5], fill=ink)
        for dx, dy in ((-16, -12), (16, -12), (-16, 12), (16, 12)):
            d.line([(cx, cy), (cx + dx, cy + dy)], fill=ink, width=2)
            d.ellipse([cx + dx - 6, cy + dy - 3, cx + dx + 6, cy + dy + 3],
                      outline=ink, width=2)


# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-60, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
     (-90, 21), (-97, 16), (-105, 20), (-117, 33), (-125, 40), (-125, 49),
     (-140, 60), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10), (-35, -20),
     (-40, -30), (-50, -35), (-60, -40), (-70, -50), (-73, -40),
     (-73, -25), (-80, -15), (-80, 5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 68), (40, 68),
     (44, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 42), (-2, 37), (-9, 37)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -28),
     (20, -35), (15, -30), (12, -18), (9, -5), (9, 4), (-8, 5), (-13, 10)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (80, 72), (100, 76), (120, 73),
     (140, 72), (160, 70), (170, 66), (162, 60), (158, 52), (142, 50),
     (140, 40), (135, 35), (127, 33), (122, 30), (120, 25), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 13),
     (77, 8), (73, 20), (68, 25), (62, 25), (57, 26), (52, 28), (48, 30),
     (44, 30), (40, 36), (36, 36), (33, 42), (30, 45), (30, 50), (30, 55)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (136, -12), (132, -12), (126, -14),
     (122, -17), (118, -20)],
]


def draw_world_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=LAND_LINE, width=1)
    lon0, lon1, lat0, lat1 = -170.0, 190.0, -60.0, 85.0

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat1 - lat) / (lat1 - lat0) * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_LINE)
    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = SANS_B(8)
        t = str(n)
        d.text((px - d.textlength(t, font=f) / 2, py - 5), t, font=f,
               fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
ALSO_REGIONS = ["GLOBAL", "EUROPE", "ASIA", "MIDDLE EAST", "MIDDLE EAST",
                "MIDDLE EAST", "EUROPE", "MIDDLE EAST", "MIDDLE EAST",
                "OCEANIA", "ASIA", "ASIA", "MIDDLE EAST", "MIDDLE EAST",
                "EUROPE", "MIDDLE EAST", "MIDDLE EAST", "GLOBAL",
                "MIDDLE EAST", "MIDDLE EAST"]

TINTS = {
    "EUROPE": (214, 228, 240), "MIDDLE EAST": (244, 214, 214),
    "ASIA": (208, 235, 231), "AMERICAS": (232, 220, 240),
    "OCEANIA": (208, 232, 240), "GLOBAL": (228, 228, 228),
    "AFRICA": (240, 230, 200),
}


def region_counts():
    counts = {}
    for s in HEROES + SECONDARIES:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for r in ALSO_REGIONS:
        counts[r] = counts.get(r, 0) + 1
    return counts


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    total = len(HEROES) + len(SECONDARIES) + len(ALSO)
    counts = region_counts()
    order = ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS",
             "OCEANIA", "GLOBAL"]
    parts = [f"{r} {counts.get(r, 0)}" for r in order if counts.get(r, 0)]

    # ---- top strip
    f_top = SANS_B(11)
    d.text((14, 10), "THE WORLD ON ONE PAGE", font=f_top, fill=INK)
    center(d, 10, "EARLY EDITION \u00b7 REPORTED BY 02:30 UTC", f_top, RED)
    rtxt = "EVERY STORY DATED WED 25 NOV"
    d.text((W - 14 - d.textlength(rtxt, font=f_top), 10), rtxt, font=f_top,
           fill=INK)
    hline(d, 14, W - 14, 30)

    # ---- masthead
    f_mast = SERIF_B(58)
    center(d, 34, "Wednesday 25 November 2026", f_mast, INK)
    hline(d, 14, W - 14, 100, width=2)

    # ---- count strip
    f_cnt = SANS_B(12)
    center(d, 106,
           f"{total} STORIES, ALL FROM WEDNESDAY 25 NOV \u00b7 "
           + " \u00b7 ".join(parts), f_cnt, INK)
    hline(d, 14, W - 14, 126)

    # ---- ticker
    f_tick = SERIF_B(14)
    center(d, 130,
           "Asia stocks tumble  \u25c6  Strike kills 3 in Gaza  \u25c6  "
           "Houthis edge closer to Aden", f_tick, INK)
    hline(d, 14, W - 14, 152)

    # ---- number strip
    y0 = 158
    for i, (num, lab) in enumerate(NUMBERS):
        x = 14 + i * (192 + 9)
        f_num = SERIF_B(26)
        center(d, y0, num, f_num, RED, cx=x + 96)
        f_lab = SANS(10)
        center(d, y0 + 32, lab, f_lab, MUTED, cx=x + 96)
        if i:
            d.line([(x - 5, y0 + 2), (x - 5, y0 + 46)], fill=LAND_LINE, width=1)
    hline(d, 14, W - 14, y0 + 52)

    # ---- heroes
    hy = 216
    for i, s in enumerate(HEROES):
        x = 14 + i * (324 + 12)
        col = REGION_COLOR[s["region"]]
        SCENES[s["scene"]](d, x, hy, 324, 148)
        ty = hy + 156
        badge(d, x, ty, s["n"])
        d.text((x + 24, ty + 2),
               f"{s['region']} \u00b7 {s['place']}", font=SANS_B(11), fill=col)
        tag_chip(d, x + 324 - 84, ty, s["tag"], col)
        draw_wrapped(d, x, ty + 22, s["headline"], SERIF_B(20), INK, 324, 23)
        draw_wrapped(d, x, ty + 94, s["summary"], SANS(12), INK, 324, 15)
    hline(d, 14, W - 14, hy + 312)

    # ---- secondaries
    sy = hy + 322
    for row in range(2):
        for col_i in range(4):
            s = SECONDARIES[row * 4 + col_i]
            x = 14 + col_i * (243 + 8)
            y = sy + row * (112 + 8)
            col = REGION_COLOR[s["region"]]
            d.rectangle([x, y, x + 243, y + 38], fill=TINTS[s["region"]],
                        outline=LAND_LINE, width=1)
            draw_icon(d, s["icon"], x, y, 243, 38, col)
            badge(d, x, y + 44, s["n"], d=15)
            d.text((x + 20, y + 45), s["place"], font=SANS_B(10), fill=col)
            draw_wrapped(d, x, y + 60, s["headline"], SERIF_B(13), INK,
                         243, 15)
            draw_wrapped(d, x, y + 91, s["summary"], SANS(10), INK, 243, 12)

    # ---- bottom: map + also-on list
    by = sy + 2 * 112 + 8 + 10
    d.rectangle([14, by, 14 + 140, by + 18], fill=INK)
    d.text((20, by + 3), "WHERE IT HAPPENED", font=SANS_B(10),
           fill=(255, 255, 255))
    d.text((160, by + 3), "pins carry the story numbers", font=SANS(10),
           fill=MUTED)
    draw_world_map(d, 14, by + 24, 316, 140)

    ax = 342
    d.text((ax, by + 3), "ALSO ON WEDNESDAY 25 NOVEMBER 2026",
           font=SANS_B(11), fill=RED)
    hline(d, ax, W - 14, by + 20)
    f_num, f_pl, f_tx = SANS_B(10), SANS_B(10), SANS(10)
    iy = by + 26
    for col_i in range(2):
        for j in range(10):
            n, place, text = ALSO[col_i * 10 + j]
            x = ax + col_i * 338
            y = iy + j * 14
            d.text((x, y), str(n), font=f_num, fill=RED)
            px = x + 20
            d.text((px, y), place, font=f_pl, fill=INK)
            tx = px + d.textlength(place, font=f_pl) + 4
            d.text((tx, y), text, font=f_tx, fill=INK)

    # ---- date check
    dy = by + 24 + 140 + 10
    d.rectangle([14, dy, W - 14, dy + 40], outline=RED, width=2)
    d.text((22, dy + 4), "DATE CHECK", font=SANS_B(10), fill=RED)
    draw_wrapped(
        d, 22, dy + 18,
        "Left out as other days\u2019 news. Mon 23 Nov: Nvidia reinstates Huang; "
        "NATO talks after Poland missiles; Dymer toll 11. Tue 24 Nov: Sarkozy "
        "trial ordered; Giuliani Medal of Freedom; rial record low; 60 Patriots "
        "held back; 700,000 toll study; Huawei convicted; Houthis hit Riyadh "
        "tower. Background only: Nasdaq\u2019s Tuesday fall.",
        SANS(10), INK, W - 44, 12)

    # ---- footer
    fy = dy + 48
    hline(d, 14, W - 14, fy)
    center(d, fy + 6,
           "Every story happened or was first reported on Wednesday 25 "
           "November 2026. Maps and drawings are original vector art. "
           "Sources: Reuters, Al Jazeera, RFE/RL, Arab News, BusinessWorld, GMA.",
           SANS(9), MUTED)
    return img


def main():
    out = os.environ.get("ENTRY_OUTPUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = build()
    img.save(out, optimize=True)
    print(f"wrote {out} {img.size} "
          f"{os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
