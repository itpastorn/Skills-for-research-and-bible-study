#!/usr/bin/env python3
"""
main.py — CLI-ingång för sammanfatta-media.

Användning (Git Bash / terminal):
    python main.py <URL> [--lang en,sv] [--output <path>]
    python main.py --inbox            # läs URL från inkorgsmappen

Denna fil hämtar transkription och sparar den. Sammanfattning och
rapportbygge sker av Claude Code-skillen (SKILL.md) med transkriptionen
som underlag. För helautomatisk körning utan Claude behövs Claude API
(framtida utbyggnad).

Inkorgsformat:
    Lägg en .txt-fil i inkorgsmappen med en URL per rad.
    Filen konsumeras (raderna tas bort) efter bearbetning.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

def _load_config() -> dict:
    """Läs config.yml från skriptmappen om den finns."""
    try:
        import yaml  # type: ignore
        cfg_path = SCRIPTS_DIR / "config.yml"
        if cfg_path.exists():
            return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except ImportError:
        pass
    return {}

_cfg = _load_config()
INBOX_DIR   = Path(_cfg.get("inbox_dir", "")).expanduser() if _cfg.get("inbox_dir") else Path.home() / "sammanfatta-media" / "inbox"
DEFAULT_OUT = Path(_cfg.get("output_dir", "")).expanduser() if _cfg.get("output_dir") else Path.home() / "sammanfatta-media" / "out"

sys.path.insert(0, str(SCRIPTS_DIR))
from hamta_transkription import get_metadata, fetch_captions
from vtt_till_text import convert_vtt

import json
import tempfile


def slugify(text: str, max_len: int = 60) -> str:
    """Titel → filnamns-slug (a-z, 0-9, bindestreck)."""
    import re
    text = text.lower()
    for src, dst in [('å','a'),('ä','a'),('ö','o'),('ü','u'),('é','e'),('ñ','n')]:
        text = text.replace(src, dst)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text[:max_len]


def hamta_och_spara(url: str, out_dir: Path, langs: list[str]) -> Path | None:
    """Hämta transkription för en URL och spara till out_dir. Returnerar textfilen."""
    print(f"\n→ Hämtar: {url}")

    meta = get_metadata(url)
    if meta is None:
        print("  FAIL: kunde inte hämta metadata.", file=sys.stderr)
        return None

    title = meta.get('title', 'utan-titel')
    slug = slugify(title)
    out_path = out_dir / f"transkript-{slug}.txt"

    print(f"  Titel: {title}")

    with tempfile.TemporaryDirectory(prefix='sammanfatta-') as tmpdir:
        vtt_path, source = fetch_captions(url, tmpdir, langs)
        if vtt_path is None:
            print("  NO_CAPTIONS: inga undertexter hittades.", file=sys.stderr)
            print("  Kör whisper-fallback.py för audio-transkribering.", file=sys.stderr)
            return None

        text = convert_vtt(vtt_path)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding='utf-8')

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

    print(f"  ✓ Sparad: {out_path} ({source}, {len(text):,} tecken)")
    return out_path


def read_inbox() -> list[str]:
    """Läs URL:er från alla .txt-filer i inkorgsmappen. Returnerar lista."""
    urls = []
    for f in INBOX_DIR.glob("*.txt"):
        if f.name == "purpose-of-folder.md":
            continue
        lines = f.read_text(encoding='utf-8').splitlines()
        new_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if line.startswith('http'):
                    urls.append(line)
                else:
                    new_lines.append(line)  # bevara icke-URL-rader
            else:
                new_lines.append(line)
        remaining = '\n'.join(new_lines).strip()
        if remaining:
            f.write_text(remaining + '\n', encoding='utf-8')
        else:
            f.unlink()
    return urls


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('url', nargs='?', help='YouTube-URL att transkribera')
    p.add_argument('--inbox', action='store_true', help='Läs URL:er från inkorgsmappen')
    p.add_argument('--lang', default='en,sv', help='Språkprioritet (default: en,sv)')
    p.add_argument('--output', help=f'Utdatamapp (default: {DEFAULT_OUT})')
    args = p.parse_args()

    langs = [l.strip() for l in args.lang.split(',')]
    out_dir = Path(args.output) if args.output else DEFAULT_OUT

    if args.inbox:
        urls = read_inbox()
        if not urls:
            print("Inkorgen är tom.")
            sys.exit(0)
        for url in urls:
            hamta_och_spara(url, out_dir, langs)
    elif args.url:
        result = hamta_och_spara(args.url, out_dir, langs)
        if result is None:
            sys.exit(1)
    else:
        p.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
