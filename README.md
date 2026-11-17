# AI Video Toolkit: Teleprompter → Mockup → Preview → Schnitt-Assets → Rechte

Generisch, an kein bestimmtes Recherche-Tool gebunden. Alles hängt an einem **Projektordner**.

## Projektordner

```
projekt/
  project.json      {"title", "speaker", "channel", "voice", "slides_dir", "pronounce", "links"}
  drehfassung.md    Teleprompter (Syntax unten)
  clips.json        O-Ton-Register (Schema unten)
  slides/s-01.jpg   Folienbilder, z.B. pdftoppm -jpeg -scale-to-x 1300 deck.pdf slides/s
  tts/<voice>.onnx  Piper-Stimme (+ .onnx.json)
```
Die Skripte erzeugen: `audio/`, `tts/manifest.json`, `clips/`, `stills/`, `index.html`, `out/`.

## Drehfassung-Syntax

```
## 1. Kapitelname
▶ EINBLENDEN 3 · Folientitel
Sprechtext, beliebig viele Absätze.
■ O-TON Sprecher, Kontext · 2:50,6–3:00,6 · «Zitat …»
## Geparkt (nicht im Video)          ← alles danach wird ignoriert
```
Text nach einem O-Ton gehört zur zuletzt eingeblendeten Folie. Fett-Markdown (`**`) wird ignoriert, man kann also direkt aus einem Doc kopieren.

## clips.json

```json
{"vid": "Qa67WOP9jYg", "a": 170.6, "b": 180.6,
 "who": "Name · Kontext (Quelle)", "text": "Wortlaut", "ut": "deutsche Untertitel (optional)",
 "still": "stills/Qa67WOP9jYg_170.jpg",
 "source": {"type": "youtube", "id": "…"},
 "rights": {"owner": "NDR", "kind": "sender", "use": "zitat", "note": ""}}
```
- Ein O-Ton der Drehfassung wird dem Clip zugeordnet, wenn `|Δa| + |Δb| < 2` Sekunden.
- `source.type`: `youtube` (Standard, `vid` = YouTube-ID), `hls` (`info_json` aus `yt-dlp -J --referer …`, `video_format`, `preview_video_format`, `audio_format`, `referer`), `file` (`path`), `url` (alles, was yt-dlp kann).
- `rights.kind`: `eigen`, `amtlich`, `us_gov`, `parlament`, `person`, `sender`, `agentur`, `wissenschaft`, `film`, `privat`. `rights.use`: `zitat` oder `bebilderung`. Optional `license` (z.B. `CC BY 4.0`) und `status: "geklärt"`.
- `project.json → links`: Link-Ziel pro `vid` für Nicht-YouTube-Quellen (z.B. Film-Website).

## Ablauf

| Schritt | Befehl | Wo |
|---|---|---|
| Stimme | `python tts.py projekt` (pip install piper-tts) | überall |
| Preview-Clips | `python fetch_clips.py projekt --mode preview` | Rechner, der YouTube erreicht |
| Mockup | `python build_mockup.py projekt` → `index.html` | überall |
| Preview-MP4 | `python render_preview.py projekt` → `out/<Titel>_Preview.mp4` | überall (ffmpeg, Pillow) |
| Schnitt-Assets | `python fetch_clips.py projekt --mode schnitt --pad 5` → `out/schnitt_1080/` + `Schnittliste.csv` | Rechner, der YouTube erreicht |
| Rechte-Ampel | `python rights.py projekt` → `out/rechte.md`, `out/rechte.csv` | überall |

Alle Skripte überspringen Vorhandenes, man kann sie also in kurzen Schritten wiederholen. Nach Textänderungen: `tts.py` → `build_mockup.py` → `render_preview.py --force` (Segmente sind zwischengespeichert, `--force` rendert alles neu).

Voraussetzungen: Python 3.10+, ffmpeg, Pillow, yt-dlp (für YouTube/HLS), piper-tts.

## Beispiel

`beispielprojekt/` enthält Drehfassung, O-Ton-Register und Rechte-Einträge des Videos «Krise der liberalen Demokratie». Folienbilder, Audio, Clips und Stimmdateien sind nicht im Repo (siehe `.gitignore`); sie entstehen mit den Skripten. Die O-Töne gehören ihren jeweiligen Rechteinhabern.

## Lizenz

Code: MIT (siehe `LICENSE`). Die Rechte-Ampel ist eine Arbeitshilfe, keine Rechtsberatung.
