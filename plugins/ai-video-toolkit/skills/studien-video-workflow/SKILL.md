---
name: studien-video-workflow
description: Faktenbasiertes Erklärvideo von der Idee bis zum Rohschnitt. Teleprompter, in dem jede Behauptung durch eine Studie belegt ist, Studien-Slides im Corporate Design, O-Töne, Prüfung gegen Originale, Quellenliste, Schnitt-Mockup mit TTS-Stimme, Preview-MP4, 1080p-Clips für den Schnitt und Rechte-Ampel. Verwenden, wenn jemand ein Video, einen Vortrag oder einen YouTube-Beitrag mit Belegen, Studien, Zahlen oder O-Tönen plant.
---

# Studien-Video-Workflow

Ziel: ein Video, in dem **jede Behauptung durch eine Studie belegt** ist und die Studie beim Sprechen eingeblendet wird. Am Ende hat der Nutzer ein geprüftes Skript, ein Foliendeck, einen anklickbaren Schnitt-Mockup, ein Preview-Video, alle O-Töne als Schnitt-Clips und eine Rechte-Übersicht.

Grundregel überall: **keine Fehler**. Lieber eine Aussage weglassen oder abschwächen als etwas behaupten, das im Original nicht steht.

Lege am Anfang eine Task-Liste mit den Schritten 0–9 an und hake sie ab. Arbeite durch, ohne auf Antworten zu warten; Fragen an den Nutzer gehen raus, sobald sie anfallen, während die Arbeit weiterläuft.

**Zu Beginn klären** (eine Nachricht, dann loslegen mit sinnvollen Standards):
- Thema, Thesen, Zielgruppe, Sprache und Ziellänge (Standard: Deutsch, Schweizer Schreibweise, 8–10 Min.).
- Corporate Design: Vorlage oder Beispiel-Folie? Folienformat? (Standard: 16:9; siehe `references/slides.md`.)
- Gibt es ein eigenes Video-Archiv oder Recherche-Tool für O-Töne? (Sonst YouTube, siehe Schritt 1.)
- Sprecher- und Kanalname für Mockup und Preview.

## Werkzeuge dieses Skills

Im Skill-Ordner liegen:
- `scripts/`: `tts.py`, `build_mockup.py` + `template.html`, `render_preview.py`, `fetch_clips.py`, `rights.py`, `common.py`. Kopiere `scripts/` in den Arbeitsordner und arbeite mit einem **Projektordner** (Format: `references/toolkit.md`).
- `examples/demo/`: kleinstes lauffähiges Projekt. `examples/demokratiekrise/`: echtes Projekt mit 19 O-Tönen als Vorlage für Struktur und Rechte-Einträge.
- `references/`: `toolkit.md` (Projektformat, Befehle), `slides.md` (Deck bauen, CD), `rechte.md` (Rechte-Ampel), `quellen-tool-beispiel.md` (Beispiel für ein eigenes O-Ton-Archiv).

Lies die jeweilige Referenz, bevor du den Schritt beginnst.

---

## Goldene Regel: Nichts aus der Ideensammlung ist geprüft

**Jede Zahl, jedes Zitat und jede Studienaussage aus den Uploads des Nutzers gilt als ungeprüft, bis sie wörtlich im Original gefunden ist.** In der Praxis weicht rund die Hälfte ab. Prüfe deshalb bei jeder Zahl:

1. **Original finden.** Primär-PDF herunterladen (eigener Ordner `src/`), `pdftotext -layout`, grep auf die exakte Zahl. Eine Zusammenfassung oder Pressemeldung ist kein Beleg.
2. **Offizieller Bericht vor Presseseite.** Bei Abweichung gilt der Bericht.
3. **Bezugsgrösse prüfen:** Wer wurde befragt? Wie viele haben abgestimmt? Gilt die Zahl für alle Kategorien oder nur eine?
4. **Richtung prüfen.** «Sinkend» braucht eine Zeitreihe.
5. **Ausnahmen prüfen.** Ein Länderdurchschnitt kann für das Land im Video falsch sein; das gehört offen auf die Folie.
6. **Wortlaut prüfen.** «begünstigt» ist nicht «erzwingt». Geänderte Frageformulierungen kommen in die Caption.
7. **Keine Details erfinden.** Daten, Orte und Teilnehmerzahlen nur, wenn sie im Original stehen. Was aus dem Gedächtnis kommt, als ungeprüft markieren.
8. **Nicht auffindbar?** Durch eine belegbare Studie ersetzen oder streichen und dem Nutzer sagen.

Jede Abweichung kommt in die Tabelle **Korrekturen gegenüber der Ideensammlung**: was dort steht, was das Original sagt, was im Skript steht.

Blockiert ein Server, eine identische Kopie suchen und vermerken. Webseiten ohne PDF per Playwright als PDF drucken. Hinter Paywalls nichts herunterladen; die Abstract-Seite reicht, wenn die Zahl dort steht.

---

## Schritt 0 – Intake & Teleprompter

1. Alle Uploads vollständig lesen. Thesen, Titel, genannte Studien und Zahlen samt Links extrahieren.
2. **Sofort** den Teleprompter als Dokument anlegen (Claude Doc, sonst Markdown-Datei), als Skelett mit den Tabs bzw. Abschnitten **Drehfassung**, **Recherche & Quellen** (Quellentabelle, Korrekturen, Schwachstellen und offene Punkte), und öffnen.
3. Jede Zahl nach der goldenen Regel prüfen, dann füllen:
   - **Drehfassung** in der Cue-Syntax aus `references/toolkit.md` (`## Kapitel`, `▶ EINBLENDEN N · Titel`, Sprechtext, `■ O-TON …`). Rund 130 Wörter pro Minute Sprechtext. Kurze, sprechbare Sätze. Lieber 8 starke Belege als 15 schwache.
   - **Quellentabelle:** Slide, Aussage, Quelle mit Link, exakte Fundstelle.
   - **Schwachstellen:** Korrelation vs. Kausalität, Stichprobe, Land, Methodenwechsel, Deutung vs. Messwert.
4. Dramaturgie: Intro mit Überblick-Folie aller Probleme bzw. Thesen; pro Problem eine **Kapitelkarte** («Problem N von M», gesprochen nur «Problem N: Name.»); vor dem Lösungsteil ein kurzes Zwischenfazit; der Schluss beantwortet die Titelfrage.
5. Ändern sich Slides oder Zahlen, Drehfassung **und** Quellentabelle anpassen.

## Schritt 1 – O-Töne

Ziel: **2–3 echte O-Töne pro Kapitel**, in denen eine Person selbst spricht (Politik, Wissenschaft, Betroffene), verschiedene Sprecher und Haltungen.

- **Quelle:** Hat der Nutzer ein eigenes Archiv oder Such-Tool, das zuerst nutzen (Beispiel: `references/quellen-tool-beispiel.md`). Sonst YouTube: `yt-dlp "ytsearch8:<suche>" --flat-playlist --print "%(id)s | %(channel)s | %(title)s"`, dann Untertitel holen (`--skip-download --write-auto-subs --sub-format json3`) und das Zitat über die Wort-Zeitmarken exakt schneiden.
- **Originalquelle bevorzugen:** Reden aus dem Parlamentskanal, Auftritte vom Kanal der Person oder Partei statt eines Senderbeitrags (Rechte, Content ID).
- **Zahlen in O-Tönen gegen Faktenchecks prüfen** und im Recherche-Tab vermerken. Polemische oder falsche Zahlen nur, wenn das Skript sie einordnet.
- Dem Nutzer die Auswahl als Tabelle vorlegen (Kapitel, Zeitstempel-Link, Sprecher, Zitat). Jede Wahl kommt mit `vid, a, b, who, text, ut?, source, rights` in `clips.json`.
- YouTube blockiert Downloads aus Rechenzentren. Downloads auf dem Rechner des Nutzers ausführen, wenn er verbunden ist; sonst das ihm überlassen.

## Schritt 2 – Studien-Slides

Für jede Kernaussage eine Folie mit der belegenden Grafik oder Tabelle aus dem Original, als **editierbares Deck** mit nativen Charts. Ablauf, CD-Extraktion, Chart-Regeln und QA: `references/slides.md`. Danach Folienbilder rendern (`pdftoppm -jpeg -scale-to-x 1300 deck.pdf <projekt>/slides/s`).

## Schritt 3 – Gegenprüfung & Original-Ordner

1. Jede Folie Zahl für Zahl gegen das Original: Chart-Werte, Captions, Callouts, Notes.
2. Korrekturen in Deck, Drehfassung und Quellentabelle nachziehen.
3. Ordner `Originalstudien_<Thema>/` mit nummerierten PDFs (wie die Slides) und `LIESMICH.txt` (Quelle, Fundstelle, was fehlt). Als ZIP liefern.

## Schritt 4 – Feedback (immer)

Nach jeder Lieferung aktiv Feedback mit nummerierten, konkreten Fragen einholen: Dramaturgie, heikle Folien, Titel, weggelassene Themen, O-Töne. Alle Korrekturen gegenüber der Ideensammlung kompakt mitschicken. Bei Konflikten zwischen Wunsch und Beleglage begründen und eine Alternative vorschlagen.

Regelmässig selbst die **schwächste Stelle** suchen (Logik, Bezug zum Zielland, Widerspruch zwischen Sprechtext und O-Ton) und konkret umformulieren.

## Schritt 5 – Quellen für die Video-Beschreibung

Kopierfertige Liste in Folienreihenfolge als Plain Text im Codeblock:
```
Quellen:
• Nachname, I. & Nachname, I. (Jahr): Titel. Journal Band(Heft). https://doi.org/…
```
DOI bevorzugen. Links, die du nicht selbst geöffnet hast, zum Anklicken markieren.

## Schritt 6 – Schnitt-Mockup

Projektordner nach `references/toolkit.md` anlegen (`project.json`, `drehfassung.md` aus dem Doc, `clips.json`, `slides/`, Stimme in `tts/`). Dann:
```
python scripts/fetch_clips.py <projekt> --mode preview   # O-Töne 720p (Rechner mit YouTube-Zugang)
python scripts/tts.py <projekt>                          # Sprechtext mit Piper vertonen
python scripts/build_mockup.py <projekt>                 # -> <projekt>/index.html
```
Smoke-Test über `python3 -m http.server` + Playwright (keine Fehler, 0 Clips «unbekannt»), dann als Artifact veröffentlichen (`index.html` + Unterordner). Bei jeder Textänderung im Doc: `drehfassung.md` aktualisieren, `tts.py` und `build_mockup.py` erneut, neu veröffentlichen. Das Doc bleibt die Quelle der Wahrheit.

## Schritt 7 – Preview-MP4

`python scripts/render_preview.py <projekt>` → `out/<Titel>_Preview.mp4`. Im Hintergrund laufen lassen, Standbilder prüfen, Datei liefern. Hinweise mitgeben (lange Applaus-Stellen, B-Roll mit Originalton).

## Schritt 8 – Schnitt-Assets

`python scripts/fetch_clips.py <projekt> --mode schnitt --pad 5` → `out/schnitt_1080/OT01_….mp4` (1080p, 5 s Vor- und Nachlauf) und `Schnittliste.csv`. Fehlerzeilen melden. Geparkte O-Töne nur auf Wunsch (`--all`).

## Schritt 9 – Rechte-Ampel

`python scripts/rights.py <projekt>` → `out/rechte.md`. Regeln und Formulierungen: `references/rechte.md`. Tabelle in den Recherche-Tab, offene 🔴-Punkte als Aufgaben nennen. Immer dazusagen: keine Rechtsberatung.

---

## Lessons learned

- Zahlen in drei Sorten trennen: zitiert, abgelesen, eigene Berechnung.
- Ein Durchschnitt über Länder belegt nichts für ein einzelnes Land.
- Philosophische Argumente als Argument kennzeichnen, nicht als Messung.
- Bei Folien-Umbauten Nummern in Cues, Notes, Dateinamen und Quellenliste synchron halten.
- Ein Argument muss zum Publikum passen: ein UK-Beispiel für Mehrheitswahlrecht trägt in DE/CH nur mit Brücke zum eigenen System.
- Redner-Daten verifizieren (Datum der Rede ≠ Datum der Abstimmung darüber).
- Polemische Belege auf Wunsch streichen; Meinungsfolien als Meinung kennzeichnen.
- Doc-Tab komplett ersetzen: alle Block-IDs löschen und neu einfügen, danach per Suche prüfen, dass nichts doppelt steht.
- Bereits veröffentlichte Artifact-Dateien, die in der Session nicht gelesen wurden, lassen sich nicht überschreiben: neuen Ordner nehmen (`slides_dir` in `project.json`).
- Auf dem Rechner des Nutzers sterben Hintergrundprozesse oft mit dem Aufruf: in kurzen Schritten arbeiten; die Skripte überspringen Erledigtes.
