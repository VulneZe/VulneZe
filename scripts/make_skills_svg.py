#!/usr/bin/env python3
"""Grille de compétences techniques : 6 domaines, chacun avec ce qu'il couvre
(outils réellement utilisés) et une phrase d'intention. Les cartes puis les pastilles
apparaissent en cascade (une seule lecture).

Usage : python scripts/make_skills_svg.py  ->  skills.svg
"""
from theme import (ACCENT, ACCENT2, ACCENT_DEEP, BG2, BORDER, DIM, SANS, TEXT, TINT, esc,
                   header, icon_atlos, panel, svg_open, text_w)

OUT = "skills.svg"
W = 860
MARGIN, GAP = 12, 12
COLS = 3
CW = (W - 2 * MARGIN - (COLS - 1) * GAP) / COLS     # largeur d'une carte
PAD = 14
TOP = 50

DOMAINS = [
    ("Détection & réponse", "télémétrie · corrélation · enquête", "eye",
     ["SIEM", "XDR", "EDR", "IDS / IPS", "SOAR", "Sysmon", "Threat hunting",
      "Corrélation", "Forensics"]),
    ("Réseau & périmètre", "segmenter · filtrer · protéger", "share",
     ["NGFW", "WAF", "Proxy sécurisé", "IDS / IPS", "VLAN", "VPN", "Routage",
      "ZTNA / SASE", "Micro-segmentation", "NAC"]),
    ("Identités & accès", "qui accède à quoi, et comment", "key",
     ["Active Directory", "GPO", "IAM", "MFA", "PAM", "RADIUS", "IdP", "Samba AD",
      "PKI / X.509", "YubiKey", "MDM", "DLP"]),
    ("Cloud & systèmes", "héberger · durcir · sauvegarder", "cloud",
     ["Azure", "Microsoft 365", "AWS ECS Fargate", "ELB", "S3", "Proxmox", "VMware",
      "Hyper-V", "Windows", "Linux", "SAN / NAS"]),
    ("Automatisation & CI/CD", "industrialiser · reproduire", "import",
     ["Ansible", "Terraform", "Kubernetes", "Docker", "CI/CD", "PowerShell", "Bash",
      "Infra as Code", "GitOps"]),
    ("Gouvernance & conformité", "cadrer · mesurer · auditer", "shield",
     ["SMSI", "NIS2", "ISO 27001", "Gestion des vulnérabilités", "Audit", "Supervision",
      "Métrologie", "KPI sécurité", "Sensibilisation"]),
]


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
    o.append(header(W, "Compétences"))

    n = 0
    y = TOP
    for ri, row in enumerate(rows):
        for ci, (title, sub, ic, placed, _h) in enumerate(row):
            x = MARGIN + ci * (CW + GAP)
            d = 0.2 + (ri * COLS + ci) * 0.18
            o.append(f'<g class="u" style="animation-delay:{d:.2f}s">'
                     f'<rect x="{x:.1f}" y="{y}" width="{CW:.1f}" height="{row_h[ri]}" rx="10" fill="{BG2}" stroke="{BORDER}"/>'
                     f'<rect x="{x:.1f}" y="{y}" width="{CW:.1f}" height="2.5" rx="1.25" fill="{ACCENT2}" fill-opacity=".8"/>'
                     f'{icon_atlos(ic, x + PAD, y + 17, 26)}'
                     f'<text x="{x + PAD + 34:.1f}" y="{y + 30}" font-family="{SANS}" font-size="14" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
                     f'<text x="{x + PAD + 34:.1f}" y="{y + 46}" font-family="{SANS}" font-size="9.5" fill="{DIM}">{esc(sub)}</text></g>')
            for lab, cx, cy, w in placed:
                dd = d + 0.35 + n * 0.035
                n += 1
                o.append(f'<g class="u" style="animation-delay:{dd:.2f}s">'
                         f'<rect x="{x + PAD + cx:.1f}" y="{y + 62 + cy}" width="{w:.1f}" height="22" rx="11" fill="{TINT}" stroke="#bfe0d8"/>'
                         f'<text x="{x + PAD + cx + w / 2:.1f}" y="{y + 62 + cy + 15}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{TEXT}">{esc(lab)}</text></g>')
        y += row_h[ri] + GAP
    o.append("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print(f"OK -> {OUT} ({W}x{H}, cartes {CW:.0f}px)")


if __name__ == "__main__":
    main()
