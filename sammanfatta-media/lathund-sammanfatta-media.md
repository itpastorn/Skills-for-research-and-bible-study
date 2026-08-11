# Lathund: sammanfatta-media

Skill i Claude Code för att sammanfatta YouTube-videor (och framtida mediakällor).
Uppdaterad: 2026-05-13.

---

## Starta en körning

### Enklaste sättet
```
/sammanfatta-media https://youtube.com/watch?v=...
```

### Naturligspråk fungerar också
- "sammanfatta denna video: [URL]"
- "berätta om den här videon: [URL]"
- "ge mig en rapport om [URL]"

---

## Två leveranslägen

| Läge | När | Hur du triggar |
|---|---|---|
| **Chatt** | Du vill se sammanfattningen direkt | Bara URL, inget mer |
| **Rapport** | Du vill spara resultatet som fil | "...som en rapport" / "ge mig en rapport om..." |

När du ber om rapport frågar Claude vilket format du vill ha:
- **Word (.docx)** — standard, IBM Plex Sans, A4
- **Markdown (.md)**
- **PDF**

Rapport sparas i den mapp du angett som `output_dir` i `config.yml`.

---

## Diagnostiknivåer

Lägg till efter URL:en eller som uppföljning efter att ha läst sammanfattningen.

| Nivå | Vad du skriver | Vad du får |
|---|---|---|
| **0** | (inget) | Bara sammanfattning |
| **1** | "diagnostik" / "bedömning" | Uppenbara svagheter, lösa trådar. Jämförelse mot din `user_context` + meningsmotståndarperspektiv. |
| **2** | "hitta svagheter" / "kritisk analys" | Hårdare och mer detaljerad än 1. |
| **3** | "djävulens advokat" / "skarp kritik" / "ge motargument" | Ärlig opponent. Skoningslös i sak. `user_context` läggs åt sidan. |

**Exempel — diagnostik som uppföljning:**
```
/sammanfatta-media https://...
[läser sammanfattningen]
"Ge mig djävulens advokat på det här"
```

---

## Spellistor och flera videor

```
/sammanfatta-media https://youtube.com/playlist?list=...
```

- **≤ 5 videor:** Bearbetas alla automatiskt.
- **> 5 videor:** Claude räknar och frågar hur du vill fortsätta.

Svar du kan ge:
- "de fem första"
- "nummer 6–10"
- "alla"
- "visa mig en lista" — får titlar, längder och datum som beslutsunderlag

---

## Inkorg (batch-dispatch)

Om du angett `inbox_dir` i `config.yml`:

1. Lägg en `.txt`-fil i inkorgsmappen med en URL per rad
2. Kör `/sammanfatta-media --inbox` i Claude Code
   — eller: `python main.py --inbox` i terminalen

Raderna tas bort automatiskt när de bearbetats.

---

## Om captions saknas

Claude försöker i ordning:

1. **yt-dlp manuella undertexter** (bäst kvalitet)
2. **yt-dlp auto-genererade undertexter** (språk enligt `default_lang` i config.yml)
3. **Whisper-fallback** — hämtar audio och transkriberar lokalt (tar tid, byggs vid behov)
4. **Manuell inklistring** — Claude ber dig öppna YouTube → `...mer` → `Visa transkription`

---

## Vad som sker automatiskt

- **Metadata** hämtas alltid (titel, kanal, datum, kapitel, videobeskrivning)
- **Transkription sparas** permanent i `transcripts_dir` (config.yml) — återanvänds vid behov
- **Namnnormalisering** körs alltid direkt efter hämtningen: förvanskade egennamn får rätt stavning inom hakparentes, så att arkivet går att söka i. Felstavningen står kvar orörd.
  - Säker identifiering: `Pchesca [Prochaska]`
  - Osäker gissning: `Pchesca [Prochaska ?]`
  - Gäller personer, organisationer, orter, länder, bibelböcker, verk — allt som är egennamn
- **Transkription bifogas** alltid som sista sektion i rapporter
- **Källidentifiering** — forskare, bibelreferenser, poddar identifieras och märks med status (*explicit nämnd*, *sannolik identifiering*, etc.)
- **Språklig genomgång** körs automatiskt före rapportleverans (du ser den städade versionen direkt)

---

## Snabbreferens: filplatser

| Vad | Var |
|---|---|
| Skript | `~/.claude/skills/sammanfatta-media/` |
| Inkorg | Värdet av `inbox_dir` i `config.yml` |
| Rapport-utdata | Värdet av `output_dir` i `config.yml` |
| Skill-definition | `~/.claude/skills/sammanfatta-media/SKILL.md` |

---

## Typiska körningar

```
# Snabb titt i chatten
/sammanfatta-media https://youtu.be/ABC123

# Rapport direkt
/sammanfatta-media https://youtu.be/ABC123 — ge mig en rapport som Word

# Chatt + diagnostik efteråt
/sammanfatta-media https://youtu.be/ABC123
[läser]
djävulens advokat

# Rapport med skarp diagnostik direkt
/sammanfatta-media https://youtu.be/ABC123 — rapport med djävulens advokat
```
