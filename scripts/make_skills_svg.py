#!/usr/bin/env python3
"""Grille de compétences techniques : 6 domaines, chacun avec ce qu'il couvre
(outils réellement utilisés) et une phrase d'intention. Les cartes puis les pastilles
apparaissent en cascade (une seule lecture).

Usage : python scripts/make_skills_svg.py  ->  skills.svg
"""
from theme import (ACCENT, ACCENT2, ACCENT_DEEP, BG2, BORDER, DIM, MONO, SANS, TEXT, esc, panel,
                   svg_open, text_w, window_chrome)

OUT = "skills.svg"
W = 860
MARGIN, GAP = 12, 12
COLS = 3
CW = (W - 2 * MARGIN - (COLS - 1) * GAP) / COLS     # largeur d'une carte
PAD = 14
TOP = 50

DOMAINS = [
    ("Détection & réponse", "télémétrie · corrélation · enquête", "radar",
     ["Wazuh", "Bitdefender", "Microsoft Defender", "Sentinel", "Tehtris", "CrowdStrike",
      "Sysmon", "Event Viewer", "SIEM", "XDR / EDR"]),
    ("Réseau & périmètre", "segmenter · filtrer · protéger", "network",
     ["Fortinet", "pfSense", "NGFW", "WAF", "Proxy sécurisé", "IDS / IPS", "VLAN", "VPN",
      "Routage", "ZTNA / SASE", "Micro-segmentation"]),
    ("Identités & accès", "qui accède à quoi, et comment", "user",
     ["Active Directory", "GPO", "IAM", "MFA", "PAM", "RADIUS", "IdP", "Samba AD",
      "PKI / X.509", "YubiKey", "MDM", "DLP"]),
    ("Cloud & systèmes", "héberger · durcir · sauvegarder", "cloud",
     ["Azure", "Microsoft 365", "AWS ECS Fargate", "ELB", "S3", "Proxmox", "VMware",
      "Hyper-V", "Windows", "Linux", "SAN / NAS"]),
    ("Automatisation & CI/CD", "industrialiser · reproduire", "term",
     ["Ansible", "Kubernetes", "Docker", "Jenkins", "Gitea", "PowerShell", "Bash", "Infra as Code"]),
    ("Gouvernance & conformité", "cadrer · mesurer · auditer", "shield",
     ["SMSI", "NIS2", "ISO 27001", "Gestion des vulnérabilités", "Audit", "Supervision",
      "Centreon", "Grafana", "Sensibilisation"]),
]


def icon(kind, x, y):
    s = f'fill="none" stroke="{ACCENT}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "radar":
        return (f'<g transform="translate({x},{y})" {s}><circle r="9"/><circle r="4.5"/>'
                f'<path d="M0 0L7 -5" stroke="{ACCENT2}"/><circle r="1.4" fill="{ACCENT}"/></g>')
    if kind == "network":
        return (f'<g transform="translate({x},{y})" {s}><circle cx="0" cy="-7" r="2.6"/><circle cx="-8" cy="6" r="2.6"/>'
                f'<circle cx="8" cy="6" r="2.6"/><path d="M-1.5 -4.6L-6.5 3.6M1.5 -4.6L6.5 3.6M-5.4 6H5.4"/></g>')
    if kind == "user":
        return (f'<g transform="translate({x},{y})" {s}><circle cy="-4" r="4"/><path d="M-9 10c0-5 4-7.5 9-7.5s9 2.5 9 7.5"/></g>')
    if kind == "cloud":
        return (f'<g transform="translate({x + 3},{y})" {s}><path d="M-8 7a5 5 0 0 1 0-10 7 7 0 0 1 13.5-1.5A5 5 0 0 1 8 7z"/></g>')
    if kind == "term":
        return (f'<g transform="translate({x},{y})" {s}><rect x="-10" y="-8" width="20" height="16" rx="3"/>'
                f'<path d="M-5 -2l4 3-4 3M1 4h5"/></g>')
    return (f'<g transform="translate({x},{y})" {s}><path d="M0 -10l9 3.5v6c0 6-4 9.5-9 11.5-5-2-9-5.5-9-11.5v-6z"/>'
            f'<path d="M-4 1l3 3 6-6.5" stroke="{ACCENT2}"/></g>')


def layout_chips(labels, inner_w):
    """Place les pastilles ligne par ligne ; renvoie ([(label, x, y, w)], hauteur)."""
    out, x, y, h = [], 0.0, 0.0, 22
    for lab in labels:
        w = text_w(lab, 11) + 18
        if x + w > inner_w:
            x, y = 0.0, y + h + 6
        out.append((lab, x, y, w))
        x += w + 6
    return out, y + h


def main():
    laid = []
    for title, sub, ic, chips in DOMAINS:
        placed, ch = layout_chips(chips, CW - 2 * PAD)
        laid.append((title, sub, ic, placed, 62 + ch + PAD))

    rows = [laid[i:i + COLS] for i in range(0, len(laid), COLS)]
    row_h = [max(c[4] for c in r) for r in rows]
    H = int(TOP + sum(row_h) + GAP * (len(rows) - 1) + MARGIN + 6)

    o = [svg_open(W, H, "Compétences techniques par domaine : détection, réseau, identités, cloud, automatisation, gouvernance")]
    o.append("<style>.u{opacity:0;animation:up .55s cubic-bezier(.2,.8,.2,1) forwards}"
             "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>")
    o.append(panel(W, H))
    o.append(window_chrome(W, "vulneze@github: ~/skills"))

    n = 0
    y = TOP
    for ri, row in enumerate(rows):
        for ci, (title, sub, ic, placed, _h) in enumerate(row):
            x = MARGIN + ci * (CW + GAP)
            d = 0.2 + (ri * COLS + ci) * 0.18
            o.append(f'<g class="u" style="animation-delay:{d:.2f}s">'
                     f'<rect x="{x:.1f}" y="{y}" width="{CW:.1f}" height="{row_h[ri]}" rx="10" fill="{BG2}" stroke="{BORDER}"/>'
                     f'<rect x="{x:.1f}" y="{y}" width="{CW:.1f}" height="2.5" rx="1.25" fill="{ACCENT}" fill-opacity=".7"/>'
                     f'{icon(ic, x + PAD + 11, y + 29)}'
                     f'<text x="{x + PAD + 30:.1f}" y="{y + 28}" font-family="{SANS}" font-size="14" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
                     f'<text x="{x + PAD + 30:.1f}" y="{y + 44}" font-family="{MONO}" font-size="9.5" fill="{DIM}">{esc(sub)}</text></g>')
            for lab, cx, cy, w in placed:
                dd = d + 0.35 + n * 0.035
                n += 1
                o.append(f'<g class="u" style="animation-delay:{dd:.2f}s">'
                         f'<rect x="{x + PAD + cx:.1f}" y="{y + 62 + cy}" width="{w:.1f}" height="22" rx="11" fill="{ACCENT}" fill-opacity=".09" stroke="{ACCENT_DEEP}"/>'
                         f'<text x="{x + PAD + cx + w / 2:.1f}" y="{y + 62 + cy + 15}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{TEXT}">{esc(lab)}</text></g>')
        y += row_h[ri] + GAP
    o.append("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print(f"OK -> {OUT} ({W}x{H}, cartes {CW:.0f}px)")


if __name__ == "__main__":
    main()
