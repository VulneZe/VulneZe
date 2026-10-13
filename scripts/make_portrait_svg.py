#!/usr/bin/env python3
"""Portrait en points (halftone) teal, façon console de supervision.

Les points apparaissent ligne par ligne, balayés par un faisceau de scan ; ensuite
un faisceau discret continue de repasser en boucle. Cadre HUD, repères d'angle et
légende animée.

Usage : python scripts/make_portrait_svg.py  ->  portrait.svg
Pré-requis : python scripts/prep_photo.py source-photo.png
"""
import cv2
import numpy as np

from theme import (ACCENT, ACCENT2, ACCENT_DEEP, DIM, INK, MONO, SANS, TEXT, TINT, TINT2,
                   esc, header, lerp_hex, panel, svg_open)

OUT = "portrait.svg"
W, H = 400, 482
COLS = 84
PITCH = 4.286
GX = (W - COLS * PITCH) / 2          # marge gauche de la grille
GY = 50                              # haut de la grille
GRID = COLS * PITCH


def load_grid():
    # luminance d'origine + CLAHE doux (le gris très contrasté de prep_photo écrase le visage)
    gray = cv2.cvtColor(cv2.imread("source-photo.png"), cv2.COLOR_BGR2GRAY)
    gray = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(6, 6)).apply(gray)
    gray = cv2.GaussianBlur(gray, (0, 0), 2.2)
    mask = cv2.imread("source-mask.png", cv2.IMREAD_GRAYSCALE)
    h, w = gray.shape
    box = (slice(int(h * 0.08), h), slice(int(w * 0.04), int(w * 0.96)))
    gray, mask = gray[box], mask[box]
    gh, gw = gray.shape
    rows = int(round(COLS * gh / gw))
    g = cv2.resize(gray, (COLS, rows), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    m = cv2.resize(mask, (COLS, rows), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    # normalisation sur le sujet + courbe douce : évite les hautes lumières « brûlées »
    subj = g[m > 0.5]
    lo, hi = np.percentile(subj, [1, 99.5])
    g = np.clip((g - lo) / max(hi - lo, 1e-3), 0, 1) ** 1.2
    return g, m


def dot_color(d):
    """d = obscurité (0 = clair, 1 = foncé) : halftone encre sur papier."""
    return lerp_hex(TINT2, INK, d ** 1.1)


def main():
    g, m = load_grid()
    rows = g.shape[0]
    grid_h = rows * PITCH
    total = 3.0                        # durée du premier balayage (s)
    t0 = 0.35

    o = [svg_open(W, H, "Portrait de Baptiste Rouault en points, style console de supervision")]
    o.append("<style>.r{opacity:0;animation:rv .55s ease-out forwards}"
             "@keyframes rv{from{opacity:0}to{opacity:1}}"
             ".fade{opacity:0;animation:rv .8s ease-out forwards}"
             "@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}"
             ".p{animation:pulse 1.8s ease-in-out infinite}</style>")
    o.append("<defs>"
             f'<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{ACCENT2}" stop-opacity="0"/>'
             f'<stop offset="0.85" stop-color="{ACCENT2}" stop-opacity="0.35"/>'
             f'<stop offset="1" stop-color="{ACCENT2}" stop-opacity="0.8"/></linearGradient>'
             f'<radialGradient id="glow" cx="0.5" cy="0.42" r="0.6">'
             f'<stop offset="0" stop-color="{TINT}"/>'
             f'<stop offset="1" stop-color="{TINT}" stop-opacity="0"/></radialGradient>'
             "</defs>")
    o.append(panel(W, H))
    o.append(f'<rect x="1" y="41" width="{W - 2}" height="{H - 42}" rx="13" fill="url(#glow)"/>')
    o.append(header(W, "Identité"))

    # trame de fond discrète
    o.append(f'<g fill="{TINT2}">')
    for gy in range(int(GY), int(GY + grid_h) + 1, 32):
        for gx in range(int(GX), int(GX + GRID) + 1, 32):
            o.append(f'<circle cx="{gx}" cy="{gy}" r="0.9"/>')
    o.append("</g>")

    # points du portrait, groupés par ligne (un délai par ligne)
    for r in range(rows):
        dots = []
        for c in range(COLS):
            if m[r, c] < 0.4:
                continue
            d = 1.0 - float(g[r, c])
            rad = PITCH * 0.5 * (0.12 + 0.88 * d ** 1.05)
            if rad < 0.4:
                continue
            dots.append(f'<circle cx="{GX + (c + 0.5) * PITCH:.1f}" cy="{GY + (r + 0.5) * PITCH:.1f}" '
                        f'r="{rad:.2f}" fill="{dot_color(d)}"/>')
        if dots:
            delay = t0 + (r / rows) * total
            o.append(f'<g class="r" style="animation-delay:{delay:.2f}s">{"".join(dots)}</g>')

    # faisceau d'apparition (une fois), puis balayage lent en boucle
    o.append(f'<rect x="{GX - 6:.1f}" y="{GY - 26}" width="{GRID + 12:.1f}" height="26" fill="url(#beam)" opacity="0">'
             f'<animate attributeName="y" from="{GY - 26}" to="{GY + grid_h - 8:.1f}" begin="{t0}s" dur="{total}s" fill="freeze"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.04;0.94;1" begin="{t0}s" dur="{total}s" fill="freeze"/></rect>')
    o.append(f'<rect x="{GX - 6:.1f}" y="{GY - 20}" width="{GRID + 12:.1f}" height="20" fill="url(#beam)" opacity="0">'
             f'<animate attributeName="y" values="{GY - 20};{GY + grid_h - 6:.1f};{GY + grid_h - 6:.1f}" keyTimes="0;0.55;1" '
             f'dur="9s" begin="{t0 + total + 1.5:.2f}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;0.35;0.35;0;0" keyTimes="0;0.05;0.5;0.56;1" '
             f'dur="9s" begin="{t0 + total + 1.5:.2f}s" repeatCount="indefinite"/></rect>')

    # repères d'angle (HUD)
    L, T, R, B = GX - 10, GY - 8, GX + GRID + 10, GY + grid_h + 8
    k = 16
    o.append(f'<g fill="none" stroke="{ACCENT2}" stroke-width="1.6" stroke-linecap="round" class="fade" style="animation-delay:.2s">'
             f'<path d="M{L} {T + k}V{T}H{L + k}"/><path d="M{R - k} {T}H{R}V{T + k}"/>'
             f'<path d="M{L} {B - k}V{B}H{L + k}"/><path d="M{R - k} {B}H{R}V{B - k}"/></g>')
    o.append(f'<g font-family="{MONO}" font-size="9" fill="{ACCENT_DEEP}" class="fade" style="animation-delay:.6s" letter-spacing="1.2">'
             f'<text x="{L + 6}" y="{T + 14}">ID // B.ROUAULT</text>'
             f'<text x="{R - 6}" y="{T + 14}" text-anchor="end">SEC-OPS</text></g>')

    # légende
    y0 = B + 30
    o.append(f'<g class="fade" style="animation-delay:{t0 + total * 0.6:.2f}s">'
             f'<text x="{GX}" y="{y0}" font-family="{SANS}" font-size="19" font-weight="800" fill="{TEXT}">Baptiste Rouault</text>'
             f'<text x="{GX}" y="{y0 + 18}" font-family="{SANS}" font-size="10.5" fill="{DIM}">RSSI adjoint · Architecte réseaux &amp; cybersécurité</text>'
             f'<circle class="p" cx="{R - 62}" cy="{y0 - 6}" r="3.2" fill="{ACCENT2}"/>'
             f'<text x="{R - 54}" y="{y0 - 2.5}" font-family="{SANS}" font-size="10" font-weight="700" fill="{ACCENT_DEEP}">vulneze</text></g>')
    o.append("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print(f"OK -> {OUT} ({W}x{H}, {rows} lignes de points)")
    assert y0 + 18 < H - 8, "légende hors cadre"


if __name__ == "__main__":
    main()
