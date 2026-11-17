# Rechte-Ampel für O-Töne

`scripts/rights.py` bewertet jeden O-Ton der Drehfassung aus seinem `rights`-Eintrag in `clips.json`. **Arbeitshilfe, keine Rechtsberatung** – das immer dazusagen.

## Grundlage
Zitatrecht CH Art. 25 URG / DE § 51 UrhG (AT § 42f UrhG ähnlich):
1. **Zweck:** Beleg, Erörterung, Auseinandersetzung. Der Sprechtext muss sich mit dem Zitat befassen.
2. **Umfang:** nur so lang, wie der Zweck es erfordert.
3. **Quelle nennen** (Bauchbinde und Beschreibung).
Reine Bebilderung (B-Roll unter dem Sprechtext ohne Auseinandersetzung) ist kein Zitat. Massgeblich ist das strengere Recht der Länder, in denen das Video abrufbar ist. YouTube Content ID kann Sendermaterial unabhängig davon claimen.

## Felder
```json
"rights": {"owner": "ZDF", "kind": "sender", "use": "zitat", "license": "CC BY 4.0", "status": "geklärt", "note": "…"}
```

| `kind` | Beispiel | Ampel |
|---|---|---|
| `eigen` | eigene Aufnahme | 🟢 |
| `amtlich`, `us_gov` | Regierungs-/Parlamentsmediathek mit freier Nutzung, US-Bundeswerke | 🟢 |
| `parlament` | Rede im Parlament (Wortlaut frei, Bild beim Kanal) | 🟡 |
| `person` | von Person/Partei selbst veröffentlicht | 🟡 |
| `sender` | TV, Zeitung, YouTube-Kanal | 🟡 |
| `wissenschaft` | Vortrag, Institut | 🟡 |
| `agentur` | Reuters, AP | 🟡 |
| `film` | Kinofilm, Doku eines Produzenten | 🔴 |
| `privat` | Privatpersonen (Persönlichkeitsrecht) | 🔴 |

Modifikatoren: `use: "bebilderung"` macht 🟡 zu 🔴; über 30 s gibt einen Hinweis; `license` CC/gemeinfrei oder `status: "geklärt"` → 🟢.

## Vorgehen
- Beim Aufnehmen eines O-Tons in `clips.json` gleich `rights` ausfüllen. Kanal des Uploads ist meist der Rechteinhaber, nicht die sprechende Person.
- Originalquelle bevorzugen (Parlamentskanal statt Sender-Mitschnitt).
- Nach `rights.py` die Tabelle `out/rechte.md` in den Recherche-Teil des Teleprompters übernehmen und 🔴 als Aufgaben nennen: Freigabe anfragen, durch Originalquelle ersetzen, kürzen, oder als Zitat einbetten (Sprechtext ordnet ein).
