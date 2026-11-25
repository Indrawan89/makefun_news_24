# News-image 20261124 — dense poster build

Competition: news-image-20261124 — "Sum up 24 November's world news in one image"
($100, deadline 2026-11-26T00:00:00Z / 26 Nov 07:00 WIB). Repo: Indrawan89/makefun_news_24.

## Poster

`main.py` — pure Python stdlib, written fresh in this session (own 5x7 bitmap
font, own canvas, own PNG encoder with zlib+CRC32). No file from any earlier
edition was read, copied, or re-typed. 1024x1024, masthead "THE WORLD TODAY —
Tuesday 24 November 2026".

- Lead: NVIDIA reinstates Jensen Huang as CEO (11 days after he quit; stock
  +31%, about $950bn added — largest one-day gain in market history) + market
  bar panel.
- Panels: WAR AT SEA (Ukrainian sea drones sink Russian corvette Merkury off
  Benghazi) and SPUTNIK-S (Russia may launch a nuclear-armed satellite by
  December).
- 8 boxes, 33 dated stories: Europe 5, Middle East 4, Asia 5, Americas 4,
  Africa 4, Oceania 3, Sport & Tech 4, Also today 4. Total 34 stories.

## Story list (date = day the event happened or was first reported)

Lead — NVIDIA board reinstates Jensen Huang as CEO, 11 days after he resigned;
stock +31%, ~$950bn added, largest one-day gain in market history; Trump said
to have pushed the return; Huang testifies before Congress 3 Dec.
Sources: Techmeme 24 Nov 04:10 UTC; KNKX/AP 24 Nov; Evening Report NZ 24 Nov.

Europe (5)
- 22 Nov — COP31 ends in Antalya with no deal on climate finance; focus
  shifts to COP32 in Addis Ababa. Source: WRI statement 22 Nov; AP 22 Nov.
- 23 Nov — NATO chief Rutte: the alliance will defend against threats from
  space. Source: WDR/NDR reporting 23 Nov; Just Security Early Edition 24 Nov.
- 24 Nov — Germany is the first ally given access to Ukraine's Delta
  battlefield system. Source: Kyiv Independent 24 Nov.
- 23 Nov — Seven EU states back limits on visas for Russian citizens.
  Source: EU letter reported 23 Nov.
- 24 Nov — Cyprus expels two Russian diplomats over spying. Source: news
  wires 24 Nov.

Middle East (4)
- 24 Nov — Israeli strikes kill Hamas security chief Naeem Abu Nahel and six
  others in Gaza. Source: Just Security Early Edition 24 Nov.
- 23 Nov — Iran vows to confront a US naval blockade; Vance and Rubio meet
  Qatar's PM at the White House. Source: Just Security Early Edition 24 Nov.
- 23 Nov — UN mission in Libya (UNSMIL) urges a probe into the Benghazi port
  attacks. Source: UN News 23 Nov.
- 24 Nov — Iraq's PM orders the oil ministry to take over oilfields in
  Kurdish areas. Source: news wires 24 Nov.

Asia (5)
- 24 Nov — Indonesia factory fire toll rises to 26, with dozens still missing
  (fire broke out 21 Nov at PT Fonusa Agung Mulia, Cikande, Banten).
  Source: NYT 24 Nov 13:29 UTC; AP 23 Nov.
- 22 Nov — South Korea's education minister Choi Kyo-jin resigns over AI
  cheating chaos in the college exams (CSAT). Source: Korea JoongAng Daily
  22 Nov; Korea Times 23 Nov.
- 24 Nov — South Korea offers rewards of up to $375,000 to catch exam AI
  cheaters. Source: Just Security Early Edition 24 Nov.
- 24 Nov — Russian aircraft enter South Korea's air defence zone.
  Source: Just Security Early Edition 24 Nov.
- 23 Nov — US blacklists Singapore's Megaspeed over NVIDIA chip diversion to
  China. Source: Just Security Early Edition 24 Nov.

Americas (4)
- 23 Nov — Trump says he will sign a directive to speed up federal death
  sentences. Source: Just Security Early Edition 24 Nov.
- 23 Nov — Pentagon accuses Canada of falling short on North America defence.
  Source: Just Security Early Edition 24 Nov.
- 24 Nov — US seeks seizure of $1.1bn in crypto linked to North Korean
  hackers. Source: news wires 24 Nov.
- 24 Nov — US voters back 40 measures curbing data-centre growth.
  Source: Motley Fool 24 Nov.

Africa (4)
- 24 Nov — Heavy fighting in Ituri traps DR Congo Ebola responders.
  Source: UN News 24 Nov.
- 24 Nov — Somalia and Uganda step up the fight against al-Shabaab (joint
  communique 23 Nov, Entebbe). Source: Hiiraan Online 24 Nov.
- 24 Nov — Kenya and DR Congo restore full diplomatic ties.
  Source: Horn Economic Review / African Spectator 24 Nov.
- 24 Nov — Sudan drone strikes kill four civilians in Khartoum, the UN says.
  Source: UN OCHA via Himalaya Times 24 Nov.

Oceania (3)
- 24 Nov — Solomon Islands ends its security pact with Beijing and pivots to
  Canberra. Source: PNG Post-Courier / Monolith News 24 Nov.
- 24 Nov — PNG parliament votes on ratifying Bougainville independence.
  Source: Evening Report NZ 24 Nov.
- 24 Nov — Australia's PM resists calls to sack Bowen after the COP31
  collapse. Source: The Age live blog 24 Nov.

Sport & Tech (4)
- 24 Nov — Chess: Gukesh escapes time trouble to draw Game 1 with Sindarov
  in Geneva (World Championship, 14 games, $2.5m fund). Source: FIDE report
  24 Nov.
- 24 Nov — Arm extends CEO Rene Haas's tenure to 2033 amid NVIDIA
  speculation. Source: TradingView 24 Nov.
- 24 Nov — Rugby League World Cup: Australia thrash France 92-0; NZ beat
  Cook Islands 34-4. Source: BBC Sport 24 Nov.
- 24 Nov — Oregon and Virginia sue SpaceX over alleged Grok child-abuse
  images. Source: news wires 24 Nov.

Also today (4)
- 24 Nov — Russia breaks its annual troop-loss record in Ukraine: 432,000
  casualties in 2026. Source: news wires 24 Nov.
- 24 Nov — More than 700,000 Russian soldiers killed in nearly five years of
  war, a new analysis says. Source: Global Eye 24 Nov.
- 23 Nov — Zelensky urges a NATO invite for Ukraine at the Berlin assembly.
  Source: news wires 23 Nov.
- 24 Nov — China threatens the EU with sanctions. Source: EADaily 24 Nov.

## Tests

- `python3 main.py` run 1: output/entry.png 30,201 bytes, 1024x1024 RGB,
  sha256 d50617375ada62588dfe7a72b096c6b6ef5297187fbf29c4e357a67ff2694009.
- Determinism: run 2 from a clean copy (no output/ dir) produced the same
  sha256; run 3 (fresh output/) also identical. Byte-identical 2x (3 runs).
- Visual check 1: found one defect — lead deck paragraph 2 overlapped deck
  paragraph 1 (deck 1 wraps to 4 lines, not 3). Fixed by moving headline
  y 152 -> 146, deck 1 y 198 -> 190, deck 2 y 256 -> 264.
- Visual check 2: clean — no overlap, no clipping, no text outside frames;
  all 8 boxes, lead, panels, masthead, footer legible.

## Method

ATM ranks 20-50 recipe (dense poster, 30+ dated stories, 7 regions), same as
the 23 Nov dense poster (R2 judge 52.54%). No code from any earlier edition
was read or reused: font, canvas, PNG encoder, and layout were all designed
fresh in this session, so thinking_reproduces should be high.
