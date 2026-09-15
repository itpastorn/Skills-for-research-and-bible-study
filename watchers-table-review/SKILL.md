---
name: watchers-table-review
description: Slår upp, uppdaterar och utökar rankningstabellen över granskare/watchers (ranking-of-watchers.xlsx). Aktiveras av /watchers-table-review eller naturligspråkliga fraser om rankningstabellen.
---

# watchers-table-review

Rankningstabellen samlar bedömningar av kritiker, granskare och diskernmentkanaler som kan dyka upp i källmaterial. Filen är:

> **Anpassa:** Byt ut sökvägen här och i kodexemplen nedan mot platsen för din egen tabell.

```
C:\sökväg\till\ranking-of-watchers.xlsx
```

## Kolumner

| Kolumn | Innehåll |
|--------|----------|
| Person(er) | Personnamn, eller "(okänt)" för anonyma kanaler |
| Kanal / Organisation | YouTube-kanal, podcastnamn eller organisation |
| Kvalitet (1–5) | Bedömningspoäng. Tom = ej ännu bedömd |
| Kommentar | Kort motivering av poängen |
| Teologisk utgångspunkt | Ett av de fördefinierade alternativen, eller tomt om det inte framgår |

### Tillåtna värden för Teologisk utgångspunkt

- `Kontinuationism - stark`
- `Kontinuationism - försiktig`
- `Progressiv/liberal`
- `Fundamentalism`
- `Dekonstruktion`
- `Sekulär`
- *(tomt om det inte framgår tydligt)*

### Kvalitetsskala 1–5

| Poäng | Innebör |
|-------|---------|
| 5 | Hög bevisstandard, distinktioner görs, öppen för korrigering |
| 4 | Välunderbyggd men med enstaka svagheter i ton eller bevisning |
| 3 | Funktionell — faktahaltig men med metodologiska eller retoriska brister |
| 2 | Ytlig eller oproportionerlig; använd med försiktighet |
| 1 | Ogrundad, desinformerande eller oärlig |

## Triggerfraser

Skillen aktiveras av `/watchers-table-review` eller fraser som:

- "Vad står det om [namn] i rankningstabellen?"
- "Hur pålitlig är [namn] som granskare / watcher?"
- "Finns det anledning att uppdatera rankningstabellen?"
- "Lägg till [namn] i rankningstabellen"
- "Uppdatera [namn] i tabellen"
- "Visa rankningstabellen"

## Arbetsflöde

### Slå upp en person

Läs tabellen med Python och sök på person- eller kanalnamn (case-insensitiv, partiell matchning är OK):

```python
import openpyxl
from pathlib import Path

path = Path(r"C:\sökväg\till\ranking-of-watchers.xlsx")
wb = openpyxl.load_workbook(path)
ws = wb.active
headers = [cell.value for cell in ws[1]]
query = "winger"  # ersätt med söktermen

matches = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if any(query.lower() in str(cell or "").lower() for cell in row[:2]):
        matches.append(dict(zip(headers, row)))

for m in matches:
    print(m)
```

Presentera resultatet i ett snyggt format i chatten — inte rådata.

### Lägga till ny rad

```python
import openpyxl
from pathlib import Path

path = Path(r"C:\sökväg\till\ranking-of-watchers.xlsx")
wb = openpyxl.load_workbook(path)
ws = wb.active

new_row = ["Person", "Kanal", None, "Kommentar", "Teologisk utgångspunkt"]
ws.append(new_row)
wb.save(path)
```

Bekräfta för användaren att raden lagts till.

### Uppdatera befintlig rad

Hitta raden (partiell matchning på kolumn A eller B), uppdatera önskade celler, spara.

```python
import openpyxl
from pathlib import Path

path = Path(r"C:\sökväg\till\ranking-of-watchers.xlsx")
wb = openpyxl.load_workbook(path)
ws = wb.active

query = "winger"
for row in ws.iter_rows(min_row=2):
    if any(query.lower() in str(cell.value or "").lower() for cell in row[:2]):
        row[2].value = 5          # Kvalitet
        row[3].value = "Ny kommentar"
        row[4].value = "Kontinuationism - försiktig"
        break

wb.save(path)
```

### Visa hela tabellen

Om användaren ber om hela tabellen: läs alla rader och presentera som en Markdown-tabell i chatten. Sortera bedömda (Kvalitet != None) före obedömda, och fallande efter kvalitetspoäng.

## Viktigt

- Lägg **aldrig** till en person med fabricerade uppgifter. Om Teologisk utgångspunkt eller Kommentar är okänd — lämna fältet tomt.
- Fråga inte om bekräftelse för enkla uppslagningar. Fråga om bekräftelse **innan** du sparar ändringar.
- Om en person redan finns i tabellen och användaren vill lägga till den igen: informera om det och fråga om de vill uppdatera befintlig rad istället.
- Spara alltid till samma sökväg — skapa aldrig en ny fil.
