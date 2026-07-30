---
name: humaniora-forskningsoversikt
description: >
  Kartlägger forskningsläget inom humaniora — teologi (exegetik, systematisk teologi, kyrkohistoria),
  filosofi, historia och religionssociologi — via Consensus och Scholar Gateway. Svar i chatten,
  docx som tillval. Använd när Lars säger "gör en forskningsöversikt om X", "vad säger forskningen
  om X", "hur ser forskningsläget ut kring X", "kartlägg debatten om X", "vilka positioner finns
  om X", "orientera mig i forskningen om X", "status quaestionis för X", eller engelska
  motsvarigheter som "state of research on X". Trigger också när han pekar på ett tema han ska
  predika, undervisa eller skriva om och frågar vad som är skrivet, eller när han vill veta vilka
  forskare som driver vilken tes. Trigger INTE för enskilda uppslagsfrågor där han bara vill ha en
  artikel eller ett snabbt svar — det är en vanlig Consensus-sökning. Denna skill är till när han
  vill ha djup, karta och syntes.
---

# Forskningsöversikt för humaniora

Producerar en orienterande kartläggning av ett forskningsläge inom humaniora. Målet är inte en
färdig forskningsöversikt utan en **startpunkt**: tillräckligt för att Lars ska kunna gå vidare på
egen hand med rätt sökord, rätt namn och rätt uppfattning om var striden står.

Svara på frågans språk. Svensk fråga ger svenskt svar; engelsk fråga ger engelskt svar. Citat
återges på originalspråk.

---

## Fas 0 — Källkritisk ram (obligatorisk, före första sökningen)

Skriv ut detta i chatten innan någon sökning körs. Det är inte en brasklapp utan ett resultat:

> **Vad verktygen ser.** Consensus indexerar Semantic Scholar, PubMed, Scopus och ArXiv.
> Scholar Gateway söker i en fulltextkorpus. **Ingetdera indexerar ATLA Religion Database,
> Index Theologicus (IxTheo) eller RAMBI** — de tre databaser som bär teologisk forskning.
> Monografin, som är humanioras dominerande genre, saknas nästan helt. Kommentarserier,
> uppslagsverk och konfessionella förlag saknas.
>
> **Vad det gör med bilden.** Sökningarna överrepresenterar open access-tidskrifter, särskilt
> sydafrikanska (HTS Teologiese Studies, Verbum et Ecclesia, In die Skriflig, Pharos) och MDPI
> (*Religions*). De underrepresenterar anglosaxisk och tyskspråkig monografiforskning.
> **En tunn träffbild är därför inte belägg för en forskningslucka.**

Detta stycke ska också in i det slutliga dokumentet, som avsnitt 2 — inte som appendix.

---

## Verktyg och roller

**`Consensus:search`** — primärverktyg. Ger titel, författare, år, citeringsantal, journal och URL.
Rate limit: **1 sökning per sekund**. Kör sekventiellt, aldrig parallellt. Vänta på att varje
resultat kommit in och innehåller data innan nästa skickas.

**Nivådetektion:** kontrollera första svaret. Står det "showing top 10" eller finns ett
uppgraderingsmeddelande är kontot på fri nivå (10 träffar/sökning). Upp till 20 träffar betyder Pro.
Registrera taket och rapportera det vid checkpoint.

**Citeringskrav:** Consensus kräver att träffar citeras med numrerade referenser och att titlarna
hyperlänkas till den fullständiga URL:en. Korta aldrig ned en URL. Verktygets
uppgraderingsmeddelande ska återges sist i chattsvaret.

**`Scholar Gateway:semanticSearch`** — komplement, används för två saker Consensus är dålig på:

1. **Förbigående omnämnanden.** Fulltextsökning hittar passager som nämner ett fenomen i förbigående
   även när ingen artikel handlar om det. Avgörande för smala studieobjekt (enskilda organisationer,
   personer, händelser inom samtida rörelser).
2. **Formuleringar och begrepp** snarare än ämnen — när frågan gäller hur en term används, inte vad
   som skrivits om ett ämne.

Verktyget kräver godkännande per anrop och kan neka. **Om det nekas: notera det, fortsätt med
Consensus, och redovisa i sökprotokollet att fulltextspåret uteblev.** Låtsas aldrig att det kördes.

---

## Datadisciplin

- Citera bara arbeten som verktygen faktiskt returnerat i den här sessionen. Kompletterar du med
  modellkunskap ska det märkas `[ej från Consensus/Scholar Gateway — modellkunskap]` och räknas bort
  från alla siffror.
- **Undantag med krav på märkning:** när standardverket i ett fält är en monografi som verktygen inte
  ser, ska verket ändå namnges — med märkning. Att utelämna Barths *Kirchliche Dogmatik* ur en
  översikt över försoningsläran därför att Consensus inte indexerar den vore en värre felrapportering
  än att ta med den märkt.
- Ger en sökning färre träffar än väntat, säg det uttryckligen och tolka det: nischad terminologi,
  fel språk, eller genuin lucka?
- Samma källkrav i chatten som i dokumentet.
- Håll tre räknare igenom hela arbetet: **sökningar körda**, **unika arbeten mottagna**
  (deduplicerade), **arbeten citerade**.

---

## Felhantering

1. Vid fel: vänta 3 sekunder, gör om samma sökning en gång.
2. Logga varje fel — vilken sökning, vilket felmeddelande, om omförsöket lyckades.
3. Efter tre fel i rad: sluta söka, förklara läget, fråga hur Lars vill gå vidare.
4. Hoppa aldrig tyst över en misslyckad sökning. Notera den som en lucka.

---

## Fas 1 — Rekognosering

Kör **en till två** breda sökningar i Consensus. Om ämnet har tysk eller fransk forskningstradition
(dogmatik, kyrkohistoria, filosofi, GT-exegetik), kör den andra på det språket.

Läs abstracten för att fånga:

- Vilken terminologi forskarna faktiskt använder — inklusive latinska och tyska fackuttryck
- Vilka positioner som finns och vilka namn som bär dem
- Vilka konfessionella och institutionella hemvister som syns
- Vilka delfrågor som visar sig vara omstridda

Notera citeringsantal, men **använd inte biomedicinska heuristiker.** Citeringar per år premierar
färska tidskriftsartiklar och missar att ett fältdefinierande verk från 1977 kan ha tvåsiffrigt
registrerat citeringsantal. Behandla högt citeringsantal som en signal bland flera, aldrig som mått
på betydelse.

---

## Fas 2 — Klassificera frågan och läs rätt referensfil

Bestäm vilken typ frågan är och **läs motsvarande fil i `references/` innan du planerar sökningarna.**
Filen innehåller axlar, genremål, sökordsvokabulär, forskningshistoriska vändningar och specifika
täckningsvarningar.

| Typ | Gäller | Läs |
|---|---|---|
| **A. Exegetisk** | En text, en perikop, en term, ett bibliskt motiv | `references/exegetisk.md` |
| **B. Systematisk-teologisk** | En lära, ett begrepp, en teologisk position | `references/systematisk.md` |
| **C. Historisk** | En händelse, en period, en rörelse i det förflutna | `references/historisk.md` |
| **D. Samtida rörelse** | Nu levande rörelser, samfund, religionssociologi | `references/samtida-rorelse.md` |

Filosofiska frågor följer B; allmänhistoriska följer C.

**Blandfrågor är vanliga.** "Hur har Wrights parusisyn tagits emot i svensk frikyrklighet" är B och D
samtidigt. Välj en primärtyp för struktur, läs båda filerna, och säg vid checkpoint att frågan
spänner över två typer. Hellre uttalad blandning än påtvingad renhet.

---

## Checkpoint — bekräfta innan fler sökningar

Skriv ut, kortfattat och skannbart:

**1. Vad rekognoseringen visade** — 3–4 meningar. Vilken terminologi används? Vilka positioner
syns? Vad är oväntat?

**2. Klassificering och delområden** — markdown-tabell:

| Delområde | Frågetypens axel | Vad jag söker efter | Förväntad täckning |
|---|---|---|---|
| ... | ... | ... | God / Tunn / Obefintlig |

Kolumnen **förväntad täckning** är en förhandsgissning om vad Consensus och Scholar Gateway rimligen
kan leverera för just det delområdet. Gissningen blir ofta fel. Det är poängen — en felaktig gissning
som Lars korrigerar här är mer värd än en oreflekterad sökning.

**3. Nivådetektion** — rapportera upptäckt tak (10 eller 20 träffar per sökning) och vad det innebär
för total täckning.

**4. Sökdjup och bekräftelse** — fråga hur djupt Lars vill gå:

```javascript
sendPrompt("Snabbskanning — 5 sökningar")
sendPrompt("Standard — 10 sökningar")
sendPrompt("Djupdykning — 20 sökningar")
```

```javascript
sendPrompt("Kör på")
sendPrompt("Jag vill justera delområdena först")
sendPrompt("Lägg till ett delområde om ...")
sendPrompt("Byt ut ett av delområdena")
```

Vänta på svar. Vid justering: uppdatera tabellen och bekräfta på nytt.

---

## Fas 3 — Genomför sökningarna

Sekventiellt, en i taget, minst en sekund emellan. Bekräfta att varje resultat kommit in innan nästa.

### Budget

**Snabbskanning (5):** en per delområde. Inga forskningshistoriska eller motståndssökningar.

**Standard (10):**
- 5 delområdessökningar
- 2 **status quaestionis-sökningar** — `"status quaestionis [ämne]"`, `"Forschungsbericht [ämne]"`,
  `"history of research [ämne]"`, `"[ämne] handbook"`, `"[ämne] companion"`.
  **Sök aldrig på "systematic review" eller "meta-analysis".** De genrerna finns inte här.
- 1 **motståndssökning** — `"critique of [position]"`, `"response to [namn]"`, `"[position] reassessed"`.
  Syftet är att få debatten, inte bara den dominerande positionen.
- 1 **språksökning** — samma delområde på tyska eller franska
- 1 **Scholar Gateway-sökning** på det smalaste delområdet, formulerad som hel fråga

**Djupdykning (20):**
- 5 delområdessökningar
- 4 status quaestionis- och handbokssökningar
- 3 motståndssökningar
- 2 språksökningar (tyska, franska)
- 2 epokdelade sökningar på det viktigaste delområdet (`year_max` och `year_min`) för att fånga
  metodvändningen
- 2 Scholar Gateway-sökningar
- 2 reserv för trådar som dyker upp under arbetet

### Vad som ska spåras genom alla sökningar

**1. Återkommande arbeten.** Ett verk som dyker upp i tre av fem sökningar är sannolikt bärande.

**2. Positioner och deras företrädare.** Notera vem som driver vilken tes — inte bara vem som
publicerar mycket.

**3. Oenighet.** Vem motsäger vem, och på vilken grund. **Detta är nyttolasten i humaniora.**
En översikt som listar arbeten utan att visa var striden står har missat uppgiften.

**4. Konfessionell och institutionell hemvist.** I teologi är detta primär tolkningsdata, inte
bakgrundsbrus. Notera när en position sammanfaller med en tradition — och notera lika noga när den
inte gör det, eftersom det ofta är det intressanta.

**5. Metodologisk vändning.** Humaniora skiftar genom metodbyten, inte genom evidensackumulation.
Se referensfilen för det aktuella fältets vändningar.

**6. Terminologiskt skifte.** Äldre litteratur använder andra termer. Notera båda uppsättningarna —
en sökning på enbart moderna termer missar grundläggande äldre arbeten.

---

## Fas 4 — Leverera

**Chattsvar först, alltid.** En kartläggning i löpande text med tabeller där de hjälper. Ingen docx
om Lars inte ber om det. Avsluta med en kort fråga om han vill ha den som Word-dokument.

Formatera enligt Consensus citeringskrav: numrerade referenser inline, hyperlänkade titlar,
fullständiga URL:er, referenslista sist, och verktygets uppgraderingsmeddelande allra sist.

### Om docx begärs

Läs `/mnt/skills/public/docx/SKILL.md` innan du genererar. Typsnitt **IBM Plex Sans**.
Filnamn: enbart `[a-z]`, `[0-9]` och bindestreck; å/ä → a, ö → o, ü → u. Spara i
`/mnt/user-data/outputs/`. Validera med `python scripts/office/validate.py` och presentera med
`present_files`.

Erbjud en språklig genomgång som separat steg efter leverans — gör den inte automatiskt.

---

## Dokumentstruktur

1. **Frågeställning och avgränsning**
2. **Korpustäckning och blindfläckar** — texten från fas 0, konkretiserad för just detta ämne.
   Vilka databaser saknas, vilka genrer saknas, vad det gör med bilden.
3. **Läsordning** — 5–7 arbeten i den ordning en nykomling bör ta dem. Börja med bästa
   forskningsöversikt eller handboksartikel; sedan det verk som definierade fältet; sedan 2–3 som
   visar var forskningen står nu; avsluta med ett som visar var striden är olöst. För varje: titel som
   hyperlänk, författare och år, en mening om vad arbetet bidrar med, en mening om vad man ska titta
   efter. **Om standardverket är en monografi som verktygen inte ser, ta med det ändå — märkt.**
4. **Forskningsläget: positioner och företrädare** — ordnat **efter position, inte efter författare**.
   Varje position får: kärntes, främsta företrädare, konfessionell eller metodologisk hemvist,
   starkaste argument, vanligaste invändning.
5. **Debattkartan** — vem argumenterar mot vem, om vad, och vad frågan hänger på. En tabell eller
   kort punktlista räcker. Var explicit när en debatt har tystnat utan avgörande.
6. **Forskningshistorisk utveckling** — metodvändningar med årtal, inte evidensackumulation.
   Terminologiskt skifte noteras här.
7. **Delområdesguider** — ett avsnitt per delområde: vad forskningen visar, 3–5 nyckelarbeten med
   hyperlänk, sökord på svenska, engelska och tyska, samt 2–3 färdiga söksträngar. Söksträngarna ska
   vara skrivna för **ATLA (EBSCO-syntax) och IxTheo**, inte PubMed.
8. **Luckor och obesvarade frågor** — i humanioras termer: otillgängliga eller oedierade primärkällor,
   oöversatt material, positioner som hävdas men inte argumenteras, kritik som aldrig besvarats,
   debatter som tystnat, angränsande fält vars resultat inte integrerats. För varje: varför det spelar
   roll. Skriv aldrig "mer forskning behövs".
9. **Primärkällor att gå till** — det verktygen inte kan leverera. Bibeltext och textutgåvor,
   arkiv, rörelsers egna publikationer, editioner, digitaliserade samlingar. Namnge dem konkret och
   ange var de finns.
10. **Bibliografi** — alfabetiskt på första författarens efternamn. `Författare (år). Titel. Tidskrift.`
    plus klickbar länk. Varje inline-citat ska ha en post; varje post ska vara citerad minst en gång.
11. **Sökprotokoll** — tabell med sökning, filter, antal träffar, status. Plus räknarna, upptäckt
    nivå, delområden med tunn täckning, och om Scholar Gateway nekades.
