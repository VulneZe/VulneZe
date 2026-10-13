#!/usr/bin/env python3
"""Section « Projets » : les dépôts mis en avant, sous forme de cartes
qui apparaissent en cascade avec un accent teal animé.

Usage : python scripts/make_projects_svg.py  ->  projects.svg
"""
from theme import (ACCENT, ACCENT2, ACCENT_DEEP, BG2, BORDER, DIM, SANS, TEXT, TINT,
                   esc, header, icon_atlos, panel, svg_open, text_w)

OUT = "projects.svg"
W = 860
MARGIN, GAP = 12, 12
COLS = 2
CW = (W - 2 * MARGIN - (COLS - 1) * GAP) / COLS
PAD = 16
TOP = 50
CARD_H = 128

# (nom, tagline, pile techno, icône)
PROJECTS = [
    ("Hydia", "Coffre-fort numérique zero-knowledge : secrets, documents, partage d'équipe.",
     ["TypeScript", "Fastify", "PostgreSQL", "E2EE"], "lock"),
    ("Lab Entreprise", "Maquette d'entreprise complète : routage, VPN, AD, PKI / AD CS, durcissement.",
     ["AD DS / AD CS", "PKI", "Routage & VPN", "GPO"], "share"),
    ("Infra as Code", "Infra sysadmin 100 % open source : provisionnement, sauvegarde, supervision.",
     ["Terraform", "Ansible", "Proxmox", "Backup"], "import"),
    ("NetRecon", "Cartographie réseau discrète : découverte passive, sans alerte côté AD.",
     ["Python", "Scan passif", "ARP / mDNS", "AD-aware"], "eye"),
    ("Detection Lab", "Chaîne de détection bout en bout : collecte, corrélation, réponse.",
     ["SIEM / XDR", "EDR", "IDS / IPS", "Sysmon"], "score"),
    ("CVEAtlos", "Veille et scoring de vulnérabilités orienté exploitation.",
     ["Next.js", "Rust"], "folder"),
]

LANG_COLORS = {
    "TypeScript": "#3178c6", "Rust": "#b7410e", "React": "#149eca",
    "Vite": "#8b5cf6", "Tailwind": "#38bdf8", "Fastify": "#181c22",
    "Supabase": "#3ecf8e", "Deno": "#181c22", "Next.js": "#181c22",
    "E2EE": ACCENT_DEEP, "Python": "#3572a5", "PostgreSQL": "#336791",
    "AD DS / AD CS": "#3178c6", "PKI": "#8b5cf6", "Routage & VPN": "#149eca",
    "GPO": "#3178c6", "Terraform": "#7b42bc", "Ansible": "#b7410e",
    "Proxmox": "#e57000", "Backup": "#38bdf8", "SIEM / XDR": "#3178c6",
    "EDR": "#b7410e", "IDS / IPS": "#8b5cf6", "Sysmon": "#149eca",
    "Scan passif": ACCENT_DEEP, "ARP / mDNS": "#38bdf8", "AD-aware": "#b7410e",
}


def chip_row(labels, x, y):
    out = []
    for lab in labels:
        w = text_w(lab, 10.5) + 18
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="20" rx="10" fill="{TINT}" stroke="#bfe0d8"/>'
            f'<circle cx="{x + 10:.1f}" cy="{y + 10}" r="3.5" fill="{LANG_COLORS.get(lab, ACCENT2)}"/>'
            f'<text x="{x + 18:.1f}" y="{y + 14}" font-family="{SANS}" font-size="10.5" fill="{TEXT}">{esc(lab)}</text>')
        x += w + 6
    return "".join(out)


def main():
    rows = (len(PROJECTS) + COLS - 1) // COLS
    H = int(TOP + rows * CARD_H + (rows - 1) * GAP + MARGIN + 6)

    o = [svg_open(W, H, "Projets mis en avant : Hydia, atlos.fr, CVEAtlos, back-office")]
    o.append("<style>.u{opacity:0;animation:up .55s cubic-bezier(.2,.8,.2,1) forwards}"
             "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
             ".bar{transform-origin:left;transform:scaleX(0);animation:bar 1s cubic-bezier(.2,.8,.2,1) forwards}"
             "@keyframes bar{to{transform:scaleX(1)}}"
             ".pulse{animation:pl 2.6s ease-in-out infinite}"
             "@keyframes pl{0%,100%{opacity:.35}50%{opacity:1}}</style>")
    o.append(panel(W, H))
    o.append(header(W, "Projets"))

    for i, (name, tag, chips, ic) in enumerate(PROJECTS):
        x = MARGIN + (i % COLS) * (CW + GAP)
        y = TOP + (i // COLS) * (CARD_H + GAP)
        d = 0.2 + i * 0.18
        o.append(f'<g class="u" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{x:.1f}" y="{y}" width="{CW:.1f}" height="{CARD_H}" rx="12" fill="{BG2}" stroke="{BORDER}"/>'
                 f'<rect class="bar" style="animation-delay:{d + 0.4:.2f}s" x="{x:.1f}" y="{y}" width="{CW:.1f}" height="3" rx="1.5" fill="{ACCENT2}"/>'
                 f'{icon_atlos(ic, x + PAD, y + 16, 30)}'
                 f'<text x="{x + PAD + 42:.1f}" y="{y + 34}" font-family="{SANS}" font-size="15" font-weight="800" fill="{TEXT}">{esc(name)}</text>'
                 f'<circle class="pulse" style="animation-delay:{d:.2f}s" cx="{x + CW - PAD - 6:.1f}" cy="{y + 24}" r="4" fill="{ACCENT2}"/>'
                 f'<text x="{x + PAD:.1f}" y="{y + 70}" font-family="{SANS}" font-size="11.5" fill="{DIM}">{esc(tag)}</text>'
                 f'{chip_row(chips, x + PAD, y + CARD_H - PAD - 20)}'
                 f'</g>')
    o.append("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print(f"OK -> {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
