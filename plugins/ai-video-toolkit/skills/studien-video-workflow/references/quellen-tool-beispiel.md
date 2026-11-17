# Beispiel: eigenes O-Ton-Archiv anbinden

Hat der Nutzer ein eigenes durchsuchbares Video-Archiv, ist es die beste O-Ton-Quelle (kuratiert, mit Transkripten und Zeitmarken). Der Skill ist nicht daran gebunden; das hier ist nur ein Muster, wie man so ein Tool nutzt. Vorlage: das Open-Source-Tool «ytrag» (YouTube-Transkripte + semantische Suche) mit HTTP-API.

## Suchen
```
GET <BASE>/api/search?q=<text>&mode=semantic&limit=8&rerank=1     # oder mode=keyword
GET <BASE>/api/context?video_id=<id>&t=<sek>                      # Transkript ±30 s
```
- Pro Folie 2–3 semantische Anfragen (These als Aussage, Alltagssprache, Gegenposition) plus Keyword-Anfragen für Begriffe. Parallel (4 Worker), Ergebnisse als `raw.json` speichern.
- Felder pro Treffer z.B. `video_id, start, end, title, channel, text, people, score` (Rerank 0–10, ab ~7 brauchbar).
- Über `/api/context` den genauen Satzanfang und -ende finden, dann `a`/`b` für `clips.json` setzen.
- Folien ohne gute Treffer als dünn markieren und fragen, ob der Nutzer passende Videos importieren will.

## Sammlung anlegen (falls das Tool das kann)
- Eine Sammlung pro Video, Beschreibung = Zuordnung Clip → Folie.
- Zugangsdaten **beim Nutzer erfragen**, nie aus `.env` oder Konfigurationsdateien lesen. Hat der Nutzer ein Passwort im Chat geteilt, raten, es danach zu ändern.
- Ohne Zugang: die Sammlung als JSON und die Deep-Links liefern.

## Ohne eigenes Archiv
YouTube direkt:
```
yt-dlp "ytsearch8:<suche>" --flat-playlist --print "%(id)s | %(channel)s | %(duration_string)s | %(title)s"
yt-dlp --skip-download --write-auto-subs --sub-langs de,en --sub-format json3 -o subs/%(id)s "https://youtu.be/<id>"
```
Die json3-Untertitel haben Wort-Zeitmarken (`tStartMs` + `tOffsetMs`); damit Zitatanfang und -ende auf die Zehntelsekunde setzen. Mediatheken (Parlamente, Sender) über ihre eigene Suche, Links mit Zeitmarke notieren.
