#!/usr/bin/env python3
"""
Hämta transkription från YouTube via yt-dlp.

Försöker i tur och ordning:
  1. Manuella undertexter (bäst kvalitet på namn och fackord)
  2. Auto-genererade undertexter

Returnerar exit-kod:
  0  — OK, transkription sparad till --output
  2  — Metadata-fel (dålig URL eller nätverk)
  3  — Inga captions hittades (kör whisper-fallback.py)
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vtt_till_text import convert_vtt


def get_video_id(url: str) -> str | None:
    m = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})', url)
    return m.group(1) if m else None


# Extractor-args som kringgår YouTubes n-challenge och 429-strypning.
# web-klienten kräver en JS-runtime för att lösa n-challenge; android-klienten
# gör det inte och faller ofta igenom även när web-klienten fått 429.
ANDROID_CLIENT = ['--extractor-args', 'youtube:player_client=android']


def _needs_android_fallback(stderr: str) -> bool:
    return ('429' in stderr
            or 'Requested format is not available' in stderr
            or 'n challenge' in stderr)


def get_metadata(url: str) -> dict | None:
    """Hämta info-JSON med titel, beskrivning, kapitel m.m."""
    cmd = [
        'yt-dlp', '--ignore-config', '--skip-download', '--dump-json',
        '--no-warnings', '--no-playlist',
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    # Bot-detection: försök med cookies om vi fick 403 eller "Sign in"
    if result.returncode != 0 and ('Sign in' in result.stderr or '403' in result.stderr):
        result = subprocess.run(cmd + ['--cookies-from-browser', 'firefox'],
                                capture_output=True, text=True, timeout=60)
    # 429/n-challenge/format-fel: försök med android-klienten
    if result.returncode != 0 and _needs_android_fallback(result.stderr):
        result = subprocess.run(cmd + ANDROID_CLIENT,
                                capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"yt-dlp metadata-fel: {result.stderr.strip()}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def fetch_captions(url: str, out_dir: str, langs: list[str]) -> tuple[Path | None, str | None]:
    """
    Försök hämta undertexter. Returnerar (vtt_path, källa) eller (None, None).
    Källa är 'manual' eller 'auto'.
    """
    vid = get_video_id(url)
    lang_str = ','.join(langs)

    for write_flag, source_label in [
        ('--write-subs', 'manual'),
        ('--write-auto-subs', 'auto'),
    ]:
        cmd = [
            'yt-dlp', '--ignore-config', '--skip-download', write_flag,
            '--sub-langs', lang_str,
            '--sub-format', 'vtt',
            '-o', f'{out_dir}/yt-%(id)s.%(ext)s',
            '--no-warnings', '--no-playlist',
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        # Kolla om vi fick VTT-filer
        pattern = f'yt-{vid}*.vtt' if vid else 'yt-*.vtt'
        vtt_files = list(Path(out_dir).glob(pattern))
        if vtt_files:
            # Välj rätt språkprioritet om flera
            for lang in langs:
                preferred = [f for f in vtt_files if f.stem.endswith(f'.{lang}')]
                if preferred:
                    return preferred[0], source_label
            return vtt_files[0], source_label

        # Bot-detection: försök med cookies om vi fick 403 eller "Sign in"
        if 'Sign in' in result.stderr or '403' in result.stderr:
            cmd_cookies = cmd + ['--cookies-from-browser', 'firefox']
            result2 = subprocess.run(cmd_cookies, capture_output=True, text=True, timeout=120)
            vtt_files = list(Path(out_dir).glob(pattern))
            if vtt_files:
                for lang in langs:
                    preferred = [f for f in vtt_files if f.stem.endswith(f'.{lang}')]
                    if preferred:
                        return preferred[0], f'{source_label}+cookies'
                return vtt_files[0], f'{source_label}+cookies'

        # 429/n-challenge/format-fel: försök med android-klienten
        if _needs_android_fallback(result.stderr):
            result3 = subprocess.run(cmd + ANDROID_CLIENT,
                                     capture_output=True, text=True, timeout=120)
            vtt_files = list(Path(out_dir).glob(pattern))
            if vtt_files:
                for lang in langs:
                    preferred = [f for f in vtt_files if f.stem.endswith(f'.{lang}')]
                    if preferred:
                        return preferred[0], f'{source_label}+android'
                return vtt_files[0], f'{source_label}+android'

    return None, None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('url', help='YouTube-URL')
    p.add_argument('--output', required=True, help='Sökväg till output-textfil')
    p.add_argument('--lang', default='en,sv', help='Språkprioritet, kommaseparerad')
    args = p.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    langs = [l.strip() for l in args.lang.split(',')]

    # Steg 1 — metadata
    meta = get_metadata(args.url)
    if meta is None:
        print('FAIL: kunde inte hämta metadata (kontrollera URL och nätverk)', file=sys.stderr)
        sys.exit(2)

    # Steg 2 — captions (använd temporär mapp för nedladdade filer)
    with tempfile.TemporaryDirectory(prefix='sammanfatta-') as tmpdir:
        vtt_path, source = fetch_captions(args.url, tmpdir, langs)
        if vtt_path is None:
            print('NO_CAPTIONS: inga undertexter hittades — kör whisper-fallback.py', file=sys.stderr)
            sys.exit(3)

        # Steg 3 — VTT → ren text
        text = convert_vtt(vtt_path)

    out_path.write_text(text, encoding='utf-8')

    # Steg 4 — metadata-sidofil
    meta_path = out_path.with_suffix('.meta.json')
    meta_path.write_text(json.dumps({
        'title':          meta.get('title'),
        'uploader':       meta.get('uploader'),
        'upload_date':    meta.get('upload_date'),
        'duration':       meta.get('duration'),
        'description':    meta.get('description'),
        'chapters':       meta.get('chapters'),
        'webpage_url':    meta.get('webpage_url'),
        'caption_source': source,
    }, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f'OK: {out_path} ({source} captions, {len(text)} tecken)')


if __name__ == '__main__':
    main()
