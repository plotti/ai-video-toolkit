"""Schnitt-Mockup (index.html) aus template.html + Projekt bauen.

  python build_mockup.py <projekt>

Schreibt <projekt>/index.html. Die Seite referenziert relativ: <slides_dir>/s-NN.jpg, audio/, clips/, stills/.
Für ein Artifact den ganzen Projektordner (ohne Rohmaterial) veröffentlichen.
"""
import glob, hashlib, json, os, sys
from common import load_project, parse, normalize_slides

HERE = os.path.dirname(os.path.abspath(__file__))


def main(pdir):
    cfg, clips, text = load_project(pdir)
    normalize_slides(cfg)
    man_p = f"{cfg['dir']}/tts/manifest.json"
    audio = json.load(open(man_p, encoding='utf-8')) if os.path.exists(man_p) else {}
    nslides = len(glob.glob(f"{cfg['dir']}/{cfg['slides_dir']}/s-*.jpg"))
    segs = parse(text, clips)
    used = {id(s['clip']) for s in segs if s['type'] == 'oton' and s['clip']}
    missing = [s['who'] for s in segs if s['type'] == 'oton' and not s['clip']]
    version = hashlib.sha1(text.encode()).hexdigest()[:8]           # neue Fassung -> neuer Speicherschlüssel
    t = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    rep = {
        '{{TITLE}}': cfg.get('title', 'Schnitt-Mockup'),
        '{{H1}}': cfg.get('title', 'Schnitt-Mockup') + ' – Schnitt-Mockup',
        '{{SPEAKER}}': cfg.get('speaker', 'Sprecher'),
        '{{CHANNEL}}': cfg.get('channel', ''),
        '{{DREHFASSUNG}}': text.replace('</script>', '<\\/script>'),
        '{{AUDIO}}': json.dumps(audio, ensure_ascii=False),
        '{{CLIPS}}': json.dumps([c for c in clips if id(c) in used], ensure_ascii=False, indent=1),
        '{{LINKS}}': json.dumps(cfg['links'], ensure_ascii=False),
        '{{NSLIDES}}': str(max(nslides, 1)),
        '{{SLIDE_DIR}}': cfg['slides_dir'],
        '{{VERSION}}': version,
        '{{VOICE}}': cfg['voice'],
    }
    for k, v in rep.items():
        t = t.replace(k, v)
    open(f"{cfg['dir']}/index.html", 'w', encoding='utf-8').write(t)
    print(f"index.html: {len(segs)} Segmente, {len(used)} Clips, {nslides} Folien, {len(audio)} Sätze vertont")
    if missing:
        print('WARNUNG: O-Töne ohne Clip im Register:', missing)


if __name__ == '__main__':
    main(sys.argv[1])
