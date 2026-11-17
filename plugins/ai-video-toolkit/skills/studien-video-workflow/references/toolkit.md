# Toolkit: Projektordner, Formate, Befehle

Alle Skripte liegen in `scripts/` dieses Skills. In den Arbeitsordner kopieren (`cp -r <skill>/scripts .`) und mit `python scripts/<name>.py <projekt>` aufrufen. Voraussetzungen: Python 3.10+, ffmpeg, poppler (`pdftoppm`), `pip install pillow piper-tts`, für Online-Quellen `yt-dlp`. Fehlt etwas, installieren (`pip install --break-system-packages …`, `apt-get install ffmpeg poppler-utils`; auf dem Mac `brew install …`).

## Projektordner

```
projekt/
  project.json      Titel, Sprecher, Kanal, Stimme
  drehfassung.md    Teleprompter (Cue-Syntax unten), aus dem Doc kopiert
  clips.json        O-Ton-Register
  slides/s-01.jpg   Folienbilder: pdftoppm -jpeg -scale-to-x 1300 deck.pdf projekt/slides/s
  tts/<voice>.onnx  Piper-Stimme + <voice>.onnx.json
```
Erzeugt werden `audio/`, `tts/manifest.json`, `clips/`, `stills/`, `index.html`, `out/`. Vorlage: `examples/demo/`.

### project.json
```json
{"title": "Mein Video", "speaker": "Name", "channel": "Kanal",
 "voice": "de_DE-thorsten-high", "slides_dir": "slides",
 "pronounce": {"CO2": "C O zwei"}, "links": {}}
```
- `voice`: beliebige Piper-Stimme von https://huggingface.co/rhasspy/piper-voices (Deutsch: `de/de_DE/thorsten/high/de_DE-thorsten-high.onnx` + `.onnx.json`, Englisch: `en/en_US/lessac/medium/…`). Mit `curl -LO` nach `projekt/tts/` laden.
- `pronounce`: Ersetzungen nur fürs Vorlesen.
- `slides_dir`: anderer Ordner, z.B. wenn ein veröffentlichtes Artifact neue Folienpfade braucht.
- `links`: Link-Ziel pro `vid` für Nicht-YouTube-Quellen (z.B. Film-Website).

## Cue-Syntax der Drehfassung

```
## 1. Kapitelname
▶ EINBLENDEN 3 · Folientitel
Sprechtext, beliebig viele Sätze und Absätze. Jeder Satz wird eine Audiodatei.
■ O-TON Sprecher, Kontext · 2:50,6–3:00,6 · «Zitat zur Orientierung»
Weiterer Sprechtext, weiter über Folie 3.
## Geparkt (nicht im Video)
■ O-TON … (alles ab hier wird ignoriert, bleibt aber im Doc erhalten)
```
- `▶ EINBLENDEN N` zeigt `slides/s-NN.jpg` (s-1.jpg wird automatisch zu s-01.jpg).
- Timecode des O-Tons im **Quellvideo**, Komma oder Punkt als Dezimalzeichen.
- `**`-Fettschrift wird ignoriert; man kann direkt aus dem Doc kopieren.

## clips.json

```json
[{"vid": "Qa67WOP9jYg", "a": 170.6, "b": 180.6,
  "who": "Name · Kontext (Quelle)", "text": "Wortlaut", "ut": "Untertitel (optional, wird ins Preview gebrannt)",
  "source": {"type": "youtube", "id": "Qa67WOP9jYg"},
  "rights": {"owner": "NDR", "kind": "sender", "use": "zitat", "note": ""}}]
```
- Zuordnung O-Ton ↔ Clip, wenn `|Δa| + |Δb| < 2` Sekunden.
- `who`: Text vor `·` = Name im Bauchbinden-Tag, danach Quelle.
- `source.type`:
  - `youtube` (Standard, wenn `source` fehlt; `vid` = YouTube-ID)
  - `url`: alles, was yt-dlp kann
  - `file`: `{"path": "/pfad/datei.mp4"}`, eigene Aufnahmen, gekaufte Footage
  - `hls`: eingebettete Streams (z.B. Vimeo auf einer Film-Website): `{"info_json": "vinfo.json", "video_format": "…", "preview_video_format": "…", "audio_format": "…", "referer": "https://…"}`. `info_json` = Ausgabe von `yt-dlp -J --referer <seite> <player-url>`. Signierte URLs laufen nach Stunden ab (HTTP 410) → neu holen.
- `rights`: siehe `rechte.md`.

## Befehle

| Schritt | Befehl | Ergebnis |
|---|---|---|
| O-Töne für Mockup | `fetch_clips.py P --mode preview` | `clips/`, `stills/` (720p, genau a–b) |
| Stimme | `tts.py P` | `audio/*.mp3`, `tts/manifest.json` |
| Mockup | `build_mockup.py P` | `index.html` (warnt bei O-Tönen ohne Clip) |
| Preview | `render_preview.py P [--force]` | `out/<Titel>_Preview.mp4` |
| Schnitt-Assets | `fetch_clips.py P --mode schnitt --pad 5 [--all]` | `out/schnitt_1080/OTnn_….mp4`, `Schnittliste.csv` |
| Rechte | `rights.py P` | `out/rechte.md`, `out/rechte.csv` |

Alle Skripte überspringen Erledigtes und schreiben atomar (`.tmp` + rename). Man kann sie in kurzen Schritten wiederholen.

Nach Änderungen:
| Geändert | Neu laufen lassen |
|---|---|
| Sprechtext | `tts.py` → `build_mockup.py` → `render_preview.py --force` |
| O-Ton / Timecode | `fetch_clips.py --mode preview` → `build_mockup.py` → `render_preview.py --force` |
| Folien | `pdftoppm` → `build_mockup.py` → `render_preview.py --force` |

## Wo was läuft

- YouTube blockiert Rechenzentren («Sign in to confirm you're not a bot»). `fetch_clips.py` daher auf dem Rechner des Nutzers ausführen (verbundener Ordner oder der Nutzer selbst). Alles andere läuft überall.
- Mockup nur über einen Webserver öffnen (`python3 -m http.server`), sonst blockiert der Browser das Audio. Für das Artifact: `index.html`, `audio/`, `clips/`, `stills/`, `slides/` als Dateien veröffentlichen.
- yt-dlp liefert gelegentlich nur Ton; das Skript prüft Bild, Ton und Länge und versucht es bis zu dreimal. Bleibt es dabei: `yt-dlp -U`.
