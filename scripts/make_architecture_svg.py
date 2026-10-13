#!/usr/bin/env python3
"""Schéma d'architecture animé : plan de trafic (accès -> identité -> périmètre -> zones
segmentées) et plan de télémétrie (agents -> SIEM/XDR -> détection & réponse), le tout
encadré par la gouvernance (SMSI, NIS2, ISO 27001).

Des paquets circulent en continu sur les liens : bleu-vert = trafic, ambre = logs/alertes.

Usage : python scripts/make_architecture_svg.py  ->  architecture.svg
"""
from theme import (ACCENT, ACCENT2, ACCENT_DEEP, BG2, BORDER, DIM, MONO, SANS, TEXT, WARN,
                   esc, header, panel, svg_open, text_w, TINT)

OUT = "architecture.svg"
W, H = 860, 372

BW, BH = 160, 74            # taille des blocs
TOP_Y, BOT_Y = 76, 226
X1, X2, X3, X4 = 24, 214, 404, 594

warnings = []


def box(x, y, w, h, title, sub, delay, accent=ACCENT):
    for s, size, mono, label in ((title, 13, False, "titre"), (sub, 9.5, True, "sous-titre")):
        if text_w(s, size, mono) > w - 24:
            warnings.append(f"{label} trop long ({s!r}: {text_w(s, size, mono):.0f} > {w - 24})")
    return (f'<g class="u" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BG2}" stroke="{BORDER}"/>'
            f'<rect x="{x}" y="{y + 14}" width="3" height="{h - 28}" rx="1.5" fill="{accent}"/>'
            f'<text x="{x + 14}" y="{y + 30}" font-family="{SANS}" font-size="13" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
            f'<text x="{x + 14}" y="{y + 50}" font-family="{MONO}" font-size="9.5" fill="{DIM}">{esc(sub)}</text></g>')


def packets(path, color, n, dur, begin0, r=2.7):
    out = []
    for i in range(n):
        b = begin0 + i * dur / n
        out.append(f'<circle r="{r}" fill="{color}" opacity="0">'
                   f'<animateMotion path="{path}" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.06;.94;1" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def arrow(x1, y1, x2, y2, color, dashed=False):
    d = ' stroke-dasharray="3 4"' if dashed else ""
    ang = (x2 - x1, y2 - y1)
    # pointe de flèche simple, orientée horizontalement ou verticalement
    if abs(ang[0]) >= abs(ang[1]):
        s = 1 if ang[0] > 0 else -1
        head = f'M{x2 - 6 * s} {y2 - 4}L{x2} {y2}L{x2 - 6 * s} {y2 + 4}'
    else:
        s = 1 if ang[1] > 0 else -1
        head = f'M{x2 - 4} {y2 - 6 * s}L{x2} {y2}L{x2 + 4} {y2 - 6 * s}'
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.4"{d}/>'
            f'<path d="{head}" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')


def main():
    o = [svg_open(W, H, "Architecture de sécurité : accès, identité, périmètre, zones segmentées, télémétrie, SIEM/XDR et gouvernance")]
    o.append("<style>.u{opacity:0;animation:up .6s cubic-bezier(.2,.8,.2,1) forwards}"
             "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>")
    o.append(panel(W, H))
    o.append(header(W, "Architecture de sécurité"))

    ty_mid = TOP_Y + BH // 2
    by_mid = BOT_Y + BH // 2

    # étiquettes de plans
    o.append(f'<g font-family="{SANS}" font-size="9" font-weight="700" letter-spacing="1.8" fill="{ACCENT_DEEP}">'
             f'<text class="u" style="animation-delay:.1s" x="{X1}" y="{TOP_Y - 10}">PLAN DE TRAFIC</text></g>'
             f'<g font-family="{SANS}" font-size="9" font-weight="700" letter-spacing="1.8" fill="{WARN}">'
             f'<text class="u" style="animation-delay:.1s" x="{X1 + 104}" y="{BOT_Y - 10}">PLAN DE TÉLÉMÉTRIE</text></g>')

    # liens (dessinés avant les blocs pour que les paquets « sortent » des blocs)
    o.append("<g>")
    for xa, xb in ((X1 + BW, X2), (X2 + BW, X3), (X3 + BW, X4)):
        o.append(arrow(xa, ty_mid, xb, ty_mid, ACCENT2))
    for xa, xb in ((X1 + BW, X2), (X2 + 350, X4)):
        o.append(arrow(xa, by_mid, xb, by_mid, WARN))
    # télémétrie descendante : chaque brique du haut alimente le plan du bas
    for xc, tgt in ((X1 + BW // 2, X1 + BW // 2), (X2 + BW // 2, X2 + BW // 2),
                    (X3 + BW // 2, X3 + BW // 2 + 20), (X4 + 121, X4 + 121)):
        o.append(arrow(xc, TOP_Y + BH, tgt, BOT_Y, WARN, dashed=True))
    o.append("</g>")

    # paquets : trafic de gauche à droite, logs vers le bas, alertes vers la réponse
    o.append(packets(f"M{X1 + BW - 4} {ty_mid} H{X2 + 4}", ACCENT2, 2, 2.6, 1.6))
    o.append(packets(f"M{X2 + BW - 4} {ty_mid} H{X3 + 4}", ACCENT2, 2, 2.6, 2.1))
    o.append(packets(f"M{X3 + BW - 4} {ty_mid} H{X4 + 4}", ACCENT2, 2, 2.6, 2.6))
    for xc, tgt in ((X1 + BW // 2, X1 + BW // 2), (X2 + BW // 2, X2 + BW // 2),
                    (X3 + BW // 2, X3 + BW // 2 + 20), (X4 + 121, X4 + 121)):
        o.append(packets(f"M{xc} {TOP_Y + BH} L{tgt} {BOT_Y}", WARN, 2, 2.4, 3.0 + (xc % 7) * 0.1))
    o.append(packets(f"M{X1 + BW - 4} {by_mid} H{X2 + 4}", WARN, 2, 2.4, 3.4))
    o.append(packets(f"M{X2 + 346} {by_mid} H{X4 + 4}", WARN, 2, 2.4, 3.9))

    # blocs — plan de trafic
    o.append(box(X1, TOP_Y, BW, BH, "Accès utilisateurs", "Windows · Linux · M365", 0.3))
    o.append(box(X2, TOP_Y, BW, BH, "Identité & accès", "AD · MFA · RADIUS · PKI", 0.45))
    o.append(box(X3, TOP_Y, BW, BH, "Périmètre · ZTNA", "Fortinet · pfSense", 0.6))

    # zones segmentées (micro-segmentation)
    zw = 242
    o.append(f'<g class="u" style="animation-delay:.75s">'
             f'<rect x="{X4}" y="{TOP_Y}" width="{zw}" height="{BH}" rx="10" fill="{BG2}" stroke="{BORDER}"/>'
             f'<text x="{X4 + 12}" y="{TOP_Y + 14}" font-family="{MONO}" font-size="8.5" letter-spacing="1.4" fill="{DIM}">ZONES MICRO-SEGMENTÉES</text>')
    zones = [("Serveurs", "Proxmox · VMware · Hyper-V"), ("Cloud", "Azure · AWS"), ("CI/CD", "Jenkins · Gitea · Docker")]
    for i, (n, d) in enumerate(zones):
        zy = TOP_Y + 21 + i * 17.5
        o.append(f'<rect x="{X4 + 10}" y="{zy:.1f}" width="{zw - 20}" height="15" rx="4" fill="{ACCENT}" fill-opacity=".08" stroke="{ACCENT_DEEP}" stroke-width=".8"/>'
                 f'<text x="{X4 + 18}" y="{zy + 10.5:.1f}" font-family="{SANS}" font-size="9.5" font-weight="700" fill="{ACCENT_DEEP}">{n}</text>'
                 f'<text x="{X4 + 70}" y="{zy + 10.5:.1f}" font-family="{SANS}" font-size="9.5" fill="{DIM}">{esc(d)}</text>')
        if text_w(d, 9.5, True) > zw - 90:
            warnings.append(f"zone trop longue: {d}")
    o.append("</g>")

    # blocs — plan de télémétrie
    o.append(box(X1, BOT_Y, BW, BH, "Agents EDR", "Wazuh · Bitdefender", 0.9, WARN))
    o.append(box(X2, BOT_Y, 350, BH, "SIEM / XDR on-premise", "collecte · corrélation · tableaux de bord", 1.05, WARN))
    o.append(box(X4, BOT_Y, zw, BH, "Détection & réponse", "alertes · investigation · remédiation", 1.2, WARN))

    # gouvernance
    gy = BOT_Y + BH + 24
    o.append(f'<g class="u" style="animation-delay:1.4s">'
             f'<rect x="{X1}" y="{gy}" width="{W - 2 * X1}" height="32" rx="9" fill="{TINT}" stroke="{ACCENT2}" stroke-dasharray="5 5"/>'
             f'<text x="{X1 + 14}" y="{gy + 20}" font-family="{SANS}" font-size="9" font-weight="700" letter-spacing="1.8" fill="{ACCENT_DEEP}">GOUVERNANCE</text>'
             f'<text x="{X1 + 120}" y="{gy + 20}" font-family="{SANS}" font-size="10.5" fill="{TEXT}" fill-opacity=".85">'
             f'SMSI · NIS2 · ISO 27001 · gestion des vulnérabilités · audits · sauvegardes</text></g>')
    assert gy + 32 + 12 <= H, "gouvernance hors cadre"

    o.append("</svg>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print(f"OK -> {OUT} ({W}x{H})")
    for w_ in warnings:
        print("[warn]", w_)


if __name__ == "__main__":
    main()
