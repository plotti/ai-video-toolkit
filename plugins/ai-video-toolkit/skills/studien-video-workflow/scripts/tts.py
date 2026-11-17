"""Sprechtext der Drehfassung Satz für Satz mit Piper TTS vertonen.

  pip install piper-tts  (Stimme: <voice>.onnx + .onnx.json in <projekt>/tts/)
  python tts.py <projekt>

Vorhandene Sätze werden übersprungen. Schreibt audio/<hash>.mp3 und tts/manifest.json (Satz -> {f, d}).
"""
import hashlib, json, os, re, subprocess, sys, wave
from common import load_project, parse, sentences

UNITS = ['', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun']
TEENS = {10: 'zehn', 11: 'elf', 12: 'zwölf', 13: 'dreizehn', 14: 'vierzehn', 15: 'fünfzehn',
         16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn'}
TENS = {2: 'zwanzig', 3: 'dreissig', 4: 'vierzig', 5: 'fünfzig', 6: 'sechzig', 7: 'siebzig', 8: 'achtzig', 9: 'neunzig'}


def n2w(n):
    if n < 10: return UNITS[n]
    if n < 20: return TEENS[n]
    t, u = divmod(n, 10)
    return ((('ein' if u == 1 else UNITS[u]) + 'und') if u else '') + TENS[t]


def speakable(t, extra):
    t = re.sub(r"(\d)'(\d{3})", r"\1\2", t)                       # 11'833 -> 11833
    t = re.sub(r'\b19(\d\d)(ern)?\b', lambda m: 'neunzehnhundert' + n2w(int(m.group(1))) + (m.group(2) or ''), t)
    t = t.replace('«', '').replace('»', '').replace('…', '')
    for k, v in extra.items():                                    # project.json: "pronounce": {"CO2": "C O zwei"}
        t = t.replace(k, v)
    return t


def ffdur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)


def main(pdir):
    cfg, clips, text = load_project(pdir)
    os.makedirs(f"{cfg['dir']}/audio", exist_ok=True); os.makedirs(f"{cfg['dir']}/tts", exist_ok=True)
    sents = [s for seg in parse(text, clips) if seg['type'] == 'slide' for s in sentences(seg['text'])]
    voice = None; man = {}
    for s in sents:
        h = hashlib.sha1(s.encode()).hexdigest()[:12]
        mp3 = f"{cfg['dir']}/audio/{h}.mp3"
        if not os.path.exists(mp3):
            if voice is None:
                from piper import PiperVoice
                from piper.config import SynthesisConfig
                voice = PiperVoice.load(f"{cfg['dir']}/tts/{cfg['voice']}.onnx")
                syn = SynthesisConfig(length_scale=cfg.get('tts_speed', 1.0), noise_scale=0.6, noise_w_scale=0.8)
            wav = f"/tmp/{h}.wav"
            with wave.open(wav, 'wb') as w:
                voice.synthesize_wav(speakable(s, cfg.get('pronounce', {})), w, syn_config=syn)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'apad=pad_dur=0.25',
                            '-codec:a', 'libmp3lame', '-b:a', '64k', mp3], check=True)
        man[s] = {'f': f'audio/{h}.mp3', 'd': round(ffdur(mp3), 2)}
    json.dump(man, open(f"{cfg['dir']}/tts/manifest.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(man), 'Sätze,', round(sum(v['d'] for v in man.values()), 1), 's Sprechzeit')


if __name__ == '__main__':
    main(sys.argv[1])
