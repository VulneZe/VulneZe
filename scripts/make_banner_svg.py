#!/usr/bin/env python3
"""Bannière d'en-tête animée : nom, rôle, ligne de commande tapée, pastilles de domaines
et un petit réseau vivant (paquets qui circulent, nœuds qui pulsent, bouclier central).

Usage : python scripts/make_banner_svg.py  ->  banner.svg
"""
import math

from theme import (ACCENT, ACCENT2, ACCENT_DEEP, BG, BORDER, DIM, MONO, SANS, TEXT, esc,
                   panel, svg_open, text_w)

OUT = "banner.svg"
W, H = 860, 240

CHIPS = ["NIS2", "ISO 27001", "Zero Trust", "SIEM / XDR", "Infra as Code"]
CMD = "defense-in-depth --zero-trust --detect --respond"

CENTER = (706, 120)
NODES = [  # x, y, étiquette, dx, dy
    (612, 52, "EDR", 0, -12), (680, 26, "SIEM", 0, -12), (782, 46, "IAM", 0, -12),
    (826, 112, "ZTNA", -2, 22), (792, 192, "NGFW", 0, 22), (706, 210, "VPN", 0, 22),
    (616, 176, "PKI", 0, 22), (572, 112, "IaC", 0, -12),
]


def main():
    o = [svg_open(W, H, "Baptiste Rouault — RSSI adjoint et architecte réseaux et cybersécurité")]
    o.append("<style>"
             ".u{opacity:0;animation:up .7s cubic-bezier(.2,.8,.2,1) forwards}"
             "@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
             "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
             ".caret{animation:blink 1s steps(1) infinite}"
             "</style>")
    o.append("<defs>"
             f'<radialGradient id="g" cx="0.82" cy="0.5" r="0.55"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.20"/>'
             f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT2}"/></linearGradient>'
             "</defs>")
    o.append(panel(W, H))
    o.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="11" fill="url(#g)"/>')

    # trame de points
    o.append(f'<g fill="{BORDER}">')
    for gy in range(20, H, 26):
        for gx in range(20, W, 26):
            o.append(f'<circle cx="{gx}" cy="{gy}" r="0.9"/>')
    o.append("</g>")

    # --- texte -----------------------------------------------------------
    x = 40
    o.append(f'<text class="u" style="animation-delay:.1s" x="{x}" y="54" font-family="{MONO}" font-size="11" '
             f'letter-spacing="2.4" fill="{ACCENT}">CYBERSÉCURITÉ · RÉSEAUX · ARCHITECTURE</text>')
    o.append(f'<text class="u" style="animation-delay:.25s" x="{x}" y="104" font-family="{SANS}" font-size="46" '
             f'font-weight="800" letter-spacing="-1" fill="{TEXT}">Baptiste Rouault</text>')
    o.append(f'<rect x="{x}" y="117" width="0" height="3" rx="1.5" fill="url(#bar)">'
             f'<animate attributeName="width" from="0" to="132" begin=".6s" dur=".8s" fill="freeze" calcMode="spline" '
             f'keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>')
    o.append(f'<text class="u" style="animation-delay:.5s" x="{x}" y="150" font-family="{SANS}" font-size="19" '
             f'fill="{TEXT}" fill-opacity=".88">RSSI adjoint &amp; Architecte réseaux et cybersécurité</text>')

    # ligne de commande tapée caractère par caractère
    cw = 13 * 0.6
    ty = 182
    t0 = 1.3
    n = len(CMD)
    dur = n * 0.045
    vals = ";".join(f"{i * cw:.1f}" for i in range(n + 1))
    o.append(f'<defs><clipPath id="typed"><rect x="{x + 16}" y="{ty - 14}" width="0" height="20">'
             f'<animate attributeName="width" values="{vals}" calcMode="discrete" begin="{t0}s" dur="{dur:.2f}s" fill="freeze"/>'
             f'</rect></clipPath></defs>')
    o.append(f'<g font-family="{MONO}" font-size="13"><text class="u" style="animation-delay:1.0s" x="{x}" y="{ty}" fill="{ACCENT}">$</text>'
             f'<text clip-path="url(#typed)" x="{x + 16}" y="{ty}" fill="{TEXT}">{esc(CMD)}</text>'
             f'<rect class="caret" x="{x + 16 + n * cw + 2:.1f}" y="{ty - 12}" width="7" height="15" fill="{ACCENT}" opacity="0">'
             f'<animate attributeName="opacity" from="0" to="1" begin="{t0 + dur:.2f}s" dur="0.01s" fill="freeze"/></rect></g>')

    # pastilles
    cx, cy = x, 204
    for i, label in enumerate(CHIPS):
        w = text_w(label, 11, mono=True) + 22
        d = 2.2 + i * 0.14
        o.append(f'<g class="u" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{cx}" y="{cy}" width="{w:.0f}" height="24" rx="12" fill="{ACCENT}" fill-opacity=".09" stroke="{ACCENT_DEEP}"/>'
                 f'<text x="{cx + w / 2:.0f}" y="{cy + 16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{ACCENT2}">{esc(label)}</text></g>')
        cx += w + 8
    assert cx < 560, "pastilles trop larges"

    # --- réseau vivant ---------------------------------------------------
    c = CENTER
    o.append(f'<g stroke="{ACCENT_DEEP}" stroke-width="1" fill="none" opacity=".55">')
    for i, (nx, ny, *_r) in enumerate(NODES):
        o.append(f'<line x1="{c[0]}" y1="{c[1]}" x2="{nx}" y2="{ny}"/>')
        mx, my, *_ = NODES[(i + 1) % len(NODES)]
        o.append(f'<line x1="{nx}" y1="{ny}" x2="{mx}" y2="{my}" stroke-dasharray="2 4" opacity=".6"/>')
    o.append("</g>")

    # paquets : sortants (trafic) et entrants (alertes)
    for i, (nx, ny, *_r) in enumerate(NODES):
        inbound = i % 2 == 0
        path = f"M{nx} {ny} L{c[0]} {c[1]}" if inbound else f"M{c[0]} {c[1]} L{nx} {ny}"
        col = ACCENT2 if inbound else ACCENT
        o.append(f'<circle r="2.6" fill="{col}" opacity="0">'
                 f'<animateMotion dur="{2.4 + (i % 3) * 0.6:.1f}s" begin="{1.0 + i * 0.35:.2f}s" repeatCount="indefinite" path="{path}"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{2.4 + (i % 3) * 0.6:.1f}s" '
                 f'begin="{1.0 + i * 0.35:.2f}s" repeatCount="indefinite"/></circle>')

    # nœuds + halos qui pulsent + étiquettes
    for i, (nx, ny, label, dx, dy) in enumerate(NODES):
        o.append(f'<circle cx="{nx}" cy="{ny}" r="6" fill="none" stroke="{ACCENT}" opacity="0">'
                 f'<animate attributeName="r" values="5;14" dur="3s" begin="{0.8 + i * 0.37:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".6;0" dur="3s" begin="{0.8 + i * 0.37:.2f}s" repeatCount="indefinite"/></circle>')
        o.append(f'<circle class="u" style="animation-delay:{0.5 + i * 0.1:.2f}s" cx="{nx}" cy="{ny}" r="5" fill="{BG}" stroke="{ACCENT}" stroke-width="1.6"/>')
        o.append(f'<text class="u" style="animation-delay:{0.7 + i * 0.1:.2f}s" x="{nx + dx}" y="{ny + dy}" text-anchor="middle" '
                 f'font-family="{MONO}" font-size="9" letter-spacing="1" fill="{DIM}">{label}</text>')

    # noyau : anneaux + bouclier
    cxn, cyn = c
    o.append(f'<circle cx="{cxn}" cy="{cyn}" r="34" fill="none" stroke="{ACCENT}" stroke-width="1" stroke-dasharray="3 7" opacity=".7">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cxn} {cyn}" to="360 {cxn} {cyn}" dur="22s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="{cxn}" cy="{cyn}" r="24" fill="{BG}" stroke="{ACCENT}" stroke-width="1.6"/>')
    o.append(f'<circle cx="{cxn}" cy="{cyn}" r="24" fill="none" stroke="{ACCENT2}" opacity="0">'
             f'<animate attributeName="r" values="24;42" dur="3.2s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".55;0" dur="3.2s" repeatCount="indefinite"/></circle>')
    o.append(f'<path d="M{cxn} {cyn - 13} l11 4.2 v8.4 c0 7.6 -5 12.8 -11 15.4 c-6 -2.6 -11 -7.8 -11 -15.4 v-8.4 z" '
             f'fill="{ACCENT}" fill-opacity=".14" stroke="{ACCENT}" stroke-width="1.6" stroke-linejoin="round"/>')
    o.append(f'<path d="M{cxn - 5} {cyn + 1} l4 4 l7.5 -8.5" fill="none" stroke="{ACCENT2}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
             f'stroke-dasharray="22" stroke-dashoffset="22"><animate attributeName="stroke-dashoffset" from="22" to="0" begin="1.2s" dur=".6s" fill="freeze"/></path>')

    o.append("</svg>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print(f"OK -> {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
