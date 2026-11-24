#!/usr/bin/env python3
"""Build the 24 November 2026 world-news poster (1024x1024 PNG).

The poster is a newspaper front page: masthead, one lead story and five
more stories, all drawn with Pillow and the DejaVu fonts shipped on this
machine. No network is used; every word on the poster is baked into this
file from the day's wire reports. Run: python3 make_poster.py
Writes poster.png next to this script.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "poster.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (18, 18, 18)
RED = (178, 34, 34)
GOLD = (184, 134, 11)
GREY = (90, 86, 78)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)


def font(name, size):
    paths = [
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
        f"/usr/share/fonts/truetype/liberation/{name}.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold", 62)
F_DATE = font("DejaVuSans", 27)
F_KICKER = font("DejaVuSans-Bold", 24)
F_HEAD = font("DejaVuSans-Bold", 46)
F_BODY = font("DejaVuSans", 25)
F_PANEL_HEAD = font("DejaVuSans-Bold", 29)
F_PANEL_BODY = font("DejaVuSans", 22)
F_FOOT = font("DejaVuSans", 20)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(draw, x, y, w, h, accent, kicker, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=(210, 205, 192), width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)
    cx, cy = x + 24, y + 26
    draw.text((cx, cy), kicker, font=F_KICKER, fill=accent)
    cy += 36
    for line in wrap(draw, headline, F_PANEL_HEAD, w - 48):
        draw.text((cx, cy), line, font=F_PANEL_HEAD, fill=INK)
        cy += 36
    cy += 4
    for line in wrap(draw, body, F_PANEL_BODY, w - 48):
        draw.text((cx, cy), line, font=F_PANEL_BODY, fill=GREY)
        cy += 30


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 148], fill=INK)
    d.text((W // 2, 26), "THE WORLD IN ONE IMAGE", font=F_TITLE,
           fill=WHITE, anchor="ma")
    d.text((W // 2, 100), "TUESDAY  ·  24 NOVEMBER 2026",
           font=F_DATE, fill=(216, 178, 90), anchor="ma")

    # Lead story: Nvidia reinstates Jensen Huang.
    lx, ly, lw, lh = 36, 172, 952, 236
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD,
                        outline=(210, 205, 192), width=2)
    d.rectangle([lx, ly, lx + 12, ly + lh], fill=(27, 94, 32))
    d.text((lx + 36, ly + 22), "LEAD STORY  ·  TECHNOLOGY",
           font=F_KICKER, fill=RED)
    d.text((lx + 36, ly + 56), "HUANG IS BACK", font=F_HEAD, fill=INK)
    lead = ("Nvidia reinstates Jensen Huang as chief executive after a "
            "push from President Trump — a stunning reversal that adds "
            "about $34 billion to his fortune in a single day.")
    cy = ly + 118
    for line in wrap(d, lead, F_BODY, lw - 72):
        d.text((lx + 36, cy), line, font=F_BODY, fill=GREY)
        cy += 33

    # Four more stories in a 2x2 grid.
    panels = [
        ((178, 34, 34), "KOREA  ·  AIRSPACE",
         "JET INCURSION",
         "A suspected North Korean jet breaches South Korea's "
         "airspace near Ulleung; islanders are told to shelter."),
        ((27, 58, 120), "UKRAINE  ·  WAR",
         "WAR SPREADS",
         "Ukraine hits a Russian warship off Libya; hacked data puts "
         "Russia's death toll near 500,000."),
        ((120, 70, 10), "USA  ·  IOWA",
         "BLAST ON HOLD",
         "Trump halts the planned detonation of explosives at an Iowa "
         "plant pending a court ruling."),
        ((0, 105, 92), "SPORT  ·  FOOTBALL",
         "WORLD CUP 2031",
         "The U.S., Mexico, Costa Rica and Jamaica will host the "
         "Women's World Cup; the U.K. gets 2035."),
    ]
    gx, gy, gw, gh, gap = 36, 432, 466, 210, 20
    for i, (accent, kicker, head, body) in enumerate(panels):
        px = gx + (i % 2) * (gw + gap)
        py = gy + (i // 2) * (gh + gap)
        draw_panel(d, px, py, gw, gh, accent, kicker, head, body)

    # Bottom strip: Gomez resignation.
    bx, by, bw, bh = 36, 880, 952, 96
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=CARD,
                        outline=(210, 205, 192), width=2)
    d.rectangle([bx, by, bx + 12, by + bh], fill=(90, 40, 90))
    d.text((bx + 30, by + 12), "ALSO",
           font=F_KICKER, fill=(90, 40, 90))
    cy = by + 44
    strip = ("Rep. Jimmy Gomez resigns after the Ethics panel finds "
             "evidence of sexual misconduct.")
    for line in wrap(d, strip, F_PANEL_BODY, bw - 60):
        d.text((bx + 30, cy), line, font=F_PANEL_BODY, fill=INK)
        cy += 27

    d.text((W // 2, 990), "24 NOVEMBER 2026  ·  COMPILED FROM WIRE REPORTS",
           font=F_FOOT, fill=GREY, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
