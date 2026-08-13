#!/usr/bin/env python3
"""
whisper_fallback.py — Form B i sammanfatta-media: transkribera med Whisper när
YouTube saknar undertexter helt.

Hämtar ljudet med yt-dlp och transkriberar med openai-whisper. Utdata får samma
format som Form A, alltså en rad per segment inledd med "(hh:mm:ss)", så att
resten av kedjan — namnnormalisering och rapportbygge — fungerar oförändrad.

Användning:
    python whisper_fallback.py <URL> --output <fil.txt> [--modell base.en]
    python whisper_fallback.py <URL> --output <fil.txt> --modell small   # svenska

Modellval:
    base.en   snabbast, duger för tydligt engelskt tal (standard)
    small     bättre på brus, brytning och namn; ungefär tre gånger långsammare
    KBLab/kb-whisper-large för svenska kräver faster-whisper, se config.yml

Beroenden:
    pip install -U openai-whisper      (kräver ffmpeg i PATH)

VIKTIGT — tyst avkortning:
    Whisper har observerats avsluta i förtid utan felmeddelande, i ett fall vid
    80 procent av ljudet. Skriptet jämför därför sista tidsstämpeln med ljudets
    faktiska längd och larmar om skillnaden är mer än 15 sekunder. Larmet ska
    tas på allvar: transkriptionen är då ofullständig och resten måste köras
    separat med ffmpeg-trim och tidsförskjutning.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOLERANS_S = 15.0


def hamta_ljud(url: str, mapp: Path) -> Path:
    """Ladda ner bästa ljudspår som mp3."""
    mal = mapp / "ljud.%(ext)s"
    cmd = [
        "yt-dlp", "--ignore-config", "-f", "bestaudio/best",
        "--extract-audio", "--audio-format", "mp3", "--audio-quality", "5",
        "-o", str(mal), "--no-playlist", url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # Samma fallbackar som hamta_transkription.py använder.
        for extra in (["--cookies-from-browser", "firefox"],
                      ["--extractor-args", "youtube:player_client=android"]):
            r = subprocess.run(cmd + extra, capture_output=True, text=True)
            if r.returncode == 0:
                break
    filer = list(mapp.glob("ljud.*"))
    if not filer:
        print(f"FEL: ljudnedladdning misslyckades: {r.stderr.strip()[:400]}", file=sys.stderr)
        raise SystemExit(1)
    return filer[0]


def ljudlangd(fil: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(fil)],
        capture_output=True, text=True,
    )
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return 0.0


def tidsstampel(sekunder: float) -> str:
    s = int(sekunder)
    return f"({s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d})"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--modell", default="base.en")
    ap.add_argument("--sprak", default=None, help="t.ex. sv; utelämna för automatik")
    args = ap.parse_args()

    import whisper  # importeras sent, laddningen tar tid

    with tempfile.TemporaryDirectory(prefix="whisper-fallback-") as tmp:
        mapp = Path(tmp)
        print("Hämtar ljud ...", file=sys.stderr)
        ljud = hamta_ljud(args.url, mapp)
        langd = ljudlangd(ljud)
        print(f"Ljud: {ljud.name}, {langd:.0f} s. Laddar modell {args.modell} ...",
              file=sys.stderr)

        modell = whisper.load_model(args.modell)
        print("Transkriberar ...", file=sys.stderr)
        resultat = modell.transcribe(str(ljud), language=args.sprak, verbose=False)

    segment = resultat.get("segments", [])
    if not segment:
        print("FEL: Whisper gav inga segment.", file=sys.stderr)
        return 1

    rader = [f"{tidsstampel(s['start'])} {s['text'].strip()}" for s in segment]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(rader) + "\n", encoding="utf-8")

    slut = segment[-1]["end"]
    print(f"OK: {args.output} ({len(rader)} segment, "
          f"{sum(len(r) for r in rader)} tecken)")
    if langd and (langd - slut) > TOLERANS_S:
        print(f"VARNING: transkriptionen slutar vid {slut:.0f} s men ljudet är "
              f"{langd:.0f} s långt. {langd - slut:.0f} s saknas — kör resten "
              f"separat med ffmpeg-trim och lägg på offset.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
