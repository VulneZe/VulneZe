# PROMPT — Refaire `info-card.svg` dans la vraie DA d'atlos.fr

> Prompt à copier dans Claude Code / Devin. Contexte complet inclus : design
> system réel du site, contenu CV, contraintes techniques SVG/GitHub.

## Mission

Dans le repo `~/Documents/VulneZe` (profil GitHub animé, style terminal), le
panneau de droite `info-card.svg` est à refaire. Il doit ressembler
**fidèlement** au site atlos.fr — pas à un générique "carte IA". Reproduire
son design system exact (tokens ci-dessous), pas juste ses couleurs.

La carte s'affiche à côté d'un portrait ASCII sombre (`vulneze-ascii.svg`,
840×880). Garder le même canvas **840×880** et le même chrome de fenêtre
terminal (3 dots + titre `vulneze@github: ~$ neofetch`) pour la cohérence.

## Références (à lire avant de coder)

- **Repo du site** : `git clone https://github.com/VulneZe/Atlos-Freelance_Website`
  - `src/index.css` — tous les design tokens (copiés ci-dessous)
  - `src/pages/Accueil.tsx`, `src/pages/Prestations.tsx` — usage des composants
  - `tailwind.config.ts` — keyframes (`fade-in`, `slide-in-left`, `float`…)
- **CV** : `~/Téléchargements/CV_RouaultBaptiste.pdf` (`pdftotext` dispo)
- **Script actuel à remplacer** : `scripts/make_info_card.py`
- **Référence animée** : `scripts/render_stats_svg.py` du repo
  `AVIVASHISHTA29/AVIVASHISHTA29` montre les patterns d'animation SVG
  (keyframes stagger, `<set>` count-up, `prefers-reduced-motion`).

## Design system atlos.fr (extraits réels de `src/index.css`)

Le site est **majoritairement clair** avec des bandes sombres — la carte
peut être light OU dark-band, choisir ce qui rend le mieux à côté du
portrait sombre (dark-band conseillé pour la cohérence, ou light avec
bordure forte `#dfe6e8`).

```
body            : bg #fafbfb, text #181c22, font Manrope (fallback system-ui)
liens           : #17a08a → hover #0e8371
gradient CTA    : linear-gradient(135deg, #3ecdb8, #2ebfa5) + shadow 0 6px 20px rgba(46,191,165,.35)
btn             : radius 14px, font-weight 600
dark-band       : linear-gradient(150deg, #101b19, #15302b 60%, #0f2420)
.halo           : radial-gradient(closest-side, rgba(62,205,184,.22), transparent)
.card           : bg #fff, border 1px #eef2f3, radius 22px,
                  hover: translateY(-4px) + shadow 0 16px 40px rgba(20,40,38,.08) + border #d4ece7
.tag / pills    : border 1px #d4ece7, bg rgba(62,205,184,.06), text #0e8371,
                  font-size 12px, weight 700, radius 999px
.pill-badge     : bg rgba(62,205,184,.12), text #0e8371, weight 700, radius 999px
.step-badge     : radius 13px, bg rgba(62,205,184,.16), text #7fe6d5, weight 800   (version dark)
.eyebrow        : 13px / 600 / letter-spacing .14em / UPPERCASE / #2ebfa5
                  (variante dark: #3ecdb8)
icon-box        : bg rgba(62,205,184,.10), centré
gris/muted      : #5a6570, #3a444e, bordures #dfe6e8 / #eef2f3 / #e4eeec
clair           : #d4ece7 (bordure teal pâle), #eef2f3, #fbfdfd
mint dark-mode  : #7fe6d5 (texte bright sur dark band), #3ecdb8 (accent), #2ebfa5
```

Éléments signature à reprendre : **pills `.tag`**, **step-badge/icon-box
carré radius 13px**, **halos radials teal**, **eyebrow uppercase
letter-spacé**, **gradient teal** sur un élément fort (le pseudo ou un
bouton), radius **14px / 22px / 999px**, ombres douces
`rgba(20,40,38,.08)`.

## Contenu (réel, issu du CV — ne pas inventer)

- Pseudo : `vulneze` / `vulneze@github`
- Nom : Baptiste Rouault
- Titre : **RSSI adjoint & Architecte réseaux et cybersécurité** — éditeur de
  logiciels (depuis fév. 2026)
- Statut : **disponible à partir de septembre 2027**
- Exp. clés : SMSI, conformité **NIS2 & ISO 27001**, solutions **XDR/EDR/SIEM
  on-premise** (Wazuh, CrowdStrike, TEHTRIS, Bitdefender), formation
  collaborateurs
- Stack : AD/GPO, M365/Azure, Fortinet/pfSense, VLAN/VPN/ZTNA, Proxmox/VMware,
  Docker, Ansible, k8s, PowerShell/Bash/Python, AWS (ECS/S3), PKI/YubiKey
- Précédents : admin réseaux/sys/cyber Logisseo (2024–25), LACROIX (2022–24,
  SOC TEHTRIS/Sentinel, Zero Trust SASE), stage SOC N1 Cooperl (2022)
- Pratique : HackTheBox, homelab Proxmox + Tailscale
- Lieu : France

Lignes à afficher (style neofetch `key: value`, keys en teal) — adapter la
hiérarchie librement tant que ça reste factuel :
Role / Defense / Networks / Systems / Homelab / Training / Stack / Location

## Contraintes techniques (obligatoires)

- **Un seul fichier SVG autonome** généré par `scripts/make_info_card.py`
  (sortie : `info-card.svg` à la racine du repo).
- GitHub exécute les animations **SMIL et CSS keyframes** dans les `<img>`,
  mais **jamais de JS**. Animation one-shot qui joue puis fige (`both`), pas
  de boucle tape-œil (seul un curseur ou le dot de statut peut pulser).
- Reproduire le stagger fade/slide existant (`.d`/`.l`/`.p` classes,
  `animation-delay` progressif).
- `STATIC=1 python scripts/make_info_card.py` doit émettre une frame figée
  pour preview locale (déjà implémenté, garder le pattern).
- **Échapper le XML** (`html.escape`) : `&` dans "CYBERSÉCURITÉ & RÉSEAUX"
  plante le rendu sinon — c'est arrivé une fois.
- Pas de font externe : `ui-monospace, SFMono-Regular, Menlo, Consolas,
  monospace` (Manrope non dispo chez les visiteurs).
- Tester : `STATIC=1 python scripts/make_info_card.py /tmp/p.svg` puis
  `cairosvg` pour rasteriser et vérifier visuellement (aucun débordement :
  max ~40 caractères par ligne à font-size 20 sur 780px utiles).
- Ne pas mentionner "atlos" ou "atlos.fr" dans les textes affichés.

## Livrable

`scripts/make_info_card.py` réécrit + `info-card.svg` régénéré + preview
PNG vérifié visuellement avant de finir.
