# Studien-Slides

Für jede Kernaussage eine Folie mit der belegenden Grafik oder Tabelle aus dem Original. Erst Fakten prüfen, dann bauen.

## Format wählen
- **Standard:** 16:9-Deck. Gibt es einen Slides-Artifact-Typ, den nehmen (Charts editierbar, Export als PPTX/PDF).
- **Eigenes Format oder eigene Vorlage** (z.B. 2308×1885 für ein Split-Screen-Layout): editierbares PPTX mit pptxgenjs (pptx-Skill lesen). Layout `H = 10`, `W = 10 * Breite/Höhe` Zoll; bei 1080 px Basis-Höhe gilt `Zoll = px/108`, `pt = px*2/3`.
- **Keine Bilder von Charts:** Daten als native Charts (`addChart`), damit der Nutzer Werte ändern kann. Einen Balken hervorheben: bei einer Serie `chartColors` als Array pro Balken. Grössenvergleiche ohne Achse als flächentreue Formen.

## Corporate Design
Immer aus der Vorlage des Nutzers extrahieren (Farben, Schrift, Logo, Positionen von Titel, Quelle, Caption, Callout) und als Tabelle festhalten. Fragen, wenn nichts vorliegt; sonst schlichtes Design: weiss, Navy-Titel, ein Akzent.

Beispiel (Kanal «Losdemokratie», Format 2308×1885):

| Element | Spezifikation |
|---|---|
| Hintergrund | Weiss |
| Folientitel | Navy `#0F2D5C`, bold, Arial, ~60 px (lang 50–52 px), y ≈ 150 |
| Oben rechts | Studientitel bold `#1B4594` ~26 px, darunter Autor · Journal · Jahr grau `#8D96B0` ~23 px |
| Logo | blaues Quadrat `#1B4594` mit 3 weissen Linien |
| Akzente | Rot `#C8102E`, Gold `#D4A017`, Hellblau `#9DB2D6`, Text `#1F2937` |
| Caption (y ≈ 825) | grau ~21 px, max. 2 Zeilen |
| Callout (y ≈ 905) | Fill `#F3F6FB`, Rand `#E1E7F0`, ~28 px, Kernzahlen bold navy |
| Titel-, Kapitel-, Schlussfolien | Navy-Hintergrund, kurzer roter Balken über dem Titel |

## Regeln
- Werte 1:1 aus dem Original. Abgelesene Werte in der Caption kennzeichnen, eigene Berechnungen als «eigene Berechnung».
- Methodenwechsel und eingeschränkte Stichproben gehören in die Caption.
- Speaker-Notes pro Folie: Fundstelle, exaktes Originalzitat, Warnhinweise («ACHTUNG: nicht … sagen»).
- Keine Wertungen ohne Beleg, keine hypothetischen Rechnungen.
- Kapitelkarten («Problem N von M») und eine Überblick-Folie aller Probleme im Intro.

## QA
- PPTX: Ordner-Einträge entfernen (`zip -dq deck.pptx '*/'`), mit dem Validator des pptx-Skills prüfen.
- Rendern (LibreOffice → PDF → `pdftoppm -jpeg -r 45`), Kontaktbogen mit 8 Folien pro Bild, **jede Folie ansehen**.
- Typische Fehler: grosse Zahlen brechen um, Labels überlappen den Chart, Caption berührt das Callout, leere Flächen auf Stat-Folien.
- Für Mockup und Preview: `pdftoppm -jpeg -scale-to-x 1300 deck.pdf <projekt>/slides/s`.
