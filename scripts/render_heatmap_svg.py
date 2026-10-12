#!/usr/bin/env python3
"""Dessine data/contributions.json en calendrier 53 semaines x 7 jours.

Cases arrondies, palette menthe/teal, révélation diagonale (une seule lecture,
puis l'image se fige), légende Moins -> Plus et pied de page de statistiques.

Usage : python scripts/render_heatmap_svg.py  ->  contrib-heatmap.svg
"""
import datetime as dt
import json

SRC = "data/contributions.json"
OUT = "contrib-heatmap.svg"

W = 860                      # = 370 (portrait) + 490 (carte) dans le README
CELL, GAP = 11, 3
PITCH = CELL + GAP
LEFT = 44                    # place pour les étiquettes des jours
TOP = 78                     # barre de titre + étiquettes des mois

BG, BAR, BORDER = "#0b1214", "#111b1e", "#1c2b2f"
ACCENT, TEXT, DIM = "#2ebfa5", "#d7ece8", "#6f8a88"
PALETTE = ["#16231f", "#0f4f45", "#14705f", "#2ebfa5", "#7be0cc", "#c9fff3"]
MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
FONT = 'ui-monospace,SFMono-Regular,Menlo,Consolas,&quot;DejaVu Sans Mono&quot;,monospace'


def level_to_palette(level, count, max_count):
    """Niveaux GitHub 0-4 -> palette à 6 teintes (le 5e est le sommet 'néon')."""
    if level <= 0 and count <= 0:
        return 0
    if level >= 4 and max_count > 0 and count >= 0.85 * max_count:
        return 5
    return max(1, min(level, 4))


def fr_int(n):
    return f"{n:,}".replace(",", " ")


def main():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)
    days = data["days"]
    st = data["stats"]
    user = data.get("user", "vulneze")
    max_count = max((d["count"] for d in days), default=0)

    first = dt.date.fromisoformat(days[0]["date"])
    # on aligne sur le dimanche précédent (colonnes = semaines GitHub)
    grid_start = first - dt.timedelta(days=(first.weekday() + 1) % 7)

    cells, month_marks = [], {}
    n_weeks = 0
    for d in days:
        date = dt.date.fromisoformat(d["date"])
        wk = (date - grid_start).days // 7
        dow = (date.weekday() + 1) % 7
        n_weeks = max(n_weeks, wk + 1)
        if date.day <= 7 and dow == 0 or (wk == 0 and date.day == first.day):
            month_marks.setdefault(wk, MONTHS[date.month - 1])
        cells.append((wk, dow, d, date))

    grid_w = n_weeks * PITCH - GAP
    x0 = max(LEFT, (W - grid_w) // 2 + 14)
    H = TOP + 7 * PITCH + 66

    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
      f'aria-label="Graphique des contributions GitHub de {user} : {st["total"]} sur la dernière année">')
    a("<style>.c{opacity:0;animation:drop .5s cubic-bezier(.2,.8,.2,1) forwards}"
      "@keyframes drop{from{opacity:0;transform:translateY(-9px)}to{opacity:1;transform:none}}</style>")
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>')
    a(f'<path d="M0.5 12.5a12 12 0 0 1 12-12h{W - 25}a12 12 0 0 1 12 12V34H0.5z" fill="{BAR}"/>')
    a(f'<line x1="0.5" y1="34" x2="{W - 0.5}" y2="34" stroke="{BORDER}"/>')
    a(f'<circle cx="20" cy="17.5" r="5" fill="#ff5f57"/><circle cx="38" cy="17.5" r="5" fill="#febc2e"/><circle cx="56" cy="17.5" r="5" fill="{ACCENT}"/>')
    a(f'<text x="{W / 2:.0f}" y="21" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{DIM}">{user}@github: ~/contributions</text>')

    a(f'<g font-family="{FONT}" font-size="10" fill="{DIM}">')
    for wk, label in sorted(month_marks.items()):
        a(f'<text x="{x0 + wk * PITCH}" y="{TOP - 10}">{label}</text>')
    for dow, label in ((1, "lun"), (3, "mer"), (5, "ven")):
        a(f'<text x="{x0 - 8}" y="{TOP + dow * PITCH + CELL - 1}" text-anchor="end">{label}</text>')
    a("</g>")

    a("<g>")
    for wk, dow, d, date in cells:
        lvl = level_to_palette(d["level"], d["count"], max_count)
        delay = 0.25 + (wk * 0.018) + (dow * 0.045)
        label = f'{d["count"]} contribution{"s" if d["count"] != 1 else ""} le {date.isoformat()}'
        a(f'<rect class="c" style="animation-delay:{delay:.3f}s" x="{x0 + wk * PITCH}" y="{TOP + dow * PITCH}" '
          f'width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[lvl]}"><title>{label}</title></rect>')
    a("</g>")

    # légende Moins -> Plus
    ly = TOP + 7 * PITCH + 18
    lx = x0 + grid_w - (len(PALETTE) * PITCH + 70)
    a(f'<g font-family="{FONT}" font-size="10" fill="{DIM}">')
    a(f'<text x="{lx}" y="{ly + 9}" text-anchor="end">Moins</text>')
    for i, c in enumerate(PALETTE):
        a(f'<rect x="{lx + 8 + i * PITCH}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
    a(f'<text x="{lx + 14 + len(PALETTE) * PITCH}" y="{ly + 9}">Plus</text>')
    a("</g>")

    # pied de page : stats
    best = st["best_day"]
    best_txt = f'{best["count"]} le {best["date"]}' if best["date"] and best["count"] else "—"
    fy = H - 18
    a(f'<g font-family="{FONT}" font-size="12">')
    a(f'<text x="{x0}" y="{fy}"><tspan fill="{ACCENT}" font-weight="700">{fr_int(st["total"])}</tspan>'
      f'<tspan fill="{TEXT}"> contributions sur la dernière année</tspan>'
      f'<tspan fill="{DIM}">  ·  série en cours </tspan><tspan fill="{TEXT}">{st["current_streak"]} j</tspan>'
      f'<tspan fill="{DIM}">  ·  record </tspan><tspan fill="{TEXT}">{st["longest_streak"]} j</tspan>'
      f'<tspan fill="{DIM}">  ·  meilleur jour </tspan><tspan fill="{TEXT}">{best_txt}</tspan></text>')
    a("</g>")
    a("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print(f"OK -> {OUT} ({W}x{H}, {n_weeks} semaines)")


if __name__ == "__main__":
    main()
