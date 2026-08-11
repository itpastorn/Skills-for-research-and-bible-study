#!/usr/bin/env python3
"""
normalisera_namn.py — infoga rätt stavning av egennamn i en hämtad
transkription, så att arkivet går att söka i.

Undertexter — särskilt auto-genererade och sändningstextade — förvanskar
regelmässigt egennamn. Transkriptionen sparas permanent och ska gå att söka
i långt senare, men "Pchesca" hittas aldrig av den som söker på
"Prochaska". Detta skript infogar den rätta stavningen inom hakparentes
direkt efter felstavningen, utan att röra originaltexten:

    Pchesca [Prochaska]

Vid osäker identifiering läggs frågetecken till:

    Pchesca [Prochaska ?]

Felstavningen står kvar orörd. Inget markeras med [sic].

Användning:
    python normalisera_namn.py <transkriptfil> --mappning <mappning.json>
    python normalisera_namn.py <transkriptfil> --mappning <m.json> --torrkorning

Mappningsfilens format — en lista av objekt:

    [
      {"fel": "Pchesca",       "ratt": "Prochaska"},
      {"fel": "Farnbeck",      "ratt": "Farnebäck"},
      {"fel": "Brad Zadznney", "ratt": "Brandy Zadrozny", "osaker": true}
    ]

Egenskaper:
    - Skiftlägesokänslig matchning (undertexter växlar ofta till VERSALER),
      men originalets skiftläge bevaras — bara hakparentesen läggs till.
    - Längsta felstavningen matchas först, så att "Brad Zadznney" hanteras
      före ett eventuellt ensamt "Zadznney".
    - Idempotent: en redan annoterad förekomst annoteras inte igen, så
      skriptet kan köras om utan att bygga på hakparenteser.
    - Engelsk genitiv ("Pchesca's") matchas och annoteras efter namnet.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GENITIV = r"(?:['’]s)?"
# Undertextfiler radbryter mitt inne i namn och lämnar kvar &nbsp; från VTT-
# källan. "Brandi\nZadrozny" och "Brandi&nbsp;Zadrozny" är samma namn som
# "Brandi Zadrozny" och måste matcha likadant.
AVSKILJARE = r"(?:\s|&nbsp;)+"


def _bygg_monster(fel: str) -> re.Pattern:
    """Ordgränsat, skiftlägesokänsligt mönster med valfri engelsk genitiv.

    Mellanslag i felstavningen matchar godtyckligt blanktecken, inklusive
    radbrytning och &nbsp;, så att flerordsnamn hittas även när textningen
    brutit dem över två rader."""
    delar = AVSKILJARE.join(re.escape(d) for d in fel.split())
    return re.compile(
        r"(?<![^\W\d_])" + delar + GENITIV + r"(?![^\W\d_])",
        re.IGNORECASE,
    )


def normalisera(text: str, mappning: list[dict]) -> tuple[str, dict[str, int]]:
    """Infoga hakparenteser med rätt stavning. Returnerar (text, antal per post)."""
    # Längsta felstavningen först — annars äter en kort post upp en längre.
    poster = sorted(mappning, key=lambda p: len(p["fel"]), reverse=True)
    antal: dict[str, int] = {}

    for post in poster:
        fel, ratt = post["fel"], post["ratt"]
        osaker = bool(post.get("osaker", False))
        etikett = f" [{ratt} ?]" if osaker else f" [{ratt}]"
        monster = _bygg_monster(fel)
        traffar = 0

        def ersatt(m: re.Match) -> str:
            nonlocal traffar
            # Redan annoterad? Lämna orörd.
            svans = text[m.end():m.end() + len(etikett) + 4]
            if re.match(r"\s*\[", svans):
                return m.group(0)
            traffar += 1
            return m.group(0) + etikett

        text = monster.sub(ersatt, text)
        antal[fel] = traffar

    return text, antal


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transkript", type=Path, help="transkriptionsfil (.txt)")
    ap.add_argument("--mappning", type=Path, required=True,
                    help="JSON-fil med felstavningar och rätta namn")
    ap.add_argument("--output", type=Path, default=None,
                    help="skriv till annan fil (standard: skriv över originalet)")
    ap.add_argument("--torrkorning", action="store_true",
                    help="visa bara vad som skulle ändras")
    args = ap.parse_args()

    if not args.transkript.exists():
        print(f"FEL: hittar inte {args.transkript}", file=sys.stderr)
        return 1
    if not args.mappning.exists():
        print(f"FEL: hittar inte {args.mappning}", file=sys.stderr)
        return 1

    mappning = json.loads(args.mappning.read_text(encoding="utf-8"))
    if not isinstance(mappning, list):
        print("FEL: mappningsfilen ska innehålla en lista av objekt.", file=sys.stderr)
        return 1
    for post in mappning:
        if "fel" not in post or "ratt" not in post:
            print(f"FEL: posten saknar fel/ratt: {post}", file=sys.stderr)
            return 1

    text = args.transkript.read_text(encoding="utf-8")
    ny_text, antal = normalisera(text, mappning)

    totalt = sum(antal.values())
    utan_traff = [f for f, n in antal.items() if n == 0]

    for post in sorted(mappning, key=lambda p: p["fel"].lower()):
        fel = post["fel"]
        markor = " ?" if post.get("osaker") else ""
        print(f"  {antal[fel]:4d}  {fel} -> {post['ratt']}{markor}")
    print(f"\nTotalt {totalt} infogningar från {len(mappning)} poster.")

    if utan_traff:
        print(f"VARNING: utan träff i texten: {', '.join(utan_traff)}", file=sys.stderr)

    if args.torrkorning:
        print("Torrkörning — ingen fil skrevs.")
        return 0

    mal = args.output or args.transkript
    mal.write_text(ny_text, encoding="utf-8")
    print(f"Skrev: {mal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
