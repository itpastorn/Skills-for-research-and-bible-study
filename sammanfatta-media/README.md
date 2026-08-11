# sammanfatta-media

En Claude Code-skill som hämtar transkriptioner från YouTube och producerar strukturerade sammanfattningar — som chattsvar eller sparade rapporter (Word, Markdown, PDF).

## Funktioner

- Hämtar undertexter automatiskt via yt-dlp (manuella och auto-genererade)
- Normaliserar egennamn i transkriptionen — förvanskade namn får rätt stavning inom hakparentes (`Pchesca [Prochaska]`), så att arkivet blir sökbart
- Stödjer enskild URL, flera URL:er och hela spellistor
- Fyra diagnostiknivåer: ingen / enkel bedömning / kritisk analys / skarp kritik
- Rapportformat: Word (.docx med IBM Plex Sans), Markdown, PDF
- Källidentifiering med statusmärkning
- Obligatorisk språklig genomgång före rapportleverans
- Fallback till Whisper-transkribering när undertexter saknas (kräver `whisper_fallback.py`)

## Krav

```bash
pip install yt-dlp python-docx
# Valfritt, för YAML-konfiguration i main.py:
pip install pyyaml
```

yt-dlp bör uppdateras regelbundet:

```bash
pip install -U yt-dlp
```

## Installation

```bash
# Klona repot direkt till Claude Code-skillsmappen
git clone https://github.com/itpastorn/Skills-for-research-and-bible-study.git
cp -r Skills-for-research-and-bible-study/sammanfatta-media ~/.claude/skills/

# Eller på Windows (PowerShell):
git clone https://github.com/itpastorn/Skills-for-research-and-bible-study.git
Copy-Item -Recurse Skills-for-research-and-bible-study\sammanfatta-media `
    "$env:USERPROFILE\.claude\skills\sammanfatta-media"
```

## Konfiguration

```bash
cd ~/.claude/skills/sammanfatta-media
cp config.yml.example config.yml
# Redigera config.yml med din editor
```

Minimikonfiguration:

```yaml
output_dir: ~/Documents/sammanfatta-media/out
transcripts_dir: ~/Documents/sammanfatta-media/transkriptioner
default_lang: "en,sv"
cookies_browser: "firefox"
```

### Personlig kontext (valfri)

Fältet `user_context` i config.yml påverkar diagnostiknivå 1 och 2. Beskriv din bakgrund så anpassar Claude analysen:

```yaml
user_context: |
  Jag är pastor och teolog med fokus på NT-exegetik.
  Teologiska preferenser: kontinuationist, egalitär.
```

## Användning

### Chatt-läge

```
/sammanfatta-media https://www.youtube.com/watch?v=XXXXX
```

Eller med naturligt språk:

```
Sammanfatta den här videon: https://...
Berätta om den här videon
```

### Rapport-läge

```
Ge mig en rapport om https://...
Skriv en Word-rapport om https://...
Sammanfatta https://... som en Markdown-rapport
```

### Med diagnostik

```
/sammanfatta-media https://...           — nivå 0, bara sammanfattning
...och ge mig en bedömning              — nivå 1
...med kritisk analys                   — nivå 2
...djävulens advokat                    — nivå 3 (ingen hänsyn till user_context)
```

### Spellista

```
/sammanfatta-media https://www.youtube.com/playlist?list=XXXXX
```

Skillen räknar videorna och frågar om det är fler än 5.

## Diagnostiknivåer

| Nivå | Trigger | Innehåll |
|------|---------|----------|
| 0 | (inget) | Sammanfattning + källista |
| 1 | "diagnostik", "bedömning" | Uppenbara svagheter, jämförelse mot user_context |
| 2 | "kritisk analys", "hitta svagheter" | Hårdare och mer detaljerad än nivå 1 |
| 3 | "djävulens advokat", "skarp kritik" | Ärlig opponent, ignorerar user_context |

## Filstruktur

```
sammanfatta-media/
  SKILL.md                  ← Claude Code-skillsdefinition
  hamta_transkription.py    ← Hämtar VTT-undertexter via yt-dlp
  vtt_till_text.py          ← Konverterar VTT till ren text
  normalisera_namn.py       ← Infogar rätt stavning av egennamn i transkriptionen
  bygg_rapport.py           ← Bygger .docx-rapporter
  main.py                   ← CLI-ingång för manuell körning
  config.yml.example        ← Konfigurationsmall
  lathund-sammanfatta-media.md  ← Snabbreferens
  README.md
```

## Manuell körning (utan Claude Code)

`main.py` kan köras direkt från terminalen:

```bash
# Enskild URL
python ~/.claude/skills/sammanfatta-media/main.py https://www.youtube.com/watch?v=XXXXX

# Från inkorg (kräver inbox_dir i config.yml)
python ~/.claude/skills/sammanfatta-media/main.py --inbox

# Annat språk
python ~/.claude/skills/sammanfatta-media/main.py https://... --lang sv,en
```

## Bot-detection

Om YouTube kräver inloggning kör skillen automatiskt om med `--cookies-from-browser <cookies_browser>`. Ändra webbläsare i config.yml om behov finns (`chrome`, `safari`, `edge`, `brave`, `chromium`).

## Licens

MIT
