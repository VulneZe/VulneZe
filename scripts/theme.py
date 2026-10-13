"""Design tokens et briques communes à tous les SVG du profil.

Identité visuelle reprise des marques Atlos / Hyzia :
fond clair, cartes blanches, teal de marque, icônes à dégradé.

Pour changer l'identité visuelle (couleurs, polices), il suffit de modifier ce fichier
puis de relancer `python scripts/build_all.py`.
"""
import html

BG = "#ffffff"              # carte principale
BG2 = "#f6faf9"             # surfaces internes
BAR = "#eef4f3"             # bandeau d'en-tête de carte
BORDER = "#dfe8e6"
TINT = "#e9fbf7"            # fond de pastille
TINT2 = "#d4ece7"           # trame / détails doux
ACCENT = "#17a08a"          # teal soutenu (lien Atlos)
ACCENT2 = "#2ebfa5"         # teal de marque
ACCENT_DEEP = "#0e8371"     # teal foncé
INK = "#15302b"             # vert très foncé des logos
TEXT = "#181c22"
DIM = "#5a6570"
WARN = "#d97706"
RED = "#ff5f57"
AMBER = "#febc2e"

MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,&quot;DejaVu Sans Mono&quot;,monospace'
SANS = 'Manrope,-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Helvetica,Arial,sans-serif'

MONO_W = 0.6    # largeur d'un caractère monospace (en em)
SANS_W = 0.56   # largeur moyenne d'un caractère sans-serif (en em)

_ICON_N = [0]


def esc(s):
    return html.escape(s, quote=False)


def text_w(s, size, mono=False):
    return len(s) * size * (MONO_W if mono else SANS_W)


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">')


def panel(w, h):
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>'


def header(w, title):
    """Bandeau de carte façon Atlos : pastille dégradé + titre en sans."""
    return "\n".join([
        f'<path d="M0.5 14.5a14 14 0 0 1 14-14h{w - 29}a14 14 0 0 1 14 14V40H0.5z" fill="{BAR}"/>',
        f'<line x1="0.5" y1="40" x2="{w - 0.5}" y2="40" stroke="{BORDER}"/>',
        f'<defs><linearGradient id="hdg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#3ecdb8"/><stop offset="1" stop-color="#1c8f7c"/></linearGradient></defs>',
        f'<rect x="18" y="14" width="13" height="13" rx="4" fill="url(#hdg)"/>',
        f'<path d="M22.2 20.5l1.9 1.9 3.6-4" fill="none" stroke="#fff" stroke-width="1.7" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<text x="40" y="24.5" font-family="{SANS}" font-size="12.5" font-weight="700" '
        f'letter-spacing=".4" fill="{INK}">{esc(title)}</text>',
    ])


# Icônes Atlos (48x48, dégradé teal + ombre décalée) — le dégradé #g est unique par appel.
_GRAD = ('<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#3ecdb8"/><stop offset="1" stop-color="#1c8f7c"/></linearGradient></defs>')

_ATLOS_ICONS = {
    "shield": '<path d="M27 7l14 5v11c0 10-6 16-14 19-8-3-14-9-14-19V12z" fill="#9fe3d6" opacity=".55"/>'
              '<path d="M23 5l14 5v11c0 10-6 16-14 19-8-3-14-9-14-19V10z" fill="url(#{gid})"/>'
              '<path d="M16.5 24l4.5 4.5 8.5-8.5" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "lock": '<rect x="13" y="21" width="24" height="19" rx="5" fill="#9fe3d6" opacity=".55"/>'
            '<rect x="10" y="19" width="24" height="19" rx="5" fill="url(#{gid})"/>'
            '<path d="M15 19v-4a7 7 0 0 1 14 0v4" fill="none" stroke="url(#{gid})" stroke-width="4" stroke-linecap="round"/>'
            '<circle cx="22" cy="28" r="3" fill="#fff"/><rect x="20.6" y="28" width="2.8" height="6" rx="1.4" fill="#fff"/>',
    "key": '<circle cx="17" cy="19" r="9" fill="#9fe3d6" opacity=".55" transform="translate(3 2)"/>'
           '<circle cx="17" cy="19" r="9" fill="url(#{gid})"/><circle cx="17" cy="19" r="3.4" fill="#fff"/>'
           '<path d="M23 25l16 16M33 35l5-5M28 30l4-4" stroke="url(#{gid})" stroke-width="4" stroke-linecap="round"/>',
    "cloud": '<path d="M16 36a9 9 0 0 1-1-17.9A12 12 0 0 1 38 20a8 8 0 0 1 0 16z" fill="#9fe3d6" opacity=".55" transform="translate(2 2)"/>'
             '<path d="M14 34a9 9 0 0 1-1-17.9A12 12 0 0 1 36 18a8 8 0 0 1 0 16z" fill="url(#{gid})"/>'
             '<rect x="20" y="24" width="10" height="7" rx="2" fill="#fff"/>'
             '<path d="M22.5 24v-2a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="#fff" stroke-width="2.2"/>',
    "device": '<rect x="9" y="11" width="34" height="22" rx="4" fill="#9fe3d6" opacity=".55"/>'
              '<rect x="6" y="9" width="34" height="22" rx="4" fill="url(#{gid})"/>'
              '<rect x="19" y="33" width="8" height="6" fill="url(#{gid})"/>'
              '<rect x="14" y="39" width="18" height="3" rx="1.5" fill="url(#{gid})"/>'
              '<rect x="12" y="15" width="16" height="3" rx="1.5" fill="#fff"/>'
              '<rect x="12" y="21" width="10" height="3" rx="1.5" fill="#fff"/>',
    "globe": '<circle cx="26" cy="26" r="17" fill="#9fe3d6" opacity=".55"/>'
             '<circle cx="23" cy="24" r="17" fill="url(#{gid})"/>'
             '<g fill="none" stroke="#fff" stroke-width="2.4"><ellipse cx="23" cy="24" rx="7" ry="17"/>'
             '<line x1="6.5" y1="19" x2="39.5" y2="19"/><line x1="6.5" y1="29" x2="39.5" y2="29"/>'
             '<line x1="23" y1="7" x2="23" y2="41"/></g>',
    "share": '<circle cx="15" cy="26" r="6.5" fill="url(#{gid})"/><circle cx="35" cy="13" r="6" fill="#9fe3d6"/>'
             '<circle cx="35" cy="38" r="6" fill="url(#{gid})"/>'
             '<path d="M20 23l10-7M20 29l10 7" stroke="url(#{gid})" stroke-width="3" stroke-linecap="round"/>',
    "score": '<path d="M27 10a17 17 0 1 1-12 5" fill="none" stroke="#9fe3d6" opacity=".55" stroke-width="6" stroke-linecap="round" transform="translate(2 2)"/>'
             '<path d="M25 8a17 17 0 1 1-12 5" fill="none" stroke="url(#{gid})" stroke-width="6" stroke-linecap="round"/>'
             '<circle cx="24" cy="25" r="5" fill="url(#{gid})"/><path d="M27 22l7-7" stroke="url(#{gid})" stroke-width="4" stroke-linecap="round"/>',
    "eye": '<path d="M8 24c4-8 10-12 17-12s13 4 17 12c-4 8-10 12-17 12S12 32 8 24z" fill="#9fe3d6" opacity=".55" transform="translate(3 2)"/>'
           '<path d="M6 24c4-8 10-12 17-12s13 4 17 12c-4 8-10 12-17 12S10 32 6 24z" fill="url(#{gid})"/>'
           '<circle cx="23" cy="24" r="6.5" fill="#fff"/><circle cx="23" cy="24" r="3" fill="url(#{gid})"/>',
    "check": '<circle cx="26" cy="26" r="16" fill="#9fe3d6" opacity=".55"/>'
             '<circle cx="23" cy="24" r="16" fill="url(#{gid})"/>'
             '<path d="M15.5 24.5l5 5 10-10" fill="none" stroke="#fff" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "note": '<rect x="13" y="9" width="26" height="32" rx="5" fill="#9fe3d6" opacity=".55"/>'
            '<rect x="9" y="6" width="26" height="32" rx="5" fill="url(#{gid})"/>'
            '<rect x="15" y="15" width="14" height="3" rx="1.5" fill="#fff"/>'
            '<rect x="15" y="22" width="11" height="3" rx="1.5" fill="#fff"/>'
            '<rect x="15" y="29" width="8" height="3" rx="1.5" fill="#fff"/>',
    "folder": '<path d="M11 14h11l4 5h15a3 3 0 0 1 3 3v16a4 4 0 0 1-4 4H14a4 4 0 0 1-4-4V17a3 3 0 0 1 1-3z" fill="#9fe3d6" opacity=".55" transform="translate(2 2)"/>'
              '<path d="M9 12h11l4 5h15a3 3 0 0 1 3 3v16a4 4 0 0 1-4 4H12a4 4 0 0 1-4-4V15a3 3 0 0 1 1-3z" fill="url(#{gid})"/>'
              '<rect x="14" y="26" width="14" height="3" rx="1.5" fill="#fff"/>',
    "clock": '<circle cx="26" cy="26" r="16" fill="#9fe3d6" opacity=".55"/>'
             '<circle cx="23" cy="24" r="16" fill="url(#{gid})"/>'
             '<path d="M23 15v9l6 4" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "sparkle": '<path d="M26 6l4.4 11.6L42 22l-11.6 4.4L26 38l-4.4-11.6L10 22l11.6-4.4z" fill="#9fe3d6" opacity=".55" transform="translate(2 3)"/>'
               '<path d="M24 4l4.4 11.6L40 20l-11.6 4.4L24 36l-4.4-11.6L8 20l11.6-4.4z" fill="url(#{gid})"/>'
               '<circle cx="38" cy="36" r="4" fill="#9fe3d6"/>',
    "import": '<rect x="11" y="26" width="30" height="14" rx="4" fill="#9fe3d6" opacity=".55"/>'
              '<rect x="8" y="24" width="30" height="14" rx="4" fill="url(#{gid})"/>'
              '<path d="M23 6v14M17 15l6 6 6-6" fill="none" stroke="url(#{gid})" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
              '<circle cx="31" cy="31" r="2.5" fill="#fff"/>',
}


def icon_atlos(kind, x, y, size=24):
    """Icône Atlos (viewBox 48) placée en (x, y) à la taille voulue."""
    _ICON_N[0] += 1
    gid = f"ag{_ICON_N[0]}"
    body = _ATLOS_ICONS[kind].format(gid=gid)
    return (f'<g transform="translate({x},{y}) scale({size / 48:.4f})">'
            + _GRAD.format(gid=gid) + body + "</g>")


# Marque Atlos (polygones du wordmark officiel, viewBox 615x120).
ATLOS_MARK = (
    '<g><polygon points="0,120 52,0 68,0 120,120 90,120 60,36 30,120"/></g>'
    '<g transform="translate(140,0)"><rect x="0" y="0" width="104" height="22"/><rect x="38.5" y="30" width="27" height="90"/></g>'
    '<g transform="translate(268,0)"><rect x="0" y="0" width="27" height="120"/><rect x="35" y="98" width="57" height="22"/></g>'
    '<g transform="translate(384,0)"><path fill-rule="evenodd" d="M52,0 C84,0 104,26 104,60 C104,94 84,120 52,120 C20,120 0,94 0,60 C0,26 20,0 52,0 Z M52,22 C33,22 27,38 27,60 C27,82 33,98 52,98 C71,98 77,82 77,60 C77,38 71,22 52,22 Z"/></g>'
    '<g transform="translate(512,0)"><path d="M97,0 V22 H42 C35,22 31,26 31,33 C31,40 35,44 42,44 H62 C85,44 99,58 99,81 C99,105 85,120 60,120 H2 V98 H58 C66,98 72,92 72,82 C72,72 66,66 58,66 H40 C17,66 4,52 4,33 C4,13 18,0 42,0 Z"/></g>'
)

# Marque Hyzia (constellation BIMI officielle, viewBox 128x128).
HYZIA_MARK = (
    '<g stroke="{c}" stroke-width="8" stroke-linecap="round">'
    '<line x1="39.55" y1="67.28" x2="35.17" y2="29.33"/>'
    '<line x1="39.55" y1="67.28" x2="27.14" y2="103.78"/>'
    '<line x1="39.55" y1="67.28" x2="89.18" y2="77.50"/></g>'
    '<g fill="{c}"><circle cx="35.17" cy="29.33" r="15.33"/><circle cx="39.55" cy="67.28" r="15.33"/>'
    '<circle cx="27.14" cy="103.78" r="10.22"/><circle cx="89.18" cy="77.50" r="21.90"/></g>'
)


def atlos_logo(x, y, height, color=INK):
    """Wordmark Atlos à la taille voulue."""
    s = height / 120.0
    return (f'<g transform="translate({x},{y}) scale({s:.4f})" fill="{color}">{ATLOS_MARK}</g>')


def hyzia_logo(x, y, size, color=ACCENT2):
    """Constellation Hyzia à la taille voulue."""
    s = size / 128.0
    return (f'<g transform="translate({x},{y}) scale({s:.4f})">{HYZIA_MARK.format(c=color)}</g>')


def lerp_hex(c1, c2, t):
    t = max(0.0, min(1.0, t))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))
