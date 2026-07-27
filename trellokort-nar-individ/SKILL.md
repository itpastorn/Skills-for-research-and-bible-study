---
name: trellokort-nar-individ
description: Skapar nya kort, uppdaterar befintliga kort, eller lägger till kommentarer på kort i listan "Enskilda individer" på Trello-tavlan "NAR, Revival Alliance och trumpprofetism". Använd denna skill när Lars säger "/trellokort-nar-individ" följt av action och namn, "skapa NAR-kort för X", "skapa kort på NAR-tavlan för X", "uppdatera NAR-kortet för X", "uppdatera Y på NAR-tavlan", "komplettera NAR-kortet", "kommentera på NAR-kortet för X", eller liknande naturligspråk som rör korten i listan "Enskilda individer" på NAR-tavlan. Trigger också om Lars pekar på en person i kontext av NAR / trumpprofetism / Revival Alliance och säger "lägg till kort", "uppdatera Trello", "komplettera kortet".
---

# trellokort-nar-individ

Skapar och underhåller kort i listan **"Enskilda individer"** på Trello-tavlan **"NAR, Revival Alliance och trumpprofetism"**.

## Tavla och lista

- Board ID: `670ad1bb32972ef2ddd9cc51`
- Listan "Enskilda individer" — slå upp lista-ID via `get_lists` vid varje körning (hårdkoda inte; lista kan flyttas / byta ID).

## Tre underkommandon

1. **skapa** — Skapa nytt kort med standardbeskrivningen.
2. **uppdatera** — Komplettera / uppdatera ett befintligt korts standardfält.
3. **kommentera** — Lägg till en kommentar på ett kort.

## Triggerformat

Slash-format:

```
/trellokort-nar-individ skapa <namn>
/trellokort-nar-individ uppdatera <namn>
/trellokort-nar-individ kommentera <namn>
```

Naturligt språk: tolka verb (skapa / uppdatera / kommentera / komplettera) + personnamn.

## Standardbeskrivning

Korten har en standardiserad `desc` med dessa rader (i ordning), separerade av en tom rad:

```
Egen sida: <URL till officiell webbplats, gärna /about>

Wikipedia: <URL till engelska Wikipedia-artikel>

Prophecy index: <URL till prophecyindex.org-sidan>

NAR-connections: <URL till narconnections.wordpress.com-sidan>

Elijah List: <söksida för personen>

Ministry watch: <URL till tag-sidan>

Roys Report: <URL till söksidan>

People for: <URL till peoplefor.org/rightwingwatch/people/[namn]>

Viktig granskning: <URL till granskande sida om sådan finns>

Spellista YouTube: <URL till Lars YouTube-spellista — fylls bara om Lars säger till>
```

Två valfria fält som kan finnas mellan "People for" och "Viktig granskning":

```
Instapaper: <URL>

OneNote: <URL>
```

Format: ren text utan markdown-länkar (matchar mönstret som etablerades i Sean Feucht-kortet). Tomma fält behåller etiketten med kolon men inget värde.

## Kortnamn

Kortnamnet är personens namn, möjligen med:
- **Sort-prefix**: "0. Charlie Kirk", "1. Mike Bickle" — siffra + punkt + mellanslag, för viktighetssortering.
- **Parentes-tillägg**: "Harold R. Eberle (systematic theology)" — för snabb påminnelse om okända.

Skillen skapar nya kort **utan** prefix eller parentes. Lars redigerar manuellt efteråt.

Update-flödet **rör aldrig kortnamnet** — sort-prefix och parentes bevaras.

## URL-källor och sökstrategi

| Fält | Källa | Strategi |
|------|-------|----------|
| Egen sida | Personens egen webbplats | WebSearch, leta `/about`-sida |
| Wikipedia | en.wikipedia.org | WebSearch "<namn> Wikipedia", verifiera rätt person |
| Prophecy index | prophecyindex.org | Fetcha alla 7 indexsidor (registrera mönstret vid första körningen), grep efter namnet. URL-mönster är `/prophets/view/<förnamn>_<efternamn>/` (lowercase, underscore) |
| NAR-connections | narconnections.wordpress.com | **Primärt**: fetcha `https://narconnections.wordpress.com/?s=<namn>` och leta efter en dedikerad sida om personen. **Fallback**: WebSearch `site:narconnections.wordpress.com <namn>`. Om båda tomma: ingen dedikerad sida finns — lämna blank. |
| Elijah List | elijahlist.com | Bygg söknings-URL: `https://www.elijahlist.com/words/search_results.html?keyword=&author=<efternamn>&day=&month=&year=&submit=Submit` (ingen check) |
| Ministry watch | ministrywatch.com | Bygg tag-URL: `https://ministrywatch.com/tag/<namn-med-bindestreck>/`. HTTP-checka. |
| Roys Report | roysreport.com | Bygg sök-URL: `https://roysreport.com/?s=<efternamn>` (ingen check) |
| People for | peoplefor.org | Bygg URL: `https://www.peoplefor.org/rightwingwatch/people/<namn-med-bindestreck>`. HTTP-checka. |
| Viktig granskning | Varierande | Letas bara om Lars uttryckligen säger var. Annars blank. |
| Spellista YouTube | Lars egen kanal | **Aldrig sökas eller gissas.** Bara om Lars uttryckligen ger URL. |
| Instapaper | instapaper.com | **Inte automatiserat** i v1. |
| OneNote | onenote.com | **Inte automatiserat** i v1. |

### HTTP-check

Innan en URL skrivs in i mönsterbaserade fält (People For, Ministry Watch tag):
- Gör HTTP-fetch och kontrollera status.
- Vid 404 / "Page Not Found"-innehåll: hoppa över fältet (lämna blank, flagga i bekräftelseutskriften).
- För söknings-URL:er (Elijah List, Roys Report): ingen check; de är alltid giltiga som söksidor även om resultatet är 0 träffar.

## Arbetsflöde: skapa nytt kort

1. **Slå upp lista-ID** för "Enskilda individer" via `get_lists` med board_id.
2. **Verifiera att namnet är ledigt.** `search` med board_ids och namnet. Om kort redan finns: avbryt och föreslå `uppdatera`.
3. **Sök URL:er** enligt tabellen. Prophecy Index kräver indexfetch + grep. NAR-connections försöker söksida först, WebSearch som fallback.
4. **Presentera fynd i chatten** som en lista. För varje fält visa antingen URL eller "blank — <skäl>" (ej hittad / inte automatiserat / väntar på Lars).
5. **Vänta på bekräftelse.** "Ja" / "kör" / "OK" → skapa. "Lägg till X i fält Y" → justera och bekräfta igen. "Nej" / "avbryt" → avbryt.
6. **Skapa kortet** med `create_card` i listan. Kortnamn = personens namn rakt av (utan prefix / parentes). `desc` enligt mall.
7. **Rapportera** Trello-URL till kortet.

## Arbetsflöde: uppdatera befintligt kort

1. **Hitta kortet** via `search` (board_ids + namn).
2. **Inspektera nuvarande `desc`**:
   - **Standardmall** = varje icke-tom rad börjar med en av etiketterna ("Egen sida:", "Wikipedia:", "Prophecy index:", "NAR-connections:", "Elijah List:", "Ministry watch:", "Roys Report:", "People for:", "Instapaper:", "OneNote:", "Viktig granskning:", "Spellista YouTube:") följt av valfri URL. Tomma rader tillåtna.
   - Om beskrivningen följer mallen: fortsätt.
   - Om beskrivningen har **fritext, anteckningar eller andra fält** OCH Lars *inte* har gett konverteringsinstruktioner: **AVBRYT**. Skriv ut den föreslagna standardbeskrivningen i chatten så Lars kan klistra in manuellt. Säg uttryckligen att kortet inte uppdaterades. Ingen force-flagga.
   - **Undantag — konverteringsläge**: Om Lars uttryckligen pekar ut hur befintligt innehåll ska mappas till standardfält ("denna länk är viktig granskning", "URL:en är hans egen sida", "behåll den befintliga texten som NAR-connections", etc.), är det grönt ljus att konvertera kortet från fritext till standardmall. Tolka generöst — Lars känner till sina kort och vet vad han ber om. Sök fortfarande URL:er för övriga fält enligt vanlig strategi. Steg 4 (presentera diff) och steg 5 (vänta på bekräftelse) gäller fortfarande — kortet uppdateras aldrig utan Lars uttryckliga "kör".
3. Om mall: **sök URL:er** för tomma fält. Verifiera befintliga URL:er — om en URL nu är 404, flagga men ta inte bort.
4. **Presentera diff**: vilka fält fylls på, vilka behålls, vilka är fortsatt blanka, vilka URL:er är döda.
5. **Vänta på bekräftelse.** Vid ja: `update_card` med ny `desc`.
6. **Rapportera.**

## Arbetsflöde: kommentera

1. **Hitta kortet** via `search` (board_ids + namn). Om det inte finns: avbryt och föreslå `skapa` först.
2. **Fråga interaktivt** vad kommentaren ska säga. Lars kan svara direkt med fullständig text, eller be om hjälp att formulera ihop kommentaren tillsammans (i ett eller flera turer). Inget kommitteras till Trello förrän Lars säger "kör" / "posta" / "ja".
3. **Posta** via `add_comment`. Rapportera kortets URL.

## Säkerhetsregler

- **Spellista YouTube, Instapaper, OneNote — aldrig automatisk ifyllnad.** Bara om Lars uttryckligen anger URL.
- **Kort skapas aldrig utan bekräftelse.**
- **Update-flödet rör aldrig icke-standard innehåll utan Lars instruktion** — vid mismatch, skriv ut förslag, ändra inget. Undantag: konverteringsläge när Lars uttryckligen pekar ut mappning (se uppdatera-flödet steg 2). Ingen force-flagga utöver det.
- **Kortnamn ändras aldrig av update-flödet** (bevara sort-prefix och parentes).
- **Bekräftelse innan varje `update_card`** med ny desc.
- **Kommentarer postas aldrig utan Lars uttryckliga "kör" / "posta" / "ja".**

## Verktyg

Trello MCP: `get_lists`, `search` (med `board_ids`), `get_card`, `create_card`, `update_card`, `add_comment`, `add_label_to_card`, `get_board_labels`.

Webb: `WebSearch` (Wikipedia, Ministry Watch-träffar, Roys Report-träffar, egen webbplats, NAR-connections-fallback), `web_fetch` (Prophecy Index-indexsidor, NAR-connections söksida, HTTP-checkar).
