#!/usr/bin/env python3
"""Carte d'info façon `neofetch` : titre, lignes clé/valeur colorées qui apparaissent
une à une à côté du portrait.

Usage : python scripts/make_info_card.py   ->  info-card.svg
        STATIC=1 python scripts/make_info_card.py   (image figée pour prévisualiser)
"""
import html
import os
import textwrap

OUT = "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

W = 490
MIN_H = 0              # hauteur = contenu
FONT = 12.5
CW = FONT * 0.6
LH = 18.0
X0 = 24
KEY_W = 15             # largeur de la colonne des clés (caractères)
WRAP = 44              # largeur max des valeurs (caractères)

BG, BAR, BORDER = "#0b1214", "#111b1e", "#1c2b2f"
ACCENT, KEY, VAL, DIM = "#2ebfa5", "#2ebfa5", "#d7ece8", "#6f8a88"

USER = "vulneze"

# (clé, valeur) — les valeurs longues sont repliées automatiquement
FIELDS = [
    ("Nom", "Baptiste Rouault"),
    ("Rôle", "RSSI adjoint · Architecte réseaux & cybersécurité"),
    ("Maintenant", "SMSI, conformité NIS2 / ISO 27001, XDR-EDR-SIEM on-premise (depuis fév. 2026)"),
    ("Avant", "Logisseo (2024-25) · LACROIX (2022-24) · SOC N1 Cooperl"),
    ("Défense", "Wazuh · Bitdefender · Tehtris · Sentinel · Defender · SIEM / XDR"),
    ("Réseau", "Fortinet · pfSense · VLAN / VPN · ZTNA · micro-segmentation"),
    ("Identité", "AD / GPO · IAM · MFA · PAM · RADIUS · PKI / Yubikey"),
    ("Infra", "Proxmox · VMware · Hyper-V · Azure & M365 · AWS · Kubernetes"),
    ("Automatisation", "Ansible · Jenkins · Docker · Gitea · PowerShell · Bash"),
    ("Certifs", "CEH (EC-Council) · AIS · Cisco Netacad Cybermenaces"),
    ("Formation", "Master SI & Cybersécurité (Diginamic-ANSSI) · ESAIP · BTS SIO"),
    ("Dispo", "à partir de septembre 2027"),
]

PALETTE = ["#1c2b2f", "#14705f", ACCENT, "#7be0cc", "#d7ece8", "#ff5f57", "#febc2e", "#6f8a88"]


def rows():
    """Aplatit FIELDS en lignes (clé|None, texte)."""
    out = []
    for key, val in FIELDS:
        parts = textwrap.wrap(val, WRAP) or [""]
        for i, p in enumerate(parts):
            out.append((key if i == 0 else None, p))
    return out


def main():
    lines = rows()
    y = 66
    body = []
    delay = 0.3
    step = 0.11

    def anim(d):
        return "" if STATIC else f' class="l" style="animation-delay:{d:.2f}s"'

    # En-tête user@host + séparateur
    body.append(f'<text x="{X0}" y="{y}"{anim(delay)} font-size="{FONT + 2}" font-weight="700">'
                f'<tspan fill="{ACCENT}">{USER}</tspan><tspan fill="{DIM}">@</tspan><tspan fill="{ACCENT}">github</tspan></text>')
    y += LH
    delay += step
    body.append(f'<text x="{X0}" y="{y}"{anim(delay)} fill="{DIM}">{"─" * 40}</text>')
    y += LH * 1.1
    delay += step

    for key, text in lines:
        k = ""
        if key:
            k = f'<tspan fill="{KEY}" font-weight="700">{html.escape(key)}</tspan>'
        pad_x = X0 + KEY_W * CW
        body.append(f'<text x="{X0}" y="{y:.1f}"{anim(delay)}>{k}</text>')
        body.append(f'<text x="{pad_x:.1f}" y="{y:.1f}"{anim(delay)} fill="{VAL}">{html.escape(text)}</text>')
        y += LH
        delay += step
        if key is not None and text == "":
            pass
        # petit espace entre les blocs
        nxt = None

    # barres de couleur façon neofetch
    y += LH * 0.6
    sw = 22
    for i, c in enumerate(PALETTE):
        body.append(f'<rect x="{X0 + i * (sw + 4)}" y="{y:.1f}" width="{sw}" height="12" rx="3" fill="{c}"{anim(delay + i * 0.05)}/>')
    y += 12

    H = max(MIN_H, int(y + 28))

    css = "" if STATIC else (
        "<style>.l{opacity:0;animation:in .45s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}</style>"
    )

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Carte d\'information de Baptiste Rouault (vulneze)">',
        css,
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M0.5 12.5a12 12 0 0 1 12-12h{W - 25}a12 12 0 0 1 12 12V34H0.5z" fill="{BAR}"/>',
        f'<line x1="0.5" y1="34" x2="{W - 0.5}" y2="34" stroke="{BORDER}"/>',
        '<circle cx="20" cy="17.5" r="5" fill="#ff5f57"/><circle cx="38" cy="17.5" r="5" fill="#febc2e"/>'
        f'<circle cx="56" cy="17.5" r="5" fill="{ACCENT}"/>',
        f'<text x="{W / 2:.0f}" y="21" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" fill="{DIM}">neofetch</text>',
        f'<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,&quot;DejaVu Sans Mono&quot;,monospace" font-size="{FONT}" xml:space="preserve">',
        *body,
        "</g>",
        "</svg>",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"OK -> {OUT} ({W}x{H}, {len(lines)} lignes)")


if __name__ == "__main__":
    main()
