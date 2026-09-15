---
name: sammanfatta-media
description: Sammanfattar YouTube-videor och Substack-inlägg med video eller podd (och i framtiden andra mediakällor). Stödjer chatt-svar och filrapporter (docx/md/pdf) med valbar diagnostik på nivå 0–3. Aktiveras av "/sammanfatta-media <URL>" eller naturligspråkliga formuleringar som "sammanfatta denna video", "ge mig en rapport om denna video", "djävulens advokat på den här". Klarar enskild URL, flera URL:er och spellistor.
---

# sammanfatta-media

Återanvändbart arbetsflöde för att sammanfatta YouTube-videor, Substack-inlägg med video eller podd (och framtida mediakällor). Stödjer två leveranslägen, tre inmatningsformer och fyra diagnostiknivåer.

## Konfiguration och sökvägar

Läs `~/.claude/skills/sammanfatta-media/config.yml` i början av varje körning för att hämta `output_dir`, `inbox_dir`, `default_lang`, `cookies_browser` och `user_context`.

Om filen saknas: be användaren kopiera `config.yml.example` till `config.yml` och fylla i sina sökvägar.

**Arbetsminne.** Om `memory_file` är angivet i config.yml: läs filen i början av körningen. Den beskriver hur just den här användaren arbetar — var färdiga rapporter sorteras in, konventioner, filer utanför `output_dir` som skillen uppdaterar, och vad som väntar. Den går före standardbeteendet i den här filen där de skiljer sig. Uppdatera den (datum, avsnitt, logg) när användaren fattar ett beslut som ska gälla framåt; skriv aldrig in engångsdetaljer.

Skriptmapp och kataloger — konstruera plattformsoberoende via Python:

```python
from pathlib import Path

SKILL_DIR       = Path.home() / ".claude" / "skills" / "sammanfatta-media"
TRANSCRIPTS_DIR = Path(config["transcripts_dir"]).expanduser()
OUTPUT_DIR      = Path(config["output_dir"]).expanduser()
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
```

Standardkommandon:

```bash
# Hämta transkription — sparas permanent i transcripts_dir
# Samma kommando för YouTube och Substack; skriptet väljer väg efter adressen.
# Substack: använd sammanfatta-substack-<slug>.txt, där <slug> är sista ledet i URL:en.
python "{SKILL_DIR}/hamta_transkription.py" <URL> \
    --output "{TRANSCRIPTS_DIR}/sammanfatta-<videoid>.txt" \
    --lang <default_lang>

# Normalisera egennamn i transkriptionen (Steg 2b — obligatoriskt)
python "{SKILL_DIR}/normalisera_namn.py" "{TRANSCRIPTS_DIR}/sammanfatta-<videoid>.txt" \
    --mappning "{TEMP_DIR}/namnmappning-<videoid>.json"

# Bygg docx-rapport
python "{SKILL_DIR}/bygg_rapport.py" <output_path>
```

## Triggerigenkänning

Skillen aktiveras av `/sammanfatta-media` följt av URL eller bifogad transkription, samt av naturligspråkliga formuleringar.

### Chatt-läge (utan filgenerering)

- `/sammanfatta-media <URL>`
- "sammanfatta denna video" (med bifogad transkription)
- "berätta om denna video"
- "summera den här videon"

### Rapport-läge (genererar fil)

[video] = platshållare för "denna video/dessa videos/filmerna i denna spellista"

- "ge mig en rapport om [video]"
- "skriv en rapport om [video]"
- "sammanfatta [video] som en rapport"
- "skapa en rapport om [video]"
- "...och skapa en rapport" / "...som en rapport"

### Diagnostik-tillägg

Aktiveras endast om användaren uttryckligen ber om det. Kan begäras i chatt- eller rapport-läge, initialt eller som uppföljning.

| Nivå | Triggers | Innehåll |
|------|----------|----------|
| **0: Ingen** | (inget) | Bara sammanfattning + källista |
| **1: Enkel bedömning** | "diagnostik", "bedömning" | Uppenbara svagheter, lösa trådar. Jämför mot `user_context` om angivet + kort meningsmotståndarperspektiv. |
| **2: Kritisk analys** | "hitta svagheter", "kritisk bedömning", "analys" | Hårdare och mer detaljerad än nivå 1. |
| **3: Skarp kritik** | "skarp kritik", "djävulens advokat", "ge motargument" | Ärlig opponent. Artig men skoningslös i sak. **Inga hänsyn till user_context.** |

## Inmatningsformer (i prioritetsordning)

### Form A — yt-dlp captions (primärväg)

Standardförfarandet för YouTube-videor. Kör `hamta_transkription.py` enligt ovan.

Skriptet försöker i tur och ordning:
1. Manuella undertexter (bäst kvalitet — fackord och namn)
2. Auto-genererade undertexter (språk enligt `default_lang`)
3. Om bot-detection: automatiskt omförsök med `--cookies-from-browser <cookies_browser>`
4. Vid 429, n-challenge eller formatfel: omförsök med android-klienten
5. Om ett språk fällde hela hämtningen: omförsök **ett språk i taget**

**Originalspåret går alltid före översättningar.** YouTube lägger videons faktiska talspråk under `<lang>-orig` och publicerar samtidigt maskinöversättningar under vanliga koder. Skriptet frågar efter båda och prioriterar **alla `-orig`-spår först**, därefter de vanliga — inte parvis per språk. Med `default_lang: "en,sv"` blir ordningen `en-orig, sv-orig, en, sv`. För en svensk video innebär det att `sv-orig` väljs framför den engelska maskinöversättningen, trots att engelska står först i önskelistan.

**Varför det spelar roll:** utan detta hämtas svenskt material antingen inte alls, eller som engelsk översättning av svenskt tal — vilket är oanvändbart för citat och förstör namnnormaliseringen. Källetiketten i utskriften visar vilken väg som användes: `auto`, `auto+cookies`, `auto+android`, `auto+enskilt` eller `auto+enskilt+android`.

**429-fällan.** yt-dlp avbryter *hela* undertexthämtningen när ett enda begärt språk faller. Ett 429 på det första spåret gör alltså att ett fullt fungerande spår längre ner i listan aldrig hämtas — och det slår hårdast mot icke-engelskt material, där översättningen ofta ligger först och originalet sist. Därav steg 5.

Vid framgång: gå till Steg 2b (namnnormalisering) och därefter Steg 3 (sammanfattning). Metadata sparas parallellt i `.meta.json`.

Transkriptionen och dess `.meta.json` sparas permanent i `transcripts_dir`. De ligger kvar efter körningen och kan återanvändas.

**Bot-detection-varning:** Om yt-dlp rapporterar "Sign in to confirm" körs cookies-läget automatiskt. Misslyckas det också: gå till Form C.

### Form A för Substack — Substacks egen transkription

Substack transkriberar själv uppladdade videor och poddavsnitt. yt-dlp når inte den transkriptionen, men den ligger öppet i inläggets API-post. `hamta_transkription.py` känner igen Substack-adresser och hämtar den via `substack.py` — **samma kommando som för YouTube, ingen webbläsare behövs**.

**Adressformer som känns igen:**

- `https://<publikation>.substack.com/p/<slug>`
- `https://open.substack.com/pub/<publikation>/p/<slug>` (delningslänkar)
- `https://substack.com/home/post/p-<id>` och `https://substack.com/@<namn>/p-<id>`
- egen domän med `/p/<slug>` — bekräftas mot API-svaret, så att t.ex. Medium inte tas för Substack

**Vad som hämtas:** API:t (`/api/v1/posts/<slug>`) ger signerade CDN-adresser till en VTT-fil per språk och till en JSON-fil med ordnivådata. VTT används i första hand, med originalspråket före översättningar — samma princip som `-orig` hos YouTube. JSON-filen är reserv. Metadata (titel, bylines, datum, längd, ingress) hämtas ur samma post. Källetiketten blir `substack-vtt` eller `substack-json`.

**Talaretiketter.** Till skillnad från YouTubes textning är Substacks diariserad. Etiketten skrivs vid varje talarbyte:

```
(00:00:01) SPEAKER_00: Välkomna ska ni vara till Teologiska tankar.
(00:00:04) Ett ganska spontant förmiddagssamtal mellan mig och Joel.
(00:00:41) SPEAKER_02: Väldigt kongenialt på något sätt …
```

Etiketten står bara vid byte, inte på varje rad, så att `normalisera_namn.py` fortfarande kan matcha namn som delats över två rader hos samma talare.

- **Koppla etiketter till namn utifrån innehållet**: vem som hälsar välkommen, vem som tilltalas, självbiografiska detaljer. Skriv kopplingen som `speaker_names` i `.meta.json` och ange den i rapportens transkriptionsingress. **Skriv aldrig om etiketterna i själva transkriptionen** — samma princip som för felstavningar.
- **Diariseringen är inte felfri. Kontrollera talaren mot innehållet innan en replik citeras.** Första körningen (Halldorf–Schüldt, 56 min) gav en tredje ”talare” som bara bestod av 15 felattribuerade fragment om 65 ord vid överlappande tal, och flera korta inslag mitt i den andres tur hade fel etikett — bland annat en replik om uppväxten i Pingstkyrkan i Linköping som hamnade hos fel person. Korta inslag kan också vara verkliga inpass; det avgör bara innehållet.

**Utfall och nästa steg:**

| Exit | Betydelse | Gör så här |
|---|---|---|
| 0 | Transkription sparad | Gå till Steg 2b |
| 3 | Inlägget har video/ljud men ingen åtkomlig transkription (ej genererad, eller bakom betalvägg) | Webbläsarreserven nedan, annars Form B — yt-dlp har en Substack-extraktor, så `whisper_fallback.py` fungerar. Svenska kräver KBLab-modellen. |
| 4 | Rent textinlägg utan media | Ingen transkription finns. Läs artikeln (webbläsarens sidtext) och sammanfatta den; spara ingenting i `transcripts_dir`. |

**Webbläsarreserv (när API:t inte räcker).** Öppna inlägget i webbläsaren — Claude in Chrome om det kräver inloggning, annars den inbyggda. Klicka på knappen med texten **Transcript**; då öppnas en behållare med hela texten. Läs den med `document.querySelector('[class*="transcription-full-body-container"]').innerText`. **Matcha på klassnamnets början**: det avslutande ledet (`-LXFSNv`) är en bygghash som skiftar mellan Substacks versioner. Texten består av tidsstämplar i formen `m:ss` eller `h:mm:ss` på egen rad, följda av ett stycke — gör om till `(hh:mm:ss) text` och spara i `transcripts_dir`. Den här vägen **saknar talaretiketter**; föredra därför API-vägen när den fungerar.

**Namnkvalitet.** Substacks transkription är av Whisper-typ och stavar i regel namn bättre än YouTubes autotextning, men svenska samtal behöver ändå Steg 2b — den första körningen gav 26 rättelser (*Timmy Barrett* för T.B. Barratt, *Vagers av Pontus* för Evagrios Pontikos, *pingkyrkan* för Pingstkyrkan).

### Form B — Whisper-fallback

Om Form A misslyckas (inga captions, geo-block, åldersgräns). Kör mot `transcripts_dir`, inte temp — utdata är en arkivpost som alla andra:

```bash
python "{SKILL_DIR}/whisper_fallback.py" <URL> \
    --output "{TRANSCRIPTS_DIR}/sammanfatta-<videoid>.txt" \
    --modell base.en
```

Skriptet hämtar ljudet med yt-dlp och transkriberar med `openai-whisper`. Utdata får samma `(hh:mm:ss)`-format som Form A, så namnnormalisering och rapportbygge fungerar oförändrat.

**Modellval:** `base.en` för tydligt engelskt tal (standard, ungefär fyra minuter per kvart ljud på CPU). `small` för brus, brytning och många egennamn — cirka tre gånger långsammare. För svenska krävs faster-whisper och KBLab-modellen (`KBLab/kb-whisper-large`), se `reference_swedish_whisper.md`.

**Meddela användaren att det tar tid** och kör i bakgrunden vid flera videor. Undvik att pipa körningen genom `tail` — då buffras förloppsutskriften och det går inte att följa arbetet.

**Tyst avkortning.** Whisper har observerats avsluta i förtid utan felmeddelande, i ett fall vid 80 procent av ljudet. Skriptet jämför sista tidsstämpeln med ljudets faktiska längd och larmar vid mer än 15 sekunders differens. **Kontrollera alltid det larmet** — vid utslag är transkriptionen ofullständig och resten måste köras separat med ffmpeg-trim och tidsförskjutning.

**Bonus värd att känna till:** Whisper stavar egennamn betydligt bättre än YouTubes auto-textning. I en körning över tolv videor behövde Whisper-transkriptionerna noll namnrättelser medan de auto-textade behövde 55. Steg 2b behövs ändå, men blir oftast tomt för Form B.

### Form C — Manuell inklistring

Sista utväg om Form A och B misslyckas. Be användaren:
> "Klistra in transkriptet — öppna YouTube, klicka på `...mer` under videon och sedan på `Visa transkription`, markera och klistra in i nästa meddelande."

## Flera videor och spellistor

Vid flera URL:er:
1. Identifiera alla videor, bevara ordningen
2. Hämta metadata och transkription per video (Form A för var och en)
3. Sammanfatta varje video separat
4. Skapa samlad syntes
5. Skapa gemensam källista med videoreferenser och timestamps

### Spellistehantering

```bash
yt-dlp --flat-playlist --print "%(playlist_index)s|%(title)s|%(duration)s|%(upload_date)s|%(id)s" <URL>
```

- **≤ 5 videor**: bearbeta alla utan att fråga
- **> 5 videor**: räkna och fråga hur användaren vill fortsätta

Svarsformer användaren kan ge: "de fem första", "nummer 6–10", "alla", "visa mig en lista".

**Numrerad lista** (när användaren ber om "lista"):
```
Spellistan innehåller N videor:
1. [Titel] — 12:34 — 2025-03-15
2. [Titel] — 1:02:11 — 2025-03-22
```

**Enskild URL i spellista:** Om URL:en innehåller `&list=...` men pekar på en enskild video: bearbeta bara den videon.

## Metadata och videobeskrivning

Samla för varje video:
- titel, kanal, URL, publiceringsdatum, längd
- videobeskrivning och dess inbäddade länkar
- kapitel/timestamps (om tillgängliga)
- spellisteposition (om relevant)
- för Substack: bylines (i `uploader`), inläggets underrubrik (i `description`) och talarkopplingen (`speaker_names`, se Form A för Substack)

**Visuell separation:** Skilj alltid videobeskrivning, transkription och Claudes sammanfattning med egna H2/H3-rubriker. Blanda dem aldrig i samma stycke. Citat ur videobeskrivningen: blockquote eller indenterat citat.

## Arbetsflöde

### Steg 1 — Identifiera läge och behov

Läs användarens meddelande och avgör:
- **Leveransläge**: chatt eller rapport?
- **Diagnostiknivå**: 0, 1, 2 eller 3?
- **Inmatning**: URL eller bifogad transkription?
- **Antal videor**: en eller flera?

Om användaren säger "rapport" utan format, fråga:
```
Vilket format vill du ha rapporten i?
- Word (.docx)
- Markdown (.md)
- PDF (.pdf)
```
Fråga inte om format är redan angivet. Fråga inte om diagnostiknivå.

### Steg 2 — Hämta transkription

Följ Form A → B → C ovan.

**Vid saknad transkription**: säg det tydligt. Gör ingen fullständig analys som om transkriptionen funnits. Fortsätt med metadata och beskrivning om möjligt.

### Steg 2b — Namnnormalisering (OBLIGATORISKT efter varje hämtning)

Undertexter förvanskar regelmässigt egennamn — *Pchesca* för Prochaska, *Farnbeck* för Farnebäck, *Zaprruder* för Zapruder. Transkriptionerna sparas permanent och ska gå att söka i långt senare, men den som söker på det rätta namnet hittar aldrig den förvanskade formen. Därför infogas rätt stavning inom hakparentes direkt efter felstavningen:

```
Pchesca [Prochaska]
```

Vid osäker identifiering — rimlig gissning utifrån sammanhanget, men inte säkerställd — läggs frågetecken till:

```
Pchesca [Prochaska ?]
```

**Felstavningen står kvar orörd.** Originalet skrivs aldrig om, och ingenting markeras med `[sic]`. Hakparentesen är ett tillägg, inte en rättelse.

**Omfattning — allt som är egennamn:**

- personer (talare, forskare, författare, omnämnda)
- organisationer, företag, myndigheter, samfund, kanaler och plattformar
- geografiska namn — städer, länder, regioner, byggnader, institutioner
- bibelböcker och bibliska namn (personer, folk, platser)
- verk — boktitlar, filmer, poddar, artiklar, album
- märkesnamn, produkter, tekniska begrepp med egennamnskaraktär

Vanliga substantiv normaliseras inte. Rena hörfel utan egennamnskaraktär (*helped built*, *sensemaking* felstavat) lämnas orörda.

**Arbetsgång:**

1. Läs igenom hela transkriptionen och notera varje förvanskat egennamn.
2. Identifiera rätt form utifrån sammanhang, videobeskrivning, metadata och egen sakkunskap. Sök på nätet när det behövs och är möjligt.
3. Bygg en mappningsfil i JSON i temp-katalogen — **inte** i `transcripts_dir`:

```json
[
  {"fel": "Pchesca",       "ratt": "Prochaska"},
  {"fel": "Farnbeck",      "ratt": "Farnebäck"},
  {"fel": "Brad Zadznney", "ratt": "Brandy Zadrozny", "osaker": true},
  {"fel": "Revelations",   "ratt": "Revelation", "skiftlagesberoende": true}
]
```

4. Kör först med `--torrkorning` och läs träfflistan. Kör sedan skarpt mot den sparade transkriptionen. Skriptet skriver över filen i `transcripts_dir` — det är den arkiverade, sökbara versionen som ska bära annoteringarna.
5. Kontrollera utskriften. Skriptet redovisar antal infogningar per post och varnar för poster utan träff. En post utan träff betyder oftast felstavad sökterm i mappningen eller att en längre post redan konsumerat förekomsten.
6. **Läs igenom de infogade annoteringarna i sitt sammanhang** innan du går vidare. Falska träffar upptäcks bara så.

**Skriptets egenskaper:** skiftlägesokänslig matchning med bevarat originalskiftläge (undertexter växlar ofta till VERSALER), längsta felstavningen först, engelsk genitiv hanterad, och idempotent — en omkörning bygger inte på fler hakparenteser. Mellanslag i en post matchar godtyckligt blanktecken, inklusive radbrytning, `&nbsp;` och inskjuten tidsstämpel, eftersom textningen bryter namn mitt itu: `Allen (00:15:50) Dedio` är samma namn som `Allen Dedio`.

**Fullnamn och kortform i samma mappning är säkert.** Alla poster matchas i ett enda svep, längsta grenen vinner, så `Chris Valatin` och `Chris` kan båda stå med. Den långa konsumerar sina förekomster och den korta annoterar bara de fristående. Ta med båda när textningen växlar mellan formerna — annars blir de lösa förnamnen osökbara.

**Skiftlägeskänsliga poster.** Sätt `"skiftlagesberoende": true` för ord som bara är egennamn när de är versaliserade. Utan flaggan annoteras *gnostic revelations* som bibelboken. Samma problem gäller ord som *Word*, *Way*, *Rock* och *Church*.

**Annotera inte enbart versalfel.** Sökning är normalt skiftlägesokänslig, så *xp media* hittas redan av den som söker *XP Media*. Hakparenteser ska reserveras för poster där bokstäverna är fel — annars dränks de verkliga rättelserna i brus.

**Osäkerhetsbedömning.** Sätt `"osaker": true` när identifieringen är en rimlig men obekräftad slutledning. Var frikostig med frågetecknet: ett felaktigt tvärsäkert namn i arkivet är värre än ett ärligt frågetecken. Markeringen ska stämma överens med källstatusen *sannolik identifiering* i källistan.

**Vid flera videor:** en mappningsfil per video. Samma person kan förvanskas olika i olika textningar.

**Gäller alla inmatningsformer.** Även transkript som klistrats in manuellt (Form C) normaliseras innan de sparas eller citeras.

**Nedströms:** sammanfattning, källista och rapportens transkriptionssektion bygger alla på den normaliserade texten. Citerar du transkriptionen ordagrant i löptext kan hakparentesen utelämnas när rätt namn redan framgår av sammanhanget — men i rapportens fullständiga transkriptionssektion ska den alltid stå kvar.

### Steg 3 — Producera sammanfattning

Standardformat:
- **Tes** — videons huvudpåstående (1–2 meningar)
- **Huvudlinjer** — numrerade avsnitt som speglar videons struktur
- **Slutsats** — vad videon vill driva

Längd: anpassad till videons längd och komplexitet.

**Vid flera videor**: sammanfatta varje separat, lägg sedan till samlad syntes med:
- Gemensamma teman och argumentationslinjer
- Skillnader och inbördes spänningar
- Gemensamma källor och referenser
- En övergripande linje (om urskiljbar)

**Chatt-läge utan diagnostik**: avsluta med kort neutral fråga om användaren vill ha rapport eller diagnostik. Inte säljande — bara informativt.

### Steg 4 — Diagnostik (endast om begärd)

**Nivå 1–2**: om `user_context` är angivet i config.yml, anpassa analysen efter det. Påpeka svagheter och lösa trådar, flagga och förklara, argumentera inte emot.

**Nivå 3**: agera som ärlig opponent. Motpartens bästa argument utan kompromiss. Ignorera `user_context`.

Strukturera efter vad som faktiskt är problematiskt. Vanliga rubriker:
- Forskningsläget framställs mer enigt än det är
- Specifika tolkningar som är omstridda
- Metodologiska problem
- Polemisk inramning
- Vad som inte diskuteras
- Eventuella faktafel

### Steg 5 — Rapport (endast om begärd)

Default-struktur:
1. **Titelsida** — videons titel, URL, datum, rapportnivå
2. **Sammanfattning** (från Steg 3)
3. **Kritisk bedömning** (om diagnostik begärdes)
4. **Källor** — alltid videoförankrade; Claudes egna källor endast vid diagnostik
5. **Transkription** — alltid med som sista sektion, med rubrik "Transkription" och källa angiven. Använd den namnnormaliserade versionen från Steg 2b, och nämn i ingressen att hakparenteserna är tillagda rätta stavningar av egennamn medan övriga hörfel är bevarade. Har transkriptionen talaretiketter (Substack), ange i ingressen vilken etikett som är vem och att enstaka repliker kan vara felattribuerade

**Rapportbygge (docx):** Anropa `bygg_rapport.py` med en strukturerad dict.

```python
import sys
sys.path.insert(0, str(SKILL_DIR))
from bygg_rapport import bygg_rapport

data = {
    "titel": "...",
    "metadata": [("Källa: ", "YouTube"), ("URL: ", url), ...],
    "sektioner": [...],
}
bygg_rapport(data, output_dir / "rapport-<slug>.docx")
```

**Slug-generering:**
- Enskild video: videons titel
- Spellista: spellistans titel
- Flera videor utan gemensam spellista: första videons titel + `-plus-N`

Normalisering: gemener, å→a, ä→a, ö→o, mellanslag→bindestreck, ta bort specialtecken, max ~60 tecken.

**Markdown (.md):** YAML front matter med svenska nyckelnamn (*språk*, *rapportnivå*, *transkriptkälla*). Filnamn: ASCII-normaliserat.

**PDF:** Konvertera från docx via pdf-skillen om tillgänglig.

### Steg 5b — Språklig genomgång (OBLIGATORISKT som sista steg för svenska rapporter)

Gäller alla rapporter på svenska — alltid, utan att fråga. Genomgången görs på texten **innan** Python-skriptet körs eller filen genereras. Verkställ ändringarna direkt i skriptkoden; presentera inte diagnostiken separat.

Återkommande fynd att leta efter och åtgärda:

- **Hybridkonstruktioner med engelska förled** (*ghostskrev*, *ghostwriting-karriären*, *ghostwriting-uppdrag*) → ersätt med etablerad svensk form (*spökskrev*, *karriären som spökskrivare*, *spökskrivaruppdrag*)
- **Påhittade försvenskningar** (*serieabusare*, *predikoutline*, *attenderar*) → etablerad term eller kursiverat original
- **Inkonsekvent transliterering** (*kerubim* vs *cherubim*) → välj ett och håll konsekvent
- **Engelska fraser inbäddade i svensk löptext** → översätt eller markera tydligt
- **Grammatikfel i genus och numerus** (*ett sträckt hand* → *en sträckt hand*; *ett uppgor* → *en uppgörelse*)
- **Oidiomatiska metaforer**
- **Raka citattecken** → typografiska (hanteras av bygg_rapport automatiskt i docx)
- **Faktafel i ordagranna citat** → dubbelkolla mot transkriptet
- **YAML-nyckelnamn** → ska ha svenska bokstäver i .md-rapporter

Användaren ser den städade versionen direkt — aldrig ett utkast.

### Steg 6 — Leverans

- **Chatt-läge**: sammanfattningen direkt i chatten
- **Rapport-läge**: presentera filsökvägen och en kort sammanfattande mening. Inga långa förklaringar.

## Källidentifiering

Samla källor löpande under transkriptionsgenomgången. Namnnormaliseringen i Steg 2b och källidentifieringen gör i praktiken samma arbete — gör dem i ett svep och låt mappningsfilen och källistan stämma överens. Identifiera:
- **Forskare och verk** — även förvanskat uttal. Ange sannolik identifiering vid osäkerhet; den statusen ska motsvara `"osaker": true` i namnmappningen.
- **Primärkällor** — bibelställen, apokryfer, pseudepigrafer, kyrkofäder, rabbinsk litteratur
- **Webbplatser och poddar**

Källista med tydliga underrubriker. Kursiv för boktitlar, citationstecken för artiklar.

## Källstatus

Märk varje källa med en eller flera etiketter (ej ömsesidigt uteslutande, kombinera med semikolon):

- explicit nämnd
- från videobeskrivning
- sannolik identifiering
- oklar hänvisning
- person nämnd, men inte nödvändigtvis använd som källa

### Presentation

Primär form — prosa eller bulletlista under underrubriker:
> Boyarin, Daniel. *Border Lines*. (Explicit nämnd; central referens.)
> Hurtado, Larry W. *Lord Jesus Christ*. (Sannolik identifiering — videon säger bara "Hurtado".)

Sammanfattande översikt sist i källsektionen:

| Källa | Typ | Video | Timestamp | Kontext | Status | Länk/identifierare |
|---|---|---|---:|---|---|---|
| Boyarin, Daniel. *Border Lines*. | Forskning | 1 | 28:22 | Anförs för tesen att... | Explicit nämnd | ISBN 978-0812219869 |

Oversiktstabellen är obligatorisk vid flera videor, valfri vid enskild video.

## Inkorg (batch-dispatch)

Om `inbox_dir` är angivet i config.yml och användaren ber om det: läs `.txt`-filer i inkorgsmappen (en URL per rad), bearbeta i ordning. Rapporter sparas i `output_dir`.

## Påminnelser

- Anpassa expertisen efter videons ämne — inte bara teologi.
- Bevara transkriptionsfel som de är — skriv aldrig om originaltexten och markera aldrig med [sic]. Enda undantaget är hakparenteserna med rätt stavning av egennamn enligt Steg 2b, som läggs till utan att felstavningen rörs.
- Filnamn: `[a-z0-9-]+\.docx` (eller motsv.). Inga diakritiska tecken, inga understreck.
- IBM Plex Sans i alla Word-dokument om användaren inte säger annat.
- Kör `pip install -U yt-dlp` vid behov — YouTube-API:t ändras ofta.
