#!/usr/bin/env python3
"""Récupère le calendrier de contributions public de GitHub, sans token ni API.

GitHub sert ce fragment HTML à l'adresse https://github.com/users/<user>/contributions
(le même que celui utilisé par la page de profil). On le parse avec BeautifulSoup
et on écrit data/contributions.json : jours bruts + stats dérivées.

Usage : python scripts/fetch_contributions.py [utilisateur]
"""
import datetime as dt
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_USER", "vulneze")
OUT = os.path.join("data", "contributions.json")
URL = f"https://github.com/users/{USER}/contributions"


def fetch_html():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "profile-art/1.0"})
    r.raise_for_status()
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    tips = {}
    for t in soup.find_all("tool-tip"):
        m = re.match(r"\s*(No|\d[\d,]*)\s+contribution", t.get_text())
        if m and t.get("for"):
            tips[t["for"]] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))

    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        count = tips.get(td.get("id"), None)
        level = int(td.get("data-level", 0))
        if count is None:
            # Pas d'infobulle : on retombe sur le niveau pour ne rien perdre
            count = 0 if level == 0 else level
        days.append({"date": td["data-date"], "count": count, "level": level})
    days.sort(key=lambda d: d["date"])
    return days


def stats(days):
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else {"date": None, "count": 0}

    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)

    # série en cours : on tolère que "aujourd'hui" soit encore vide
    current = 0
    seq = list(days)
    if seq and seq[-1]["count"] == 0:
        seq = seq[:-1]
    for d in reversed(seq):
        if d["count"] > 0:
            current += 1
        else:
            break

    months = {}
    for d in days:
        key = d["date"][:7]
        months[key] = months.get(key, 0) + d["count"]

    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "months": months,
    }


def main():
    os.makedirs("data", exist_ok=True)
    try:
        days = parse(fetch_html())
        if not days:
            raise RuntimeError("calendrier introuvable dans la réponse")
        source = "github"
    except Exception as exc:  # hors-ligne, profil vide ou HTML modifié
        print(f"[warn] récupération impossible ({exc}) — calendrier vide généré", file=sys.stderr)
        end = dt.date.today()
        start = end - dt.timedelta(days=364)
        days = [
            {"date": (start + dt.timedelta(days=i)).isoformat(), "count": 0, "level": 0}
            for i in range(365)
        ]
        source = "empty"

    payload = {
        "user": USER,
        "source": source,
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "days": days,
        "stats": stats(days),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"OK -> {OUT} ({len(days)} jours, {payload['stats']['total']} contributions, source={source})")


if __name__ == "__main__":
    main()
