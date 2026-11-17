"""O-Töne aus den Originalquellen holen.

  python fetch_clips.py <projekt> --mode preview          # 720p, genau a–b, nach clips/ + stills/ (für Mockup & Preview)
  python fetch_clips.py <projekt> --mode schnitt [--pad 5] # 1080p, a-pad bis b+pad, nach out/schnitt_1080/ + Schnittliste.csv

Nur O-Töne, die in der Drehfassung vorkommen (nicht der Abschnitt «## Geparkt»), ausser --all.
Vorhandene Dateien werden übersprungen; man kann das Skript beliebig oft wiederholen (z.B. in kurzen Schritten).
Quellen (clips.json -> "source"):
  {"type":"youtube","id":"…"}                         Standard, wenn "source" fehlt: vid = YouTube-ID
  {"type":"hls","info_json":"vinfo.json","video_format":"…","audio_format":"…","referer":"https://…"}
       info_json = Ausgabe von  yt-dlp -J --referer <seite> <player-url>  (signierte URLs laufen ab -> neu holen)
  {"type":"file","path":"/pfad/zur/datei.mp4"}       lokale Datei (z.B. eigene Aufnahme, gekaufte Footage)
  {"type":"url","url":"https://…"}                    alles andere, das yt-dlp kann
Braucht yt-dlp und ffmpeg (YouTube blockiert oft Rechenzentren -> auf dem eigenen Rechner ausführen).
"""
import argparse, json, os, re, subprocess, urllib.parse, urllib.request
from common import load_project, parse, source_of, clip_file, tc

ap = argparse.ArgumentParser()
ap.add_argument('project'); ap.add_argument('--mode', choices=['preview', 'schnitt'], default='preview')
ap.add_argument('--pad', type=float, default=5.0); ap.add_argument('--all', action='store_true')
args = ap.parse_args()
cfg, clips, text = load_project(args.project)
D = cfg['dir']
PRE = args.mode == 'preview'
pad = 0.0 if PRE else args.pad
height = 720 if PRE else 1080


def ok_video(p, want):
    if not os.path.exists(p): return False
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type',
                                    '-of', 'json', p], capture_output=True, text=True).stdout or '{}')
    kinds = {s['codec_type'] for s in pr.get('streams', [])}
    return {'video', 'audio'} <= kinds and abs(float(pr['format']['duration']) - want) < 1.0


def ytdlp(target, a, b, out):
    for attempt in range(3):
        if os.path.exists(out): os.remove(out)
        subprocess.run(['yt-dlp', '-q', '-f', 'bv*+ba/b', '-S', f'res:{height},vcodec:h264', '--merge-output-format', 'mp4',
                        '--download-sections', f'*{a}-{b}', '--force-keyframes-at-cuts', '-o', out, target],
                       capture_output=True, text=True)
        if ok_video(out, b - a): return True        # yt-dlp liefert manchmal nur Ton -> erneut
    return False


def hls(src, a, b, out):
    info = json.load(open(os.path.join(D, src['info_json'])))
    fm = {f['format_id']: f for f in info['formats']}
    H = {'Referer': src.get('referer', ''), 'User-Agent': 'Mozilla/5.0'}
    get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read()

    def grab(fid, dst):
        url = fm[fid]['url']; t = 0; init = None; segs = []; dur = 0
        for line in get(url).decode().splitlines():
            if line.startswith('#EXT-X-MAP'): init = urllib.parse.urljoin(url, line.split('URI="')[1].split('"')[0])
            elif line.startswith('#EXTINF'): dur = float(line.split(':')[1].split(',')[0])
            elif line and not line.startswith('#'):
                if t + dur >= a and t <= b: segs.append((t, urllib.parse.urljoin(url, line)))
                t += dur
        with open(dst, 'wb') as f:
            if init: f.write(get(init))
            for _, u in segs: f.write(get(u))
        return segs[0][0]
    vf = src['video_format'] if not PRE else src.get('preview_video_format', src['video_format'])
    tv = grab(vf, '/tmp/_v.mp4'); ta = grab(src['audio_format'], '/tmp/_a.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a - tv), '-i', '/tmp/_v.mp4', '-ss', str(a - ta),
                    '-i', '/tmp/_a.mp4', '-t', str(b - a), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264',
                    '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', out], check=True)
    return ok_video(out, b - a)


def local(path, a, b, out):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-i', path, '-t', str(b - a),
                    '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', out], check=True)
    return ok_video(out, b - a)


def finish(raw, dst):
    vf = f'scale=-2:{height}' if PRE else \
        'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast',
                    '-crf', '23' if PRE else '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-movflags', '+faststart', dst + '.tmp.mp4'], check=True)
    os.replace(dst + '.tmp.mp4', dst)


segs = [s for s in parse(text, clips) if s['type'] == 'oton']
items = [(s['no'], s['clip'], s['who']) for s in segs if s['clip']]
if args.all:
    items = [(i + 1, c, c['who'].split('·')[0]) for i, c in enumerate(clips)]
outdir = f'{D}/clips' if PRE else f'{D}/out/schnitt_1080'
os.makedirs(outdir, exist_ok=True); os.makedirs(f'{D}/stills', exist_ok=True)
rows = ['Nr;Datei;Einstieg im File;Ausstieg im File;Original-Timecode;Quelle']
for no, c, who in items:
    slug = re.sub(r'[^A-Za-z0-9]+', '_', who.encode('ascii', 'ignore').decode()).strip('_')[:40]
    dst = f'{D}/{clip_file(c)}' if PRE else f'{outdir}/OT{no:02d}_{slug}.mp4'
    a, b = max(0.0, c['a'] - pad), c['b'] + pad
    src = source_of(c)
    link = src.get('url') or (f"https://www.youtube.com/watch?v={src['id']}&t={int(c['a'])}s" if src['type'] == 'youtube'
                             else src.get('referer') or src.get('path', ''))
    rows.append(f"{no};{os.path.basename(dst)};{tc(c['a'] - a)};{tc(c['a'] - a + c['b'] - c['a'])};{tc(c['a'])}–{tc(c['b'])};{link}")
    if os.path.exists(dst):
        continue
    raw = f'/tmp/_raw_{no}.mp4'
    if src['type'] == 'youtube': good = ytdlp(f"https://www.youtube.com/watch?v={src['id']}", a, b, raw)
    elif src['type'] == 'url': good = ytdlp(src['url'], a, b, raw)
    elif src['type'] == 'hls': good = hls(src, a, b, raw)
    else: good = local(src['path'], a, b, raw)
    if not good:
        print('FEHLER', no, who, '(Quelle prüfen, ggf. info_json erneuern)', flush=True); continue
    finish(raw, dst)
    if PRE and not os.path.exists(f"{D}/stills/{c['vid']}_{int(c['a'])}.jpg"):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '2', '-i', dst, '-frames:v', '1', '-vf', 'scale=1280:-2',
                        f"{D}/stills/{c['vid']}_{int(c['a'])}.jpg"])
    print('OK', no, os.path.basename(dst), flush=True)
if not PRE:
    open(f'{outdir}/Schnittliste.csv', 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
    print('Schnittliste.csv geschrieben')
