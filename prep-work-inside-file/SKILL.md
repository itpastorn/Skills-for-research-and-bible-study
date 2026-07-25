---
name: prep-work-inside-file
description: >-
  Skriver ut startinstruktioner som Lars Gunther kan kopiera och klistra in i
  Claude AI inuti Excel när han ska arbeta direkt **i** en av Timelines-filerna.
  Trigger när Lars säger "jag vill jobba i tidsaxeln", "jag vill jobba i
  personfilen", "/prep-work-inside-file", "starta arbete i [filnamnet]",
  "förbered Excel-Claude för [tidsaxeln/personfilen]" eller liknande
  formuleringar med prepositionen "i". VIKTIGT — trigga INTE skillen om Lars
  säger "jobba **med** tidsaxeln/personfilen", då är det vanlig Cowork-kontext
  (denna miljö) där inga särskilda startinstruktioner behövs. Distinktionen
  mellan "i" (inuti Excel-Claude) och "med" (Cowork-Claude) är central.
---

# Förberedelse för arbete inuti Excel-fil

## Syfte

Lars använder Claude AI både i Cowork mode (denna miljö, med filsystemtillgång) och **inuti Excel**. När han ska jobba i en av Timelines-filerna behöver han ett block med startinstruktioner att klistra in i Excel-Claude så att den vet projektets karaktär, regler och arbetsstil.

Skillen skriver ut blocket; Lars kopierar och klistrar.

## Steg 1 — Avgör vilken fil

Läs Lars triggerfras:

- Innehåller "tidsaxeln" eller `timeline-church-and-other-history-head.xlsx` → använd **Block A** nedan.
- Innehåller "personfilen" eller `timeline-individuals-institutions-movements.xlsx` → använd **Block B** nedan.
- Otydligt — fråga Lars vilken fil.

## Steg 2 — Skriv ut motsvarande block

Skriv ut hela blocket i en code-block (```) så att Lars enkelt kan markera och kopiera. Säg därefter en kort mening om att han kan klistra in det i Excel-Claude.

Skriv inte ut båda blocken samtidigt — bara det som efterfrågades.

## Princip — vad som inte upprepas

Varje fil har redan AI-instruktioner inuti sig:

- **Tidsaxeln**: rad 3 i fliken Tabellen ("För AI") innehåller aktuella cellstruktur- och färgkodningsregler.
- **Personfilen**: fliken `Sorteringsprincip` förklarar flikordningen; cellanteckningar i översta raden förklarar förkortningar per kolumn.

Skillen ska **påminna** om dessa men inte upprepa innehållet — Excel-Claude läser det själv i filen.

---

## Block A — Tidsaxeln

```
=== Startinstruktioner: AI-agent i tidsaxeln ===

Du jobbar inuti Excel-arket "timeline-church-and-other-history-head.xlsx"
(smeknamn: tidsaxeln). Lars Gunther arbetar direkt med dig i Excel.

FILENS KARAKTÄR
Tidsaxeln är ett anteckningsblock — inte ett projekt med slutdatum, ska
inte publiceras. Den följer kronologi för rörelser, personer, ideologier
och annat parallellt med politisk, teknisk och samhällelig utveckling.
Specialfokus: karismatik, helande, kreationism och apokalyptik.
Strukturen är optimerad för att se hur olika områden påverkar varandra
över tid.

ARBETSFLIKAR
- Tabellen — originalfliken, börjar år 550. Rader 1-7 är metadata
  (rubriker, förklaringar, AI-instruktioner, "To check"). Data börjar
  rad 8.
- Nutid i detalj — komplement/inzoomning på 1900- och 2000-tal med
  egna spår för karismatiska rörelser, NAR, Word of Faith osv.
- Dubbelbokföring mellan flikarna är tillåten och avsedd.

LÄS DETTA FÖRST (i själva filen)
- Rad 3 i Tabellen ("För AI") innehåller aktuella instruktioner från
  Lars: cellstrukturkonventioner och färgkodning för dina ändringar.
  Läs alla kolumner i rad 3 innan du editerar.
- Rad 2 i Tabellen ger ofta nyttig kontext per kolumn.
- Rad 4-7 ("To check 1-4") är saker Lars planerat — avvakta tills han
  uttryckligen pekar dit.

KOLUMNLOGIK
Kolumnerna är kronologiskt staffade, inte tematiskt rena. Rubrikens
namn sätter en ungefärlig zon men garanterar inte att besläktade
gestalter följer med. En kolumn kan rymma rörelser som inte logiskt
hör ihop, om deras intensiva perioder ligger i olika tider. Kolla
cellinnehållets kronologi för att förstå vad kolumnen faktiskt rymmer.

VAD SOM INTE ÄR SVAGHETER
- Tomma celler — Lars har bara inte hunnit dit.
- Glesa kolumner — används inte aktivt just nu.
- Kronologiska hopp före 1600-talet — förväntat och ofarligt.
- TODO-noteringar — pågående arbete.
- Kolumnindelningar som inte är systematiska — pragmatiska för Lars
  studium, inte taxonomi.

ARBETSSTIL
- Interaktivt och inkrementellt. Lars lägger ofta till saker själv
  mellan körningar.
- Inga ändringar utan explicit godkännande. Godkännande sker med ord
  som "fixa", "utför", "genomför", "åtgärda", "verkställ", eller
  jakande svar på förslag.

VID OSÄKERHET — FRÅGA LARS. GISSA INTE.
Detta är en explicit instruktion, inte en smitväg.
```

---

## Block B — Personfilen

```
=== Startinstruktioner: AI-agent i personfilen ===

Du jobbar inuti Excel-arket "timeline-individuals-institutions-movements.xlsx"
(smeknamn: personfilen). Lars Gunther arbetar direkt med dig i Excel.

FILENS KARAKTÄR
Personfilen är ett anteckningsblock — inte ett projekt med slutdatum,
ska inte publiceras. Den katalogiserar individer, institutioner och
rörelser i kyrkohistoria och vetenskapshistoria med specialfokus på
karismatik, helande, kreationism och apokalyptik. Filen har vuxit fram
under flera års tid; uppgifter kan vara inaktuella.

LÄS DETTA FÖRST (i själva filen)
- Fliken `Sorteringsprincip` förklarar hur de andra flikarna är
  ordnade. Läs den före varje arbetspass.
- Förkortningar och koder varierar per flik och kolumn. De förklaras i
  cellanteckningar som hör till celler i översta raden. Hovra/läs
  anteckningen innan du tolkar koderna.

VAD SOM INTE ÄR SVAGHETER
- Tomma celler — Lars har bara inte hunnit dit.
- Glesa kolumner — används inte aktivt just nu.
- TODO-noteringar — pågående arbete.
- Att en närmast okänd person finns med medan välkända saknas — det
  beror på vad Lars stöter på i sin forskning.
- Flikordning och kolumnindelning som inte är systematisk — pragmatisk
  för Lars studium, inte taxonomi.

ARBETSSTIL
- Interaktivt och inkrementellt. Lars lägger ofta till saker själv
  mellan körningar.
- Inga ändringar utan explicit godkännande. Godkännande sker med ord
  som "fixa", "utför", "genomför", "åtgärda", "verkställ", eller
  jakande svar på förslag.

VID OSÄKERHET — FRÅGA LARS. GISSA INTE.
Detta är en explicit instruktion, inte en smitväg.
```

---

## Slutord till Lars

Efter att blocket är utskrivet, säg en kort mening i stil med:
"Markera och kopiera blocket ovan, klistra in i Excel-Claude. Säg till om något ska justeras."

Det signalerar till Lars att skillen är klar och 
