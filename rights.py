"""Rechte-Ampel für alle O-Töne der Drehfassung.

  python rights.py <projekt>      -> out/rechte.csv + out/rechte.md

Pro Clip in clips.json ein Feld "rights":
  {"owner": "ZDF", "kind": "<siehe KINDS>", "use": "zitat|bebilderung", "license": "CC BY 4.0"?, "status": "geklärt"?, "note": "…"}
Keine Rechtsberatung: die Ampel ist eine Arbeitshilfe, die Entscheidung trifft der Nutzer.
"""
import json, os, sys
from common import load_project, parse, tc

KINDS = {
    'eigen':      ('grün', 'Eigene Aufnahme.'),
    'amtlich':    ('grün', 'Amtliches Werk bzw. frei nutzbare Parlaments-/Regierungsaufnahme (Nutzungsbedingungen der Mediathek prüfen, Quelle nennen).'),
    'us_gov':     ('grün', 'Werk der US-Bundesregierung (gemeinfrei), z.B. Weisses Haus, C-SPAN-Kongressbild.'),
    'parlament':  ('gelb', 'Rede im Parlament: Wortlaut frei (DE § 48 UrhG), Bildrechte beim Kanal. Originalkanal des Parlaments bevorzugen.'),
    'person':     ('gelb', 'Von der Person/Partei selbst veröffentlicht. Zitatrecht meist tragfähig.'),
    'sender':     ('gelb', 'Rundfunk-/Medienmaterial. Zitatrecht nur mit Auseinandersetzung im Sprechtext; Content-ID-Claim möglich.'),
    'agentur':    ('gelb', 'Agenturbild (Reuters, AP …). Als B-Roll ohne Auseinandersetzung kaum gedeckt; Lizenz prüfen.'),
    'wissenschaft': ('gelb', 'Vortrag/Interview von Forschenden. Zitatrecht meist tragfähig.'),
    'film':       ('rot',  'Kinofilm/Doku eines Produzenten. Freigabe anfragen.'),
    'privat':     ('rot',  'Privatpersonen ohne Zustimmung: Persönlichkeitsrecht. Zustimmung oder unkenntlich machen.'),
}
LIMIT_ZITAT = 30.0   # Sekunden; länger -> Umfang begründen


def judge(c, dur):
    r = c.get('rights') or {}
    kind = r.get('kind', 'sender'); use = r.get('use', 'zitat')
    if r.get('status') == 'geklärt':
        return 'grün', 'Freigabe liegt vor. ' + r.get('note', '')
    if r.get('license', '').upper().startswith(('CC', 'PUBLIC', 'GEMEINFREI')):
        return 'grün', f"Lizenz {r['license']}: Bedingungen (Namensnennung) einhalten."
    level, why = KINDS.get(kind, ('gelb', 'Unbekannte Quelle: einordnen.'))
    if level == 'gelb' and use == 'bebilderung':
        level, why = 'rot', why + ' Als reine Bebilderung (ohne Auseinandersetzung) nicht vom Zitatrecht gedeckt: Lizenz/Freigabe oder eigenes Material.'
    if level == 'gelb' and dur > LIMIT_ZITAT:
        why += f' Länge {dur:.0f} s: Umfang für ein Zitat begründen oder kürzen.'
    return level, (why + ' ' + r.get('note', '')).strip()


def main(pdir):
    cfg, clips, text = load_project(pdir)
    os.makedirs(f"{cfg['dir']}/out", exist_ok=True)
    rows = [('Nr', 'O-Ton', 'Dauer', 'Rechteinhaber', 'Art', 'Nutzung', 'Ampel', 'Begründung / To-do')]
    for s in parse(text, clips):
        if s['type'] != 'oton':
            continue
        c = s['clip'] or {'who': s['who'], 'a': s['a'], 'b': s['b']}
        r = c.get('rights') or {}
        dur = c['b'] - c['a']
        level, why = judge(c, dur)
        rows.append((str(s['no']), s['who'], f'{dur:.0f} s', r.get('owner', '?'), r.get('kind', '?'),
                     r.get('use', 'zitat'), level, why))
    open(f"{cfg['dir']}/out/rechte.csv", 'w', encoding='utf-8').write('\n'.join(';'.join(x) for x in rows) + '\n')
    icon = {'grün': '🟢', 'gelb': '🟡', 'rot': '🔴'}
    md = ['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|' * len(rows[0])]
    md += ['| ' + ' | '.join(x[:6] + (icon.get(x[6], x[6]),) + x[7:]) + ' |' for x in rows[1:]]
    counts = {k: sum(1 for x in rows[1:] if x[6] == k) for k in icon}
    head = (f"Rechte-Ampel: {counts['grün']} grün, {counts['gelb']} gelb, {counts['rot']} rot. "
            "Grundlage: Zitatrecht CH Art. 25 URG / DE § 51 UrhG (Zweck: Beleg/Auseinandersetzung, "
            "Umfang durch den Zweck gedeckt, Quelle nennen). Massgeblich ist das strengere Recht der Länder, "
            "in denen das Video abrufbar ist. Keine Rechtsberatung.")
    open(f"{cfg['dir']}/out/rechte.md", 'w', encoding='utf-8').write(head + '\n\n' + '\n'.join(md) + '\n')
    print(head)


if __name__ == '__main__':
    main(sys.argv[1])
