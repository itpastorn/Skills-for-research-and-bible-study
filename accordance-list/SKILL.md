---
name: accordance-list
description: Producerar en kompakt, semikolon-separerad lista över bibelreferenser i det format som Accordance och Logos kan parsa direkt vid copy-paste, t.ex. "Matt 22:41-46; 26:64; 28:18; Mark 12:35-37". Skillen har två lägen — den kan antingen generera en helt ny lista utifrån ett tema/ämne Lars beskriver (t.ex. "ge mig en accordance-lista över texter om Kristi upphöjelse"), eller konvertera en befintlig prosalista, citatlista eller blandad lista som Lars klistrar in eller pekar på i chatten. Använd denna skill när Lars skriver "/accordance-list", säger "ge mig en accordance-lista", "lista för accordance/logos", "som en lista för bibelprogram", "som en lista för bibelprogram/accordance", "lista dem för accordance", "konvertera till accordance-format", eller pekar på en redan producerad lista och ber om den i kompakt form. Skillen täcker GT, NT och apokryferna (Logos/Accordance-förkortningar enligt logos.com/bible-book-abbreviations).
---

# accordance-list

Genererar bibelreferenslistor i ett format som Accordance och Logos kan parsa direkt vid copy-paste. Lars använder Accordance som sitt primära bibelprogram och behöver ofta en kompakt referenslista efter att ha fått en längre prosalista med kommentarer.

## Triggerigenkänning

Skillen aktiveras av:

- `/accordance-list <ämne eller inklistrad lista>`
- "ge mig en accordance-lista"
- "lista för accordance/logos"
- "som en lista för bibelprogram"
- "som en lista för bibelprogram/accordance"
- "lista dem för accordance"
- "konvertera till accordance-format"
- "kompakt bibelreferenslista"

## Två lägen

### Läge A: Konvertera en befintlig lista

Aktiveras när Lars pekar på en redan producerad lista (oftast tidigare i samma konversation) eller klistrar in en lista med vers­hänvisningar med kommentarer/prosa runt omkring.

Arbetsflöde:

1. Identifiera alla bibelreferenser i källtexten.
2. Behåll referensernas inbördes ordning från källan om inget annat sägs — Lars har ofta strukturerat texten kanoniskt eller tematiskt redan.
3. Formatera enligt formatreglerna nedan.
4. Leverera **endast** den färdiga listan i en kodblock. Ingen prosa, inga rubriker, ingen inledning.

### Läge B: Generera en ny lista

Aktiveras när Lars ger ett ämne men ingen källista (t.ex. "ge mig en accordance-lista över texter om Andens frukter").

Arbetsflöde:

1. Sammanställ relevanta texter.
2. Sortera kanoniskt om inget annat sägs.
3. Formatera enligt reglerna nedan.
4. Leverera endast listan i en kodblock.

Om ämnet är så brett att urvalet riskerar bli godtyckligt, fråga kort om avgränsning (max en fråga) innan listan genereras.

## Formatregler

Detta är Accordance/Logos kompakta referensformat. Reglerna har testats av Lars och fungerar i Accordance.

### Separatorer

- **Semikolon + mellanslag** mellan olika referenser till olika kapitel eller böcker: `Matt 22:41-46; 26:64; 28:18`
- **Komma + mellanslag** mellan verser eller versspann inom samma kapitel: `Joh 12:16, 23, 32`
- **Bindestreck** (`-`, inte en-dash `–`) för versspann: `Phil 2:9-11` (inte `Phil 2:9–11`)
- När en boks namn inte upprepas (för att samma bok fortsätter) räcker det med kapitel:vers: `Mark 12:35-37; 14:62; 16:19`
- När en bok byts, skriv ut bokens förkortning igen.

### Bokförkortningar

Använd "Most common"-förkortningen från Logos/Accordance. Se `abbreviations.md` i denna mapp för full lista.

**Viktigt:**

- Accordance/Logos kompakta format brukar utelämna punkten efter förkortningen. Lars exempel använde `Matt 22:41-46` (inte `Matt. 22:41-46`). Skillen följer detta — **utan punkt** i kompakta listan.
- För enkapitliga böcker (Obad, Phlm, 2 John, 3 John, Jude) skrivs bara vers: `Jude 14-15`, `Phlm 8`. (Accordance accepterar både `Jude 1:14-15` och `Jude 14-15`; använd den punktlösa vers-only-formen.)
- För nummerprefixerade böcker, mellanslag mellan siffra och bok: `1 Cor 15:20-28` (inte `1Cor` eller `I Cor`).

### Psaltaren och versnumrering

Lars använder normalt svenska biblar (B2000) som grund. Den svenska och den engelska versnumreringen i Psaltaren skiljer sig på ett par sätt:

- **Psalmöverskrifter** (de redaktionella inledningarna typ "En psalm av David, när profeten Natan kom till honom...") är **vers 1 i svenska biblar** (`Ps 51:1`) men är **vers 0 eller obenämnd** i de flesta engelska biblar. Accordance förstår **inte** `Ps 51:title` — använd istället `Ps 51:1` för svensk numrering, vilket är standard i denna skill.
- För psalmer med överskrift förskjuts hela versnumreringen med ett steg jämfört med engelska översättningar. När Lars i källtexten skrivit en vers efter svensk numrering, bevara den. När referenser hämtas från engelska källor och rör en psalm med överskrift, **konvertera till svensk numrering** (lägg till +1) om inget annat anges.
- Vid osäkerhet om en specifik referens gäller engelsk eller svensk numrering, fråga kort.

### Övriga regler

- Inga punkter, semikolon eller annat efter sista referensen.
- Hela listan i **en enda kodblock** så Lars kan kopiera den.
- Ingen prosa runt listan i Läge A — bara koden. I Läge B får skillen lägga en kort mening före kodblocket *endast* om en avgränsningsfråga ställts och besvarats; annars bara listan.

## Levereransform

Inline i chatten i en kodblock. Ingen filgenerering, ingen rapport.

Exempel:

```
Matt 22:41-46; 26:64; 28:18; Mark 12:35-37; 14:62; 16:19
```

## Apokryfer och pseudoepigrafer

Skillen stöder apokryferna med Logos "Most common"-förkortningar (Tob, Jth, Wis, Sir, Bar, 1 Macc, etc.). Se `abbreviations.md`. För pseudoepigrafer som inte finns i Logos-listan (1 Enok, Jubileerna, etc.) — använd den i akademisk litteratur vedertagna förkortningen (1 En, Jub) och flagga kort att Accordance kanske inte parsar dem automatiskt; Lars får då bedöma själv.

## Felhantering

- Om en referens i källan är oklar eller felaktig (t.ex. "Luk 24:50–53" vs "Luk 24:50-51"), använd källans version men flagga inte detta — Lars har redan gjort sitt urval.
- Om Lars källtext blandar svenska och engelska bokförkortningar, normalisera till engelska Logos/Accordance-förkortningar.
- Om listan blir mycket lång (>500 referenser), fråga om uppdelning per bok eller kategori.

## Referens

Förkortningstabellen finns i `abbreviations.md` i denna mapp. Den är hämtad från logos.com/bible-book-abbreviations och täcker GT, NT och apokryferna.
