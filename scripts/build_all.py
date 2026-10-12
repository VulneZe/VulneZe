#!/usr/bin/env python3
"""Régénère tous les visuels du profil d'un coup.

Usage : python scripts/build_all.py
  (la première fois : python scripts/prep_photo.py source-photo.png)
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.chdir(ROOT)

STEPS = [
    "make_banner_svg",
    "make_portrait_svg",
    "make_info_card",
    "make_architecture_svg",
    "make_skills_svg",
    "render_heatmap_svg",   # nécessite data/contributions.json (workflow quotidien)
]

for name in STEPS:
    mod = importlib.import_module(name)
    mod.main()
