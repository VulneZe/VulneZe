#!/usr/bin/env python3
"""Carte « neofetch » : le profil en clair — rôle, périmètre, ce qui a été livré.
Les lignes apparaissent une à une à côté du portrait.

Usage : python scripts/make_info_card.py   ->  info-card.svg
        STATIC=1 python scripts/make_info_card.py   (image figée pour prévisualiser)
"""
import os
import textwrap

from theme import (ACCENT, ACCENT2, ACCENT_DEEP, BORDER, DIM, MONO, TEXT, esc, panel,
                   svg_open, window_chrome)

OUT = "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

W, H = 460, 482                 # même hauteur que le portrait (400 + 460 = 860)
FONT = 12.5
CW = FONT * 0.6
LH = 18.0
X0 = 24
KEY_W = 12
WRAP = 40

FIELDS = [
    ("Rôle", "RSSI adjoint · Architecte réseaux & cybersécurité"),
    ("Focus", "Défense en profondeur · Zero Trust · détection & réponse"),
    ("En cours", "SMSI & conformité NIS2 / ISO 27001 · XDR-EDR-SIEM on-premise · architecture réseau"),
    ("Livré", "Déploiement Wazuh & Bitdefender · migration VPN → ZTNA · micro-segmentation · durcissement Windows / Linux, AD, GPO"),
    ("Échelle", "parc de 600 utilisateurs"),
    ("Détection", "Wazuh · Bitdefender · Sentinel · Tehtris"),
    ("Périmètre", "Fortinet · pfSense · WAF · VLAN / VPN"),
    ("Automation", "Ansible · Jenkins · Docker · PowerShell · Bash"),
]

PALETTE = [BORDER, ACCENT_DEEP, ACCENT, ACCENT2, TEXT, "#ff5f57", "#febc2e", DIM]


def main():
    lines = []
    for key, val in FIELDS:
        parts = textwrap.wrap(val, WRAP, break_on_hyphens=False)
        for i, p in enumerate(parts):
            lines.append((key if i == 0 else None, p))

    def a(d):
        return "" if STATIC else f' class="l" style="animation-delay:{d:.2f}s"'

    y, delay, step = 68, 0.3, 0.12
    body = [f'<text x="{X0}" y="{y}"{a(delay)} font-size="{FONT + 3}" font-weight="700">'
            f'<tspan fill="{ACCENT}">vulneze</tspan><tspan fill="{DIM}">@</tspan><tspan fill="{ACCENT}">github</tspan></text>']
    y += LH
    delay += step
    body.append(f'<text x="{X0}" y="{y}"{a(delay)} fill="{DIM}">{"─" * 36}</text>')
    y += LH * 1.2
    delay += step

    prev_key = None
    for key, text in lines:
        if key and prev_key is not None:
            y += 5                       # respiration entre deux champs
        if key:
            prev_key = key
        k = f'<tspan fill="{ACCENT}" font-weight="700">{esc(key)}</tspan>' if key else ""
        body.append(f'<text x="{X0}" y="{y:.1f}"{a(delay)}>{k}</text>')
        body.append(f'<text x="{X0 + KEY_W * CW:.1f}" y="{y:.1f}"{a(delay)} fill="{TEXT}">{esc(text)}</text>')
        y += LH
        delay += step

    y += 10
    for i, c in enumerate(PALETTE):
        body.append(f'<rect x="{X0 + i * 26}" y="{y:.1f}" width="22" height="12" rx="3" fill="{c}"{a(delay + i * 0.05)}/>')
    y += 12
    assert y + 20 < H, f"contenu trop long pour la carte ({y:.0f} > {H})"

    css = "" if STATIC else (
        "<style>.l{opacity:0;animation:in .45s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}</style>")
    svg = [svg_open(W, H, "Carte de profil de Baptiste Rouault : rôle, périmètre, réalisations"), css,
           panel(W, H), window_chrome(W, "neofetch"),
           f'<g font-family="{MONO}" font-size="{FONT}" xml:space="preserve">', *body, "</g>", "</svg>"]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"OK -> {OUT} ({W}x{H}, {len(lines)} lignes, fin du contenu y={y:.0f})")


if __name__ == "__main__":
    main()
