"""Gemeinsame Funktionen: Projekt laden, Drehfassung parsen, Clips zuordnen.

Projektordner (generisch, an kein bestimmtes Tool gebunden):
  project.json      Titel, Sprecher, Kanal, Stimme, Folienordner, Links
  drehfassung.md    Teleprompter in der Cue-Syntax (siehe README)
  clips.json        O-Ton-Register: vid, a, b, who, text, ut?, still?, source?, rights?
  slides/s-01.jpg   Folienbilder (aus dem Deck gerendert)
  audio/            TTS-Sätze (von tts.py)
  clips/, stills/   Preview-Clips (von fetch_clips.py --mode preview)
"""
import json, os, re

SENT_RE = re.compile(r'[^.!?]+[.!?]+[»"]?\s*|[^.!?]+$')
TC_RE = re.compile(r'(\d+):(\d{2})(?:[,.](\d))?\s*[–-]\s*(\d+):(\d{2})(?:[,.](\d))?')


def load_project(pdir):
    pdir = os.path.abspath(pdir)
    cfg = json.load(open(os.path.join(pdir, 'project.json'), encoding='utf-8'))
    cfg.setdefault('slides_dir', 'slides')
    cfg.setdefault('voice', 'de_DE-thorsten-high')
    cfg.setdefault('links', {})
    cfg['dir'] = pdir
    clips = json.load(open(os.path.join(pdir, 'clips.json'), encoding='utf-8'))
    text = open(os.path.join(pdir, 'drehfassung.md'), encoding='utf-8').read()
    return cfg, clips, text


def normalize_slides(cfg):
    """pdftoppm nummeriert bei < 10 Seiten s-1.jpg statt s-01.jpg: auf zwei Stellen bringen."""
    d = os.path.join(cfg['dir'], cfg['slides_dir'])
    for f in os.listdir(d) if os.path.isdir(d) else []:
        m = re.match(r'^s-(\d+)\.(jpe?g|png)$', f, re.I)
        if m and len(m.group(1)) == 1:
            os.rename(os.path.join(d, f), os.path.join(d, f's-{int(m.group(1)):02d}.jpg'))


def sentences(t):
    return [s.strip() for s in SENT_RE.findall(t) if s.strip()]


def tosec(m, s, d):
    return int(m) * 60 + int(s) + (int(d) / 10 if d else 0)


def tc(t):
    return f"{int(t // 60)}:{t % 60:04.1f}".replace('.', ',')


def clean(line):
    return line.replace('**', '').strip()


def match_clip(clips, a, b):
    best = min(clips, key=lambda c: abs(c['a'] - a) + abs(c['b'] - b)) if clips else None
    if best and abs(best['a'] - a) + abs(best['b'] - b) < 2:
        return best
    return None


def parse(text, clips):
    """Liefert Segmente: {'type':'slide','slide','label','chapter','text'} oder
    {'type':'oton','who','a','b','clip','chapter','no'}. Abschnitt '## Geparkt' wird ignoriert."""
    segs, slide, label, chapter, last, no = [], 1, '', '', None, 0
    for raw in text.replace('\r', '').split('\n'):
        l = clean(raw)
        if not l or re.match(r'^#\s', l) or l.lower().startswith('sprechtext rund'):
            continue
        m = re.match(r'^##\s*(.+)$', l)
        if m:
            chapter = m.group(1).strip()
            if chapter.lower().startswith('geparkt'):
                break
            continue
        m = re.match(r'^▶?\s*EINBLENDEN[:\s]+(?:Slide\s*)?(\d+)\s*[·\-–:]?\s*(.*)$', l, re.I)
        if m:
            slide, label, last = int(m.group(1)), m.group(2).strip(), 'cue'
            continue
        m = re.match(r'^■?\s*O-TON\s*(.*)$', l, re.I)
        if m:
            rest = m.group(1)
            t = TC_RE.search(rest)
            if not t:
                continue
            a, b = tosec(*t.groups()[:3]), tosec(*t.groups()[3:])
            no += 1
            segs.append({'type': 'oton', 'who': rest.split('·')[0].strip(), 'a': a, 'b': b,
                         'clip': match_clip(clips, a, b), 'chapter': chapter, 'no': no, 'slide': slide})
            last = 'oton'
            continue
        prev = segs[-1] if segs else None
        if prev and prev['type'] == 'slide' and last == 'text' and prev['slide'] == slide:
            prev['text'] += ' ' + l
        else:
            segs.append({'type': 'slide', 'slide': slide, 'label': label, 'chapter': chapter, 'text': l})
        last = 'text'
    return segs


def clip_file(c, folder='clips'):
    return f"{folder}/{c['vid']}_{int(c['a'])}.mp4"


def source_of(c):
    """Quelle eines Clips. Standard: YouTube-ID = vid."""
    return c.get('source') or {'type': 'youtube', 'id': c['vid']}
