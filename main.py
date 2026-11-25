#!/usr/bin/env python3
"""THE WORLD TODAY -- Tuesday 24 November 2026.

A one-day world news poster drawn from scratch with pure Python stdlib:
my own 5x7 bitmap font, my own canvas, my own PNG encoder (zlib + CRC32).
No network, no files read, no randomness: two runs write identical bytes.

Layout (1024x1024):
  masthead  -> lead story (Nvidia / Huang) + one-day market bar
  two panels -> War at sea (Merkury) + Sputnik-S
  eight region boxes -> 33 dated stories from 7 regions + Also today
  footer    -> source note
"""

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (248, 244, 232)   # newsprint cream
INK = (20, 20, 20)       # near-black text
RED = (178, 34, 26)      # headline red
NAVY = (28, 58, 92)      # region header band
GOLD = (200, 162, 74)    # thin rules
GREY = (96, 92, 80)      # secondary text
LIGHT = (238, 232, 214)  # panel fill
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- font ----
# My own 5-wide, 7-tall bitmap glyphs. '#' is an ink pixel, '.' is empty.
# One entry per character; unknown characters render as a blank.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "%": ("#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "&": (".###.", "#...#", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "<": ("....#", "...#.", "..#..", ".#...", "..#..", "...#.", "....#"),
    ">": ("#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."),
    "[": (".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."),
    "]": (".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."),
    "*": (".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "....."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
}

BLANK = (".....", ".....", ".....", ".....", ".....", ".....", ".....")


def text_px(text, scale):
    """Pixel width of text at a scale (each glyph 5 wide + 1 gap)."""
    return len(text) * 6 * scale - scale


def wrap_text(text, max_chars):
    """Greedy word wrap to at most max_chars per line; long words split."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            while len(w) > max_chars:
                if cur:
                    lines.append(cur)
                    cur = ""
                lines.append(w[:max_chars])
                w = w[max_chars:]
            if not w:
                continue
            if not cur:
                cur = w
            elif len(cur) + 1 + len(w) <= max_chars:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


# -------------------------------------------------------------- canvas ----
class Canvas:
    """A plain RGB byte buffer with rectangle and bitmap-text drawing."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        self.fill(0, 0, w, h, bg)

    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._idx(x, y)
            self.buf[i] = color[0]
            self.buf[i + 1] = color[1]
            self.buf[i + 2] = color[2]

    def fill(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.buf[i] = r
                self.buf[i + 1] = g
                self.buf[i + 2] = b

    def hline(self, x, y, w, color, thick=1):
        self.fill(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.fill(x, y, thick, h, color)

    def rect(self, x, y, w, h, color, thick=1):
        self.hline(x, y, w, color, thick)
        self.hline(x, y + h - thick, w, color, thick)
        self.vline(x, y, h, color, thick)
        self.vline(x + w - thick, y, h, color, thick)

    def glyph(self, x, y, ch, scale, color, bold=False):
        rows = FONT.get(ch, BLANK)
        for gy in range(7):
            row = rows[gy]
            for gx in range(5):
                if row[gx] != "#":
                    continue
                px = x + gx * scale
                py = y + gy * scale
                self.fill(px, py, scale, scale, color)
                if bold:
                    self.fill(px + 1, py, scale, scale, color)

    def text(self, x, y, s, scale, color, bold=False):
        cx = x
        for ch in s:
            self.glyph(cx, y, ch, scale, color, bold)
            cx += 6 * scale
        return cx

    def text_center(self, cx, y, s, scale, color, bold=False):
        self.text(cx - text_px(s, scale) // 2, y, s, scale, color, bold)

    def text_right(self, rx, y, s, scale, color, bold=False):
        self.text(rx - text_px(s, scale), y, s, scale, color, bold)

    def para(self, x, y, s, scale, color, max_chars, leading, bold_first=False):
        """Draw wrapped paragraph; return the y after the last line."""
        lines = wrap_text(s, max_chars)
        for i, line in enumerate(lines):
            self.text(x, y, line, scale, color, bold=(bold_first and i == 0))
            y += leading
        return y


# ------------------------------------------------------------------ png ----
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(canvas, path):
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    row_len = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        start = y * row_len
        raw += canvas.buf[start:start + row_len]
    data = b"\x89PNG\r\n\x1a\n"
    data += _chunk(b"IHDR", ihdr)
    data += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    data += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


# ------------------------------------------------------------- content ----
# 34 stories, all verified against public reporting of 22-24 Nov 2026.
# Each item is (date tag, headline). Dates are the day the event happened
# or was first reported. Sources are listed in PROGRESS.md.

LEAD_KICKER = "TECH - MARKETS"
LEAD_HEADLINE = "HUANG IS BACK"
LEAD_DECK_1 = (
    "NVIDIA'S BOARD REINSTATES JENSEN HUANG AS CHIEF EXECUTIVE, 11 DAYS "
    "AFTER HE QUIT AMID REPORTS OF AFFAIRS, ONE WITH AN ALLEGED CHINESE "
    "SPY. SHARES JUMP 31%."
)
LEAD_DECK_2 = (
    "TRUMP IS SAID TO HAVE PUSHED FOR THE RETURN. HUANG TESTIFIES BEFORE "
    "CONGRESS ON 3 DEC."
)
BAR_TITLE = "ONE DAY ON WALL STREET"
BAR_CAPTION = (
    "ADDS ABOUT $950BN IN A DAY - THE LARGEST ONE-DAY GAIN IN MARKET HISTORY."
)

PANEL_LEFT_KICKER = "UKRAINE - LIBYA"
PANEL_LEFT_HEADLINE = "WAR AT SEA"
PANEL_LEFT_DECK = (
    "UKRAINIAN SEA DRONES SINK THE RUSSIAN CORVETTE MERKURY OFF BENGHAZI. "
    "A KA-27 HELICOPTER AND THE FREIGHTER MV ANGARA WERE ALSO HIT."
)
PANEL_RIGHT_KICKER = "SPACE - SECURITY"
PANEL_RIGHT_HEADLINE = "SPUTNIK-S"
PANEL_RIGHT_DECK = (
    "GERMAN INVESTIGATORS SAY RUSSIA MAY LAUNCH A NUCLEAR-ARMED SATELLITE "
    "BY DECEMBER. NATO SAYS IT WILL DEFEND SPACE. THE KREMLIN DENIES IT."
)

BOXES = [
    ("EUROPE - 5", [
        ("22 NOV", "COP31 ENDS IN ANTALYA WITH NO DEAL ON CLIMATE FINANCE. "
                   "FOCUS SHIFTS TO COP32 IN ADDIS ABABA."),
        ("23 NOV", "NATO CHIEF RUTTE: THE ALLIANCE WILL DEFEND AGAINST "
                   "THREATS FROM SPACE."),
        ("24 NOV", "GERMANY IS THE FIRST ALLY GIVEN ACCESS TO UKRAINE'S "
                   "DELTA BATTLEFIELD SYSTEM."),
        ("23 NOV", "SEVEN EU STATES BACK LIMITS ON VISAS FOR RUSSIAN CITIZENS."),
        ("24 NOV", "CYPRUS EXPELS TWO RUSSIAN DIPLOMATS OVER SPYING."),
    ]),
    ("MIDDLE EAST - 4", [
        ("24 NOV", "ISRAELI STRIKES KILL HAMAS SECURITY CHIEF NAEEM ABU NAHEL "
                   "AND SIX OTHERS IN GAZA."),
        ("23 NOV", "IRAN VOWS TO CONFRONT A US NAVAL BLOCKADE. VANCE AND RUBIO "
                   "MEET QATAR'S PM AT THE WHITE HOUSE."),
        ("23 NOV", "UN MISSION IN LIBYA URGES A PROBE INTO THE BENGHAZI PORT "
                   "ATTACKS."),
        ("24 NOV", "IRAQ'S PM ORDERS THE OIL MINISTRY TO TAKE OVER OILFIELDS "
                   "IN KURDISH AREAS."),
    ]),
    ("ASIA - 5", [
        ("24 NOV", "INDONESIA FACTORY FIRE TOLL RISES TO 26, WITH DOZENS "
                   "STILL MISSING."),
        ("22 NOV", "SOUTH KOREA'S EDUCATION MINISTER QUITS OVER AI CHEATING "
                   "CHAOS IN THE COLLEGE EXAMS."),
        ("24 NOV", "SOUTH KOREA OFFERS REWARDS OF UP TO $375,000 TO CATCH "
                   "EXAM AI CHEATERS."),
        ("24 NOV", "RUSSIAN AIRCRAFT ENTER SOUTH KOREA'S AIR DEFENCE ZONE."),
        ("23 NOV", "US BLACKLISTS SINGAPORE'S MEGASPEED OVER NVIDIA CHIP "
                   "DIVERSION TO CHINA."),
    ]),
    ("AMERICAS - 4", [
        ("23 NOV", "TRUMP SAYS HE WILL SIGN A DIRECTIVE TO SPEED UP FEDERAL "
                   "DEATH SENTENCES."),
        ("23 NOV", "PENTAGON ACCUSES CANADA OF FALLING SHORT ON NORTH AMERICA "
                   "DEFENCE."),
        ("24 NOV", "US SEEKS SEIZURE OF $1.1BN IN CRYPTO LINKED TO NORTH "
                   "KOREAN HACKERS."),
        ("24 NOV", "US VOTERS BACK 40 MEASURES CURBING DATA-CENTRE GROWTH."),
    ]),
    ("AFRICA - 4", [
        ("24 NOV", "HEAVY FIGHTING IN ITURI TRAPS DR CONGO EBOLA RESPONDERS."),
        ("24 NOV", "SOMALIA AND UGANDA STEP UP THE FIGHT AGAINST AL-SHABAAB."),
        ("24 NOV", "KENYA AND DR CONGO RESTORE FULL DIPLOMATIC TIES."),
        ("24 NOV", "SUDAN DRONE STRIKES KILL FOUR CIVILIANS IN KHARTOUM, "
                   "THE UN SAYS."),
    ]),
    ("OCEANIA - 3", [
        ("24 NOV", "SOLOMON ISLANDS ENDS ITS SECURITY PACT WITH BEIJING AND "
                   "PIVOTS TO CANBERRA."),
        ("24 NOV", "PNG PARLIAMENT VOTES ON RATIFYING BOUGAINVILLE "
                   "INDEPENDENCE."),
        ("24 NOV", "AUSTRALIA'S PM RESISTS CALLS TO SACK BOWEN AFTER THE "
                   "COP31 COLLAPSE."),
    ]),
    ("SPORT & TECH - 4", [
        ("24 NOV", "CHESS: GUKESH ESCAPES TIME TROUBLE TO DRAW GAME 1 WITH "
                   "SINDAROV IN GENEVA."),
        ("24 NOV", "ARM EXTENDS CEO RENE HAAS'S TENURE TO 2033 AMID NVIDIA "
                   "SPECULATION."),
        ("24 NOV", "RUGBY LEAGUE WORLD CUP: AUSTRALIA THRASH FRANCE 92-0; "
                   "NZ BEAT COOK ISLANDS 34-4."),
        ("24 NOV", "OREGON AND VIRGINIA SUE SPACEX OVER ALLEGED GROK "
                   "CHILD-ABUSE IMAGES."),
    ]),
    ("ALSO TODAY - 4", [
        ("24 NOV", "RUSSIA BREAKS ITS ANNUAL TROOP-LOSS RECORD IN UKRAINE: "
                   "432,000 CASUALTIES IN 2026."),
        ("24 NOV", "MORE THAN 700,000 RUSSIAN SOLDIERS KILLED IN NEARLY FIVE "
                   "YEARS OF WAR, A NEW ANALYSIS SAYS."),
        ("23 NOV", "ZELENSKY URGES A NATO INVITE FOR UKRAINE AT THE BERLIN "
                   "ASSEMBLY."),
        ("24 NOV", "CHINA THREATENS THE EU WITH SANCTIONS."),
    ]),
]

FOOTER = ("COMPILED BY AN AI AGENT FROM PUBLIC SOURCES - TUESDAY 24 NOVEMBER "
          "2026 - 34 STORIES, 7 REGIONS")


# -------------------------------------------------------------- layout ----
MX, RX = 28, 996          # left margin, right edge of the content column
COL_W = 472               # region box width
ROW_Y = (444, 579, 714, 849)
ROW_H = 127


def region_box(c, x, y, title, items):
    c.fill(x, y, COL_W, 22, NAVY)
    c.text(x + 8, y + 4, title, 2, WHITE, bold=True)
    c.rect(x, y, COL_W, ROW_H, INK, 1)
    cy = y + 25
    max_chars = (COL_W - 16) // 6
    for date, text in items:
        lines = wrap_text(date + " - " + text, max_chars)[:2]
        for i, line in enumerate(lines):
            c.text(x + 8, cy, line, 1, INK, bold=(i == 0))
            cy += 10
        cy += 2


def build():
    c = Canvas(W, H, PAPER)

    # ---- masthead ------------------------------------------------------
    c.text_center(W // 2, 24, "THE WORLD TODAY", 7, INK)
    c.hline(MX, 82, RX - MX, GOLD, 2)
    c.text(MX, 90, "TUESDAY, 24 NOVEMBER 2026", 2, INK)
    c.text_right(RX, 90, "THE DAY'S WORLD NEWS IN ONE IMAGE", 2, GREY)
    c.hline(MX, 112, RX - MX, GOLD, 2)

    # ---- lead story ----------------------------------------------------
    c.text(MX, 128, LEAD_KICKER, 2, RED)
    c.text(MX, 146, LEAD_HEADLINE, 5, INK)
    c.para(MX, 190, LEAD_DECK_1, 2, INK, 52, 17)
    c.para(MX, 264, LEAD_DECK_2, 2, INK, 52, 17)

    # ---- market bar panel ----------------------------------------------
    px, py, pw, ph = 676, 122, 320, 174
    c.fill(px, py, pw, ph, LIGHT)
    c.rect(px, py, pw, ph, INK, 1)
    c.text_center(px + pw // 2, py + 10, BAR_TITLE, 2, NAVY, bold=True)
    c.text(px + 12, py + 36, "NVIDIA", 2, INK)
    c.fill(px + 12, py + 60, 280, 26, RED)
    c.hline(px + 12, py + 86, 280, INK, 1)
    c.text(px + 12, py + 94, "+31%", 4, RED)
    c.para(px + 12, py + 130, BAR_CAPTION, 1, INK, 49, 9)

    c.hline(MX, 304, RX - MX, INK, 1)

    # ---- second row: two panels -----------------------------------------
    for x, kicker, headline, deck in (
        (MX, PANEL_LEFT_KICKER, PANEL_LEFT_HEADLINE, PANEL_LEFT_DECK),
        (524, PANEL_RIGHT_KICKER, PANEL_RIGHT_HEADLINE, PANEL_RIGHT_DECK),
    ):
        c.text(x, 318, kicker, 1, GREY)
        c.text(x, 330, headline, 3, INK)
        c.para(x, 356, deck, 2, INK, 38, 17)

    c.hline(MX, 436, RX - MX, INK, 1)

    # ---- region grid -----------------------------------------------------
    for i, (title, items) in enumerate(BOXES):
        col = i % 2
        row = i // 2
        region_box(c, MX + col * (COL_W + 24), ROW_Y[row], title, items)

    # ---- footer + frame ---------------------------------------------------
    c.text_center(W // 2, 988, FOOTER, 1, GREY)
    c.rect(10, 10, W - 20, H - 20, INK, 2)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    write_png(build(), os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
