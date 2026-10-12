"""Design tokens et briques communes à tous les SVG du profil.

Pour changer l'identité visuelle (couleurs, polices), il suffit de modifier ce fichier
puis de relancer `python scripts/build_all.py`.
"""
import html

BG = "#0b1214"
BG2 = "#0f1a1d"
BAR = "#111b1e"
BORDER = "#1c2b2f"
ACCENT = "#2ebfa5"        # teal de la marque
ACCENT2 = "#7be0cc"
ACCENT_DEEP = "#14705f"
TEXT = "#d7ece8"
DIM = "#6f8a88"
WARN = "#febc2e"
RED = "#ff5f57"

MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,&quot;DejaVu Sans Mono&quot;,monospace'
SANS = '-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Helvetica,Arial,sans-serif'

MONO_W = 0.6    # largeur d'un caractère monospace (en em)
SANS_W = 0.56   # largeur moyenne d'un caractère sans-serif (en em)


def esc(s):
    return html.escape(s, quote=False)


def text_w(s, size, mono=False):
    return len(s) * size * (MONO_W if mono else SANS_W)


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">')


def panel(w, h):
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>'


def window_chrome(w, title):
    """Barre de titre façon terminal : 3 pastilles + titre centré."""
    return "\n".join([
        f'<path d="M0.5 12.5a12 12 0 0 1 12-12h{w - 25}a12 12 0 0 1 12 12V34H0.5z" fill="{BAR}"/>',
        f'<line x1="0.5" y1="34" x2="{w - 0.5}" y2="34" stroke="{BORDER}"/>',
        f'<circle cx="20" cy="17.5" r="5" fill="{RED}"/><circle cx="38" cy="17.5" r="5" fill="{WARN}"/>'
        f'<circle cx="56" cy="17.5" r="5" fill="{ACCENT}"/>',
        f'<text x="{w / 2:.0f}" y="21" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{DIM}">{esc(title)}</text>',
    ])


def lerp_hex(c1, c2, t):
    t = max(0.0, min(1.0, t))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))
