#!/usr/bin/env python3
"""
Hand-authored neofetch-style info card SVG: a terminal window with a small
ASCII logo on the left and colored `key: value` rows on the right
(role, stack, lab, focus...), a dashed separator under the user@host line,
and a classic 8-color palette row at the bottom -- just like `neofetch`
output.

Each line fades and slides in on a short stagger so the panel looks like it
is printing next to the portrait, then freezes (CSS keyframes inside the SVG
-- GitHub runs those even though it strips JS).

Canvas is 840 x 880, identical to vulneze-ascii.svg, so the two panels line
up in the README's side-by-side table.

    python scripts/make_info_card.py [output.svg]
    STATIC=1 python scripts/make_info_card.py    # frozen frame for previews
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

W, H = 840, 880
PAD = 20
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
KEY = "#39d353"       # neofetch-style colored keys (green)
ACCENT = "#22d3ee"    # user@host + highlights
LOGO = "#ff7b72"      # small ascii logo color
DIM = "#484f58"

STATIC = bool(os.environ.get("STATIC"))  # emit frozen state for previews

# ---- reveal timing (one-shot) -------------------------------------------
LINE_STAGGER = 0.22
LINE_DUR = 0.5
LOGO_STAGGER = 0.06

# ---- content (edit me) ---------------------------------------------------
USER_HOST = ("vulneze", "github")
ROWS = [
    ("Role",      "Architecte Sécu & Réseaux · RSSI"),
    ("Focus",     "Pentest · AD · Réseaux"),
    ("Offensive", "Kali · Exegol · nmap · nxc"),
    ("Homelab",   "Proxmox · Docker · Tailscale"),
    ("Training",  "HackTheBox · TryHackMe"),
    ("Stack",     "Python · Bash · Git"),
    ("Shell",     "bash · zsh"),
    ("Location",  "France"),
]

# small ascii logo -- stylized terminal skull, neofetch-left-column style
LOGO_LINES = [
    "    .-\"\"\"\"\"\"\"-.",
    "   /  _   _   \\",
    "  |  (o) (o)  |",
    "  |     ^     |",
    "   \\  \\___/  /",
    "    '._____.'",
    "   /| ROOT  |\\",
    "      |  |",
]

PALETTE = ["#ff5f56", "#ffbd2e", "#27c93f", "#1f6feb",
           "#bc8cff", "#22d3ee", "#e6edf3", "#484f58"]
PALETTE_BRIGHT = ["#ff8a80", "#ffe082", "#69f0a0", "#79c0ff",
                  "#d2a8ff", "#76e3ea", "#ffffff", "#8b949e"]

css = f"""
@keyframes in {{
  0%   {{ opacity: 0; transform: translateX(-14px); }}
  100% {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes drop {{
  0%   {{ opacity: 0; transform: translateY(-8px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
.l {{ opacity: 0; animation: in {LINE_DUR}s ease-out both; }}
.g {{ opacity: 0; animation: drop .35s ease-out both; }}
@media (prefers-reduced-motion: reduce) {{
  .l, .g {{ opacity: 1 !important; transform: none !important; animation: none !important; }}
}}
""".strip()

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<style>{css}</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">vulneze@github: ~$ neofetch</text>')

# ---- layout ---------------------------------------------------------------
LOGO_X = PAD + 24
TEXT_X = LOGO_X + 220          # info column starts right of the logo
TOP = TITLEBAR_H + 50
LINE_H = 56
FS = 22

def delay(s):
    return "" if STATIC else f' style="animation-delay:{s:.2f}s"'

def cls(c):
    return "" if STATIC else f' class="{c}"'

# ascii logo drops in line by line
for i, line in enumerate(LOGO_LINES):
    y = TOP + i * 30
    parts.append(
        f'<text{cls("g")}{delay(0.2 + i * LOGO_STAGGER)} xml:space="preserve" '
        f'x="{LOGO_X}" y="{y}" fill="{LOGO}" font-size="22">{html.escape(line)}</text>'
    )

# user@host + dashed separator (neofetch header)
user, host = USER_HOST
t = 0.1
parts.append(
    f'<text{cls("l")}{delay(t)} x="{TEXT_X}" y="{TOP}" font-size="{FS+6}" font-weight="700">'
    f'<tspan fill="{KEY}">{user}</tspan><tspan fill="{MUTED}">@</tspan>'
    f'<tspan fill="{ACCENT}">{host}</tspan></text>'
)
t += LINE_STAGGER
dashes = "-" * (len(user) + 1 + len(host))
parts.append(
    f'<text{cls("l")}{delay(t)} x="{TEXT_X}" y="{TOP + LINE_H * 0.7:.0f}" '
    f'fill="{DIM}" font-size="{FS}">{dashes}</text>'
)

# key: value rows
row_y = TOP + LINE_H * 0.7 + 50
for i, (k, v) in enumerate(ROWS):
    t += LINE_STAGGER
    y = row_y + i * LINE_H
    parts.append(
        f'<text{cls("l")}{delay(t)} x="{TEXT_X}" y="{y}" font-size="{FS}">'
        f'<tspan fill="{KEY}" font-weight="700">{html.escape(k)}</tspan>'
        f'<tspan fill="{MUTED}">: </tspan>'
        f'<tspan fill="{INK}">{html.escape(v)}</tspan></text>'
    )

# ---- neofetch color palette blocks, two rows of 8 -------------------------
pal_y = row_y + len(ROWS) * LINE_H + 40
sq, gap = 34, 14
for r, colors in enumerate([PALETTE, PALETTE_BRIGHT]):
    for i, color in enumerate(colors):
        x = TEXT_X + i * (sq + gap)
        y = pal_y + r * (sq + 12)
        parts.append(f'<rect{cls("g")}{delay(t + 0.25 + (r * 8 + i) * 0.05)} '
                     f'x="{x}" y="{y}" width="{sq}" height="{sq}" rx="6" fill="{color}"/>')

# status bar: steady blinking cursor after a fake prompt
status_line_y = H - 50
parts.append(f'<line x1="0" y1="{status_line_y}" x2="{W}" y2="{status_line_y}" stroke="{FRAME}"/>')
prompt = "vulneze@github:~$ uptime --security"
parts.append(f'<text x="{PAD}" y="{status_line_y + 30}" fill="{MUTED}" font-size="18">'
             f'{html.escape(prompt)} <tspan fill="{ACCENT}">always-on</tspan></text>')
cursor_x = PAD + (len(prompt) + len(" always-on") + 1) * 18 * 0.6
parts.append(f'<rect x="{cursor_x:.1f}" y="{status_line_y + 14}" width="11" height="20" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
             f'dur="1s" repeatCount="indefinite"/></rect>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
