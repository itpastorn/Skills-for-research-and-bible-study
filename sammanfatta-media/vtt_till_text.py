#!/usr/bin/env python3
"""Konvertera VTT-undertext till ren text med tidsstämplar."""
import re
import sys
from pathlib import Path

TIMESTAMP_RE = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> ')


def convert_vtt(vtt_path: str | Path) -> str:
    """VTT → "(hh:mm:ss) text\\n..." med deduplicering av auto-caption-upprepningar."""
    lines = Path(vtt_path).read_text(encoding="utf-8").splitlines()
    out = []
    current_ts = None
    seen_texts: set[str] = set()

    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT" or line.startswith("NOTE") or line.startswith("STYLE"):
            continue
        # Hoppa över VTT-metadatarader (Kind: captions, Language: en, etc.)
        if re.match(r'^[A-Za-z-]+:\s', line) and not TIMESTAMP_RE.match(line):
            continue
        # Hoppa över cue-identifierare (rena siffror eller UUID-liknande)
        if re.fullmatch(r'[\w-]+', line) and not TIMESTAMP_RE.match(line):
            if re.fullmatch(r'\d+', line):
                continue
        m = TIMESTAMP_RE.match(line)
        if m:
            ts_full = m.group(1)
            current_ts = ts_full[:8]  # hh:mm:ss
            continue
        # Rensa HTML-taggar (<c>, <i>, etc.)
        text = re.sub(r'<[^>]+>', '', line).strip()
        if not text or text in seen_texts:
            continue
        seen_texts.add(text)
        if current_ts:
            out.append(f'({current_ts}) {text}')
            current_ts = None
        else:
            out.append(text)

    return '\n'.join(out)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Användning: vtt-till-text.py <fil.vtt>", file=sys.stderr)
        sys.exit(1)
    print(convert_vtt(sys.argv[1]))
