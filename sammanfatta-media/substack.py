#!/usr/bin/env python3
"""
Hämta transkription från ett Substack-inlägg (video eller podd).

Substack transkriberar själv uppladdade videor och poddavsnitt. Transkriptionen
nås inte via yt-dlp men ligger öppet i inläggets API-post:

    https://<publikation>.substack.com/api/v1/posts/<slug>

Där finns ett transkriptionsobjekt med signerade CDN-adresser till en VTT-fil
per språk (`signed_captions`) och till en JSON-fil med ordnivådata (`cdn_url`).
Båda bär talaretiketter — SPEAKER_00, SPEAKER_01 … — som YouTubes textning
saknar, och de bevaras här.

Anrop från hamta_transkription.py och main.py:

    text, meta = hamta(url, langs)

    (None, None)  — inte ett Substack-inlägg; gå vidare till yt-dlp
    (None, meta)  — Substack-inlägg utan åtkomlig transkription
    (text, meta)  — klart; meta har samma nycklar som YouTube-vägens sidofil
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from urllib.parse import urlparse

UA = 'Mozilla/5.0 (sammanfatta-media)'
TIMEOUT = 30


# --------------------------------------------------------------------------
# URL → API-adress
# --------------------------------------------------------------------------
def api_adresser(url: str) -> list[str]:
    """Möjliga API-adresser för en inläggs-URL, i prioritetsordning.

    Täcker:
      https://<pub>.substack.com/p/<slug>
      https://open.substack.com/pub/<pub>/p/<slug>
      https://substack.com/home/post/p-<id>   och   https://substack.com/@<namn>/p-<id>
      https://<egen domän>/p/<slug>            (bekräftas mot API-svaret)
    """
    u = urlparse(url.strip())
    if u.scheme not in ('http', 'https') or not u.netloc:
        return []
    vard = u.netloc.lower()
    vag = u.path.rstrip('/')

    m = re.search(r'/p-(\d+)$', vag)
    if m:
        return [f'https://substack.com/api/v1/posts/by-id/{m.group(1)}']

    m = re.match(r'^/pub/([^/]+)/p/([^/]+)$', vag)
    if vard == 'open.substack.com' and m:
        return [f'https://{m.group(1)}.substack.com/api/v1/posts/{m.group(2)}']

    m = re.match(r'^/p/([^/]+)$', vag)
    if m:
        return [f'https://{vard}/api/v1/posts/{m.group(1)}']

    return []


def ar_trolig_substack(url: str) -> bool:
    """Billig kontroll utan nätverk. YouTube-adresser ger alltid False."""
    return bool(api_adresser(url))


def _hamta_json(adress: str) -> dict | list | None:
    # Ingen kontroll av Content-Type: CDN:et serverar transcription.json som
    # binärdata, och en HTML-sida från en främmande domän faller ändå i json.loads.
    req = urllib.request.Request(adress, headers={'User-Agent': UA,
                                                  'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as svar:
            return json.loads(svar.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None


def _hamta_text(adress: str) -> str | None:
    req = urllib.request.Request(adress, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as svar:
            return svar.read().decode('utf-8')
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError):
        return None


def hamta_post(url: str) -> dict | None:
    """Inläggsposten, eller None om adressen inte är ett Substack-inlägg."""
    for adress in api_adresser(url):
        data = _hamta_json(adress)
        if isinstance(data, dict) and isinstance(data.get('post'), dict):
            data = data['post']                      # by-id-svaret är inkapslat
        # En egen domän med /p/ kan vara något helt annat (Medium m.fl.) —
        # godta bara svar som ser ut som en Substack-post.
        if isinstance(data, dict) and 'publication_id' in data and 'slug' in data:
            return data
    return None


# --------------------------------------------------------------------------
# Hitta transkriptionen i posten
# --------------------------------------------------------------------------
def _transkriptionsobjekt(post: dict) -> list[dict]:
    """Alla transkriptionsobjekt i posten, de med VTT-adresser först.

    Placeringen varierar: videoUpload.extractedAudio.transcription för video,
    podcastUpload.transcription för podd — och Substack flyttar saker. Därför
    söks hela posten igenom efter objekt som bär adressfälten."""
    hittade: list[dict] = []

    def gå(o):
        if isinstance(o, dict):
            if o.get('signed_captions') or o.get('cdn_url'):
                if o not in hittade:
                    hittade.append(o)
            for v in o.values():
                gå(v)
        elif isinstance(o, list):
            for v in o:
                gå(v)

    gå(post)
    return sorted(hittade, key=lambda t: 0 if t.get('signed_captions') else 1)


def _valj_undertext(transkr: dict, langs: list[str]) -> tuple[str, str] | None:
    """(url, språk) för bästa VTT. Originalspråket går före översättningar —
    samma princip som -orig-spåren i YouTube-vägen."""
    spar = [s for s in (transkr.get('signed_captions') or []) if s.get('url')]
    if not spar:
        return None
    karta = transkr.get('captions_map') or {}

    def prio(s):
        sprak = s.get('language') or ''
        original = bool((karta.get(sprak) or {}).get('original'))
        plats = langs.index(sprak) if sprak in langs else len(langs)
        return (0 if original else 1, plats)

    basta = sorted(spar, key=prio)[0]
    return basta['url'], basta.get('language') or ''


# --------------------------------------------------------------------------
# Konvertering till arkivformatet "(hh:mm:ss) text"
# --------------------------------------------------------------------------
TIDSRAD = re.compile(r'^((?:\d{1,2}:)?\d{2}:\d{2})\.\d{3}\s+-->')
TALARE = re.compile(r'<v\s+([^>]+)>')


def _hhmmss(tid: str) -> str:
    delar = tid.split(':')
    if len(delar) == 2:
        delar.insert(0, '0')
    return ':'.join(f'{int(d):02d}' for d in delar)


def _sekunder_till_hhmmss(s: float) -> str:
    s = int(s)
    return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def _rader_med_talare(poster: list[tuple[str, str | None, str]]) -> tuple[str, list[str]]:
    """[(hh:mm:ss, talare, text)] → text där talaren anges vid varje talarbyte.

    Etiketten sätts bara vid byte, inte på varje rad. Då kan
    normalisera_namn.py matcha ett namn som textningen delat över två rader
    hos samma talare, och texten blir läsbar. Ingen deduplicering: till skillnad
    från YouTubes rullande autotext är upprepade repliker här verkliga ("Ja.")."""
    ut: list[str] = []
    forra = None
    sedda: list[str] = []
    for tid, talare, text in poster:
        if talare and talare not in sedda:
            sedda.append(talare)
        if talare and talare != forra:
            ut.append(f'({tid}) {talare}: {text}')
            forra = talare
        else:
            ut.append(f'({tid}) {text}')
    return '\n'.join(ut), sedda


def vtt_till_text(vtt: str) -> tuple[str, list[str]]:
    poster: list[tuple[str, str | None, str]] = []
    tid = None
    for rad in vtt.splitlines():
        rad = rad.strip()
        m = TIDSRAD.match(rad)
        if m:
            tid = _hhmmss(m.group(1))
            continue
        if not rad or tid is None or rad == 'WEBVTT' or re.fullmatch(r'\d+', rad):
            continue
        t = TALARE.search(rad)
        text = re.sub(r'<[^>]+>', '', rad).strip()
        if text:
            poster.append((tid, t.group(1).strip() if t else None, text))
            tid = None
    return _rader_med_talare(poster)


def json_till_text(segment: list) -> tuple[str, list[str]]:
    """Reservväg: transcription.json har talare per ord, inte per segment.
    Segmentets talare blir den som äger flest av dess ord."""
    poster: list[tuple[str, str | None, str]] = []
    for seg in segment:
        text = (seg.get('text') or '').strip()
        if not text:
            continue
        talare = Counter(w.get('speaker') for w in seg.get('words') or [] if w.get('speaker'))
        poster.append((_sekunder_till_hhmmss(seg.get('start') or 0),
                       talare.most_common(1)[0][0] if talare else None,
                       text))
    return _rader_med_talare(poster)


# --------------------------------------------------------------------------
# Huvudfunktion
# --------------------------------------------------------------------------
def _metadata(post: dict, url: str) -> dict:
    byline = ', '.join(b.get('name') for b in post.get('publishedBylines') or [] if b.get('name'))
    langd = ((post.get('videoUpload') or {}).get('duration')
             or (post.get('podcastUpload') or {}).get('duration')
             or post.get('podcast_duration'))
    return {
        'title':          post.get('title'),
        'uploader':       byline or None,
        'upload_date':    (post.get('post_date') or '')[:10].replace('-', '') or None,
        'duration':       round(langd) if isinstance(langd, (int, float)) else None,
        'description':    post.get('subtitle') or post.get('description'),
        'chapters':       None,
        'webpage_url':    post.get('canonical_url') or url,
        'caption_source': None,
        'platform':       'substack',
        'media':          'video' if post.get('videoUpload') else
                          'podd' if post.get('podcastUpload') else None,
        'audience':       post.get('audience'),
    }


def hamta(url: str, langs: list[str]) -> tuple[str | None, dict | None]:
    if not ar_trolig_substack(url):
        return None, None
    post = hamta_post(url)
    if post is None:
        return None, None

    meta = _metadata(post, url)
    for transkr in _transkriptionsobjekt(post):
        val = _valj_undertext(transkr, langs)
        if val:
            vtt = _hamta_text(val[0])
            if vtt and 'WEBVTT' in vtt[:20]:
                text, talare = vtt_till_text(vtt)
                if text:
                    meta.update(caption_source='substack-vtt', caption_language=val[1],
                                speakers=talare)
                    return text, meta
        if transkr.get('cdn_url'):
            segment = _hamta_json(transkr['cdn_url'])
            if isinstance(segment, list):
                text, talare = json_till_text(segment)
                if text:
                    meta.update(caption_source='substack-json', speakers=talare)
                    return text, meta
    return None, meta


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Användning: substack.py <inläggs-URL>', file=sys.stderr)
        sys.exit(1)
    text, meta = hamta(sys.argv[1], ['sv', 'en'])
    if meta is None:
        print('Inte ett Substack-inlägg.', file=sys.stderr)
        sys.exit(2)
    if text is None:
        print('Substack-inlägg utan åtkomlig transkription.', file=sys.stderr)
        sys.exit(3)
    print(text)
