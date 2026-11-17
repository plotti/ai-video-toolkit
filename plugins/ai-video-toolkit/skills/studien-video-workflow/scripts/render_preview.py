"""Preview-MP4 aus dem Projekt rendern (Folie links + Sprecher-Platzhalter rechts, O-Töne im Vollbild).

  python render_preview.py <projekt> [--force]

Braucht: ffmpeg, Pillow, tts/manifest.json (tts.py), Folienbilder, Preview-Clips in clips/ (fetch_clips.py --mode preview).
Ergebnis: <projekt>/out/<titel>_Preview.mp4. Segmente werden zwischengespeichert (out/seg/), nur geänderte neu rendern mit --force.
"""
import json, os, re, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
from common import load_project, parse, normalize_slides, sentences, clip_file

W, H = 1920, 1080
NAVY, RED, WHITE, SKY = (15, 45, 92), (200, 16, 46), (255, 255, 255), (157, 178, 214)
FONTS = ['/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf', '/System/Library/Fonts/Supplemental/Arial{}.ttf']


def font(bold, size):
    for f in FONTS:
        p = f.format('-Bold' if bold and 'dejavu' in f else (' Bold' if bold else ''))
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p', '-r', '30',
       '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2']


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def slide_frame(cfg, n, path):
    bg = Image.new('RGB', (W, H), (10, 16, 28))
    sl = Image.open(f"{cfg['dir']}/{cfg['slides_dir']}/s-{n:02d}.jpg").convert('RGB')
    sw = min(int(sl.width * H / sl.height), W - 400); sl = sl.resize((sw, H))
    bg.paste(sl, (0, 0)); d = ImageDraw.Draw(bg)
    for y in range(H):
        k = y / H; d.line([(sw, y), (W, y)], fill=(int(42 - 30 * k), int(58 - 40 * k), int(94 - 62 * k)))
    cx = sw + (W - sw) // 2
    d.ellipse([cx - 95, 330, cx + 95, 560], fill=(59, 76, 114))
    d.rounded_rectangle([cx - 230, 600, cx + 230, 1100], radius=120, fill=(45, 60, 92))
    d.text((sw + 36, 40), cfg.get('speaker', 'Sprecher'), font=font(True, 34), fill=WHITE)
    d.text((sw + 36, 84), cfg.get('channel', ''), font=font(False, 26), fill=SKY)
    d.text((sw + 36, H - 70), 'Sprecher (Platzhalter)', font=font(False, 22), fill=SKY)
    bg.save(path, quality=92)


def oton_overlay(c, no, path):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([60, 50, 290, 104], fill=RED); d.text((76, 58), f'O-TON {no}', font=font(True, 32), fill=WHITE)
    who, _, src = c['who'].partition('·')
    fy = 790 if c.get('ut') else 880; fw, fs = font(True, 40), font(False, 28)
    d.rectangle([60, fy, 60 + d.textlength(who.strip(), font=fw) + 40, fy + 62], fill=NAVY)
    d.text((80, fy + 8), who.strip(), font=fw, fill=WHITE)
    if src.strip():
        d.rectangle([60, fy + 62, 60 + d.textlength(src.strip(), font=fs) + 40, fy + 106], fill=WHITE)
        d.text((80, fy + 68), src.strip(), font=fs, fill=NAVY)
    if c.get('ut'):
        f = font(True, 34); lines = textwrap.wrap(c['ut'], 80)[:3]; y = H - 40 - 46 * len(lines)
        for ln in lines:
            lw = d.textlength(ln, font=f)
            d.rectangle([(W - lw) / 2 - 16, y - 4, (W + lw) / 2 + 16, y + 44], fill=(8, 12, 22, 215))
            d.text(((W - lw) / 2, y), ln, font=f, fill=WHITE); y += 46
    im.save(path)


def main(pdir, force=False):
    cfg, clips, text = load_project(pdir)
    normalize_slides(cfg)
    audio = json.load(open(f"{cfg['dir']}/tts/manifest.json", encoding='utf-8'))
    out = f"{cfg['dir']}/out/seg"; os.makedirs(out, exist_ok=True)
    files = []
    for i, s in enumerate(parse(text, clips)):
        o = f'{out}/{i:03d}.mp4'; files.append(o)
        if os.path.exists(o) and not force:
            continue
        if s['type'] == 'slide':
            png = f'{out}/{i:03d}.jpg'; slide_frame(cfg, s['slide'], png)
            parts = [audio[t]['f'] for t in sentences(s['text']) if t in audio]
            miss = [t for t in sentences(s['text']) if t not in audio]
            if miss: print('ohne Aufnahme (tts.py laufen lassen):', miss[:2])
            lst = f'{out}/{i:03d}.txt'
            open(lst, 'w').write(''.join(f"file '{cfg['dir']}/{p}'\n" for p in parts))
            wav = f'{out}/{i:03d}.wav'
            run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-ar', '48000', '-ac', '2', wav])
            run(['ffmpeg', '-y', '-loop', '1', '-i', png, '-i', wav, '-af', 'apad=pad_dur=0.4', '-shortest',
                 '-tune', 'stillimage'] + ENC + [o])
        else:
            c = s['clip']
            if not c:
                print('O-Ton ohne Clip übersprungen:', s['who']); files.pop(); continue
            ov = f'{out}/{i:03d}.png'; oton_overlay(c, s['no'], ov)
            fc = (f'[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,'
                  f'setsar=1,fps=30[v];[v][1:v]overlay=0:0[o]')
            run(['ffmpeg', '-y', '-i', f"{cfg['dir']}/{clip_file(c)}", '-i', ov, '-filter_complex', fc,
                 '-map', '[o]', '-map', '0:a', '-af', 'loudnorm=I=-18:TP=-2'] + ENC + [o])
        print(i, s['type'], flush=True)
    lst = f"{cfg['dir']}/out/all.txt"
    open(lst, 'w').write(''.join(f"file '{f}'\n" for f in files))
    name = re.sub(r'[^A-Za-z0-9]+', '_', cfg.get('title', 'Video')).strip('_')
    dst = f"{cfg['dir']}/out/{name}_Preview.mp4"
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', dst])
    print('FERTIG', dst)


if __name__ == '__main__':
    main(sys.argv[1], '--force' in sys.argv)
