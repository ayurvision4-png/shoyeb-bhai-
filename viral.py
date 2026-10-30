"""Viral-style Teamex reels (style: "viral" in reels.json).
Hook in the first second, hard cuts every 1-2 s, push-in zoom, word-by-word captions (Hinglish, uppercase,
yellow highlight on *starred* words), step badges, product label, whoosh/hit SFX, progress bar, comment-keyword CTA,
Beautilook end card. No prices. Called from make_reel.make() when reel["style"] == "viral"."""
import os, re, glob, wave, zlib, random, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_reel as M

W, H, FPS = M.W, M.H, M.FPS
YELLOW, WHITE = (255, 212, 0), (255, 255, 255)
TEST = os.environ.get("VIRAL_TEST") == "1"
os.makedirs("tmp/v", exist_ok=True)

# ---------------------------------------------------------------- fonts
def _find_font():
    pats = ["Montserrat*ExtraBold*", "Montserrat*Black*", "Montserrat-Bold*", "Poppins-ExtraBold*", "Poppins-Bold.ttf"]
    def search():
        for p in pats:
            hits = [h for h in glob.glob(f"/usr/share/fonts/**/{p}", recursive=True)
                    if h.lower().endswith((".ttf", ".otf")) and "italic" not in h.lower()]
            if hits: return sorted(hits)[0]
    f = search()
    if not f and os.environ.get("CI"):
        subprocess.run("sudo apt-get install -y -qq fonts-montserrat", shell=True, capture_output=True)
        f = search()
    return f or M.LATIN
FONT = _find_font()
print("viral font:", FONT)

def fit_font(d, text, max_w, size, min_size=40):
    while size > min_size:
        f = ImageFont.truetype(FONT, size)
        if d.textlength(text, font=f) <= max_w: return f
        size -= 4
    return ImageFont.truetype(FONT, min_size)

def parse_words(txt):
    """'Thyroid *wale ye *3' -> [('THYROID',False),('WALE',True),...]"""
    out = []
    for w in txt.split():
        hi = w.startswith("*"); w = w.lstrip("*")
        if w: out.append((w.upper(), hi))
    return out

# ---------------------------------------------------------------- overlay images
def stroke_text(d, x, y, text, font, fill, stroke=9):
    d.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))

def chunk_png(words, out, size=104):
    """one caption chunk, centred, white with yellow highlight words, thick black outline"""
    im = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    text = " ".join(w for w, _ in words)
    f = fit_font(d, text, W - 110, size, 56)
    sp = d.textlength(" ", font=f)
    tw = sum(d.textlength(w, font=f) for w, _ in words) + sp * (len(words) - 1)
    x, y = (W - tw) / 2, 60
    for w, hi in words:
        stroke_text(d, x, y, w, f, YELLOW if hi else WHITE, 10); x += d.textlength(w, font=f) + sp
    im.save(out); return out

def static_layer(sc, out):
    """gradient + TEAMEX logo + centred WhatsApp watermark (same as other reels) + badge + label + big hook text"""
    base = M.logo_layer("")
    d = ImageDraw.Draw(base)
    if sc.get("badge"):
        f = ImageFont.truetype(FONT, 58); t = sc["badge"].upper(); tw = d.textlength(t, font=f)
        x0, y0 = (W - tw) / 2 - 44, 232
        d.rounded_rectangle((x0, y0, x0 + tw + 88, y0 + 104), 52, fill=YELLOW)
        d.text(((W - tw) / 2, y0 + 20), t, font=f, fill=(20, 14, 6))
    if sc.get("label"):
        f = fit_font(d, sc["label"].upper(), W - 200, 54, 34); t = sc["label"].upper(); tw = d.textlength(t, font=f)
        x0, y0 = (W - tw) / 2 - 36, 330
        d.rounded_rectangle((x0, y0, x0 + tw + 72, y0 + 90), 45, fill=(255, 255, 255, 235))
        d.text(((W - tw) / 2, y0 + 14), t, font=f, fill=(20, 14, 6))
    big = sc.get("big")
    if big:
        y = sc.get("big_y", 400); size = sc.get("big_size", 132)
        for ln in big:
            hi = ln.startswith("*"); ln = ln.lstrip("*").upper()
            f = fit_font(d, ln, W - 100, size, 60)
            tw = d.textlength(ln, font=f)
            stroke_text(d, (W - tw) / 2, y, ln, f, YELLOW if hi else WHITE, 12)
            y += int(f.size * 1.22)
    if sc.get("small"):
        f = fit_font(d, sc["small"], W - 120, 38, 26); tw = d.textlength(sc["small"], font=f)
        d.text(((W - tw) / 2, H - 330), sc["small"], font=f, fill=(255, 255, 255, 230), stroke_width=3, stroke_fill=(0, 0, 0))
    base.save(out); return out

def photo_png(path, out):
    im = Image.open(path).convert("RGB")
    bg = im.copy(); sc = max(W / bg.width, H / bg.height); bg = bg.resize((int(bg.width * sc) + 1, int(bg.height * sc) + 1))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(45))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (10, 10, 12)), 0.5)
    s2 = min(1020 / im.width, 1100 / im.height); im = im.resize((int(im.width * s2), int(im.height * s2)))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width, im.height), 36, fill=255)
    bg.paste(im, ((W - im.width) // 2, (H - im.height) // 2 + 20), m); bg.save(out); return out

def img_png(path, out, zoom=1.0, fx=0.5, fy=0.5):
    """full-bleed AI still: drop the generator's corner mark, cover-fit to WxH, optional punch-in crop around (fx, fy)"""
    im = Image.open(path).convert("RGB"); im = im.crop((0, 0, im.width, int(im.height * 0.955)))
    sc = max(W / im.width, H / im.height) * zoom
    big = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x0 = min(max(int(fx * big.width) - W // 2, 0), big.width - W); y0 = min(max(int(fy * big.height) - H // 2, 0), big.height - H)
    big.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2)).save(out); return out

# ---------------------------------------------------------------- audio
SR = 44100
def _wav(path, x):
    x = np.clip(x, -1, 1); a = (x * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())

def make_sfx():
    rng = np.random.default_rng(7)
    # whoosh: band-passed noise sweeping up, fast fade
    n = int(SR * 0.38); t = np.linspace(0, 1, n); noise = rng.standard_normal(n)
    k = np.cumsum(noise); k -= np.convolve(k, np.ones(400) / 400, mode="same")        # crude high-pass -> airy
    env = np.sin(np.pi * t) ** 1.6; _wav("tmp/v/whoosh.wav", k / (np.abs(k).max() + 1e-9) * env * 0.9)
    # hit: low sine drop + click
    n = int(SR * 0.55); t = np.arange(n) / SR; f = 90 * np.exp(-t * 6) + 40
    hit = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) + rng.standard_normal(n) * np.exp(-t * 60) * 0.5
    _wav("tmp/v/hit.wav", hit * 0.95)
    # pop: short rising blip
    n = int(SR * 0.14); t = np.arange(n) / SR; _wav("tmp/v/pop.wav", np.sin(2 * np.pi * (500 + 2500 * t) * t) * np.exp(-t * 28) * 0.8)

def voice(text, vname, out):
    """tts -> trim silence both ends, +8% tempo (punchier) -> wav; returns duration"""
    raw = out.replace(".wav", "_raw.mp3")
    if TEST:
        n = max(1.4, len(text.split()) * 0.34)
        M.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=f=200:d={n:.2f}", "-ac", "1", raw])
    else:
        M.tts(text, vname, raw)
    sil = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03"
    M.run(["ffmpeg", "-y", "-i", raw, "-af", f"{sil},areverse,{sil},areverse,atempo=1.08", "-ar", str(SR), "-ac", "1", out])
    return M.dur(out)

# ---------------------------------------------------------------- video
_test_n = [0]
def get_clip(patterns, seed, used):
    if TEST:
        _test_n[0] += 1; p = f"tmp/clips/test_{_test_n[0]}.mp4"
        M.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"testsrc2=s=1920x1080:r=30:d=6", "-c:v", "libx264", "-pix_fmt", "yuv420p", p]); return p
    import re as _re
    want = {i for i, n in M.SCOUT if _re.search("|".join(patterns), n)}
    p = M.fetch_clip(patterns, seed, used)
    got = os.path.basename(p).split(".")[0]
    print(("CLIP OK " if got in want else "CLIP FALLBACK ") + f"{patterns} -> {got}", flush=True)
    return p

def probe_wh(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip().split(",")
    return int(r[0]), int(r[1])

def clip_shot(clip, secs, out, punch=0.14):
    w0, h0 = probe_wh(clip)
    if w0 / h0 >= W / H: sc = f"scale=w=-2:h='trunc(({H}*1.04+{H}*{punch}*t/{secs:.2f})/2)*2':eval=frame"
    else:                sc = f"scale=w='trunc(({W}*1.04+{W}*{punch}*t/{secs:.2f})/2)*2':h=-2:eval=frame"
    vf = f"[0:v]{sc},crop={W}:{H},fps={FPS},eq=saturation=1.14:contrast=1.07,setsar=1,format=yuv420p[o]"
    M.run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", clip, "-t", f"{secs:.2f}", "-filter_complex", vf, "-map", "[o]", "-an",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out])

def photo_shot(png, secs, out):
    frames = max(2, int(secs * FPS))
    vf = (f"[0:v]scale={W*1.25:.0f}:-2,zoompan=z='min(1.0+0.0012*on,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
          f"setsar=1,format=yuv420p[o]")
    M.run(["ffmpeg", "-y", "-loop", "1", "-i", png, "-t", f"{secs:.2f}", "-filter_complex", vf, "-map", "[o]", "-an",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out])

def make(reel):
    name = reel["name"]
    M.RATE, M.CAPSIZE, M.LIGHT, M.FADE = reel.get("rate", "+8%"), 64, False, 0.0
    make_sfx()
    used, parts, voices, cuts, pops = set(), [], [], [], []          # cuts: absolute times of every shot start
    t0, n_scenes = 0.0, len(reel["scenes"])
    for i, sc in enumerate(reel["scenes"]):
        who = sc.get("v") or ("m" if i % 2 == 0 else "f")
        wav = f"tmp/v/{name}_{i}.wav"; d = voice(sc["say"], M.MALE if who == "m" else M.FEMALE, wav) + 0.12
        shots = sc["shots"]
        n = max(1, min(len(shots), int(d / 0.9)))           # never shorter than ~0.9 s per shot
        shots = shots[:n]; each = d / n
        raws = []
        for j, sh in enumerate(shots):
            o = f"tmp/v/{name}_{i}_{j}.mp4"
            if sh.get("anim"):
                import anim; anim.render(sh["anim"], wav, each, o, FPS, FONT)
                pops += [t0 + j * each + ac["in"] for ac in sh["anim"].get("actors", []) if ac.get("in", 0) > 0.05 and ac.get("kind") != "label"]
            elif sh.get("img"): photo_shot(img_png(sh["img"], f"tmp/v/{name}_{i}_{j}.png", sh.get("zoom", 1.0), sh.get("fx", 0.5), sh.get("fy", 0.5)), each, o)
            elif sh.get("photo"): photo_shot(photo_png(sh["photo"], f"tmp/v/{name}_{i}_{j}.png"), each, o)
            else: clip_shot(get_clip(sh["clip"], zlib.crc32(f"{name}{i}{j}".encode()), used), each, o, sh.get("punch", 0.14))
            raws.append(o); cuts.append(t0 + j * each)
        lst = f"tmp/v/{name}_{i}.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in raws))
        raw = f"tmp/v/{name}_{i}_raw.mp4"; M.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", raw])
        # overlays: static layer + word-by-word caption chunks timed to the voice
        words = parse_words(sc.get("txt", ""))
        chunks, k = [], 0
        while k < len(words):                                # 2 words per chunk (3 when all short)
            take = 3 if k + 3 <= len(words) and sum(len(w) for w, _ in words[k:k + 3]) <= 11 else 2
            chunks.append(words[k:k + take]); k += take
        weights = [sum(len(w) + 2 for w, _ in c) for c in chunks]; tot = sum(weights) or 1
        ins, fc, prev, tt = ["-i", raw, "-i", static_layer(sc, f"tmp/v/{name}_{i}_st.png")], ["[0:v][1:v]overlay[o0]"], "o0", 0.0
        for c, wt in zip(chunks, weights):
            span = (d - 0.05) * wt / tot; cp = chunk_png(c, f"tmp/v/{name}_{i}_c{len(ins)}.png")
            ins += ["-i", cp]; idx = len(ins) // 2 - 1
            fc.append(f"[{prev}][{idx}:v]overlay=x=0:y=1250:enable='between(t,{tt:.2f},{tt + span:.2f})'[o{idx}]"); prev = f"o{idx}"; tt += span
        scene = f"tmp/v/{name}_{i}.mp4"
        M.run(["ffmpeg", "-y", *ins, "-filter_complex", ";".join(fc), "-map", f"[{prev}]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", scene])
        parts.append(scene); voices.append((wav, t0)); t0 += d
    # brand end card
    ew = f"tmp/v/{name}_end.wav"; ed = voice(reel["end_say"], M.FEMALE, ew) + 0.5
    M.card_scene(reel.get("end_cut") or "1000153679.jpg", ed, (lambda p: (M.logo_layer(reel.get("end_cap", "")).save(p), p)[1])(f"tmp/v/{name}_end.png"),
                 f"tmp/v/{name}_endv.mp4", crop=None if reel.get("end_cut") else (90, 40, 1090, 530))
    parts.append(f"tmp/v/{name}_endv.mp4"); voices.append((ew, t0)); cuts.append(t0); total = t0 + ed
    # assemble video + progress bar
    lst = f"tmp/v/{name}_all.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    allv = f"tmp/v/{name}_all.mp4"; M.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", allv])
    vid = f"tmp/v/{name}_vid.mp4"
    M.run(["ffmpeg", "-y", "-i", allv, "-f", "lavfi", "-i", f"color=c=0xFFD400:s={W}x16:r={FPS}:d={total + 1:.2f}",
           "-filter_complex", f"[0:v][1:v]overlay=x='-{W}+{W}*t/{total:.2f}':y={H-16}:shortest=1,format=yuv420p[o]", "-map", "[o]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", vid])
    # audio: voices + sfx on cuts + music ducked under voice
    ains, af = [], []
    for k, (p, st) in enumerate(voices):
        ains += ["-i", p]; ms = int(st * 1000); af.append(f"[{k}:a]adelay={ms}|{ms},volume=1.7[v{k}]")
    nv = len(voices); sfx_in = []
    for k, ct in enumerate(cuts):
        src, vol = ("tmp/v/hit.wav", 0.8) if k == 0 else ("tmp/v/whoosh.wav", 0.55)
        ains += ["-i", src]; idx = nv + k; ms = int(max(0, ct - 0.04) * 1000)
        af.append(f"[{idx}:a]adelay={ms}|{ms},volume={vol}[s{k}]"); sfx_in.append(f"[s{k}]")
    for k, pt in enumerate(pops):
        ains += ["-i", "tmp/v/pop.wav"]; idx = nv + len(cuts) + k; ms = int(max(0, pt - 0.02) * 1000)
        af.append(f"[{idx}:a]adelay={ms}|{ms},volume=0.5[p{k}]"); sfx_in.append(f"[p{k}]")
    mus = f"tmp/v/{name}_mus.mp3"; ok = False
    if not TEST:
        for mid in reel.get("music", [148, 614, 871]):
            try: open(mus, "wb").write(M.get(f"https://assets.mixkit.co/music/{mid}/{mid}.mp3", True)); ok = True; break
            except Exception: continue
    if not ok:
        M.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=f=110:d={total+1}", "-f", "lavfi", "-i", f"sine=f=165:d={total+1}", "-filter_complex",
               "[0:a][1:a]amix=inputs=2,lowpass=f=700,volume=0.4[m]", "-map", "[m]", mus])
    vmix = "".join(f"[v{k}]" for k in range(nv)); mi = nv + len(cuts) + len(pops)
    M.run(["ffmpeg", "-y", *ains, "-stream_loop", "-1", "-i", mus, "-filter_complex",
           ";".join(af) + f";{vmix}amix=inputs={nv}:normalize=0,highpass=f=90,acompressor=threshold=-18dB:ratio=3,asplit=2[vo][sc];"
           + "".join(sfx_in) + f"amix=inputs={len(cuts)+len(pops)}:normalize=0[sfx];"
           f"[{mi}:a]volume=0.55,afade=t=in:d=1.0[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=350[md];"
           f"[vo][md][sfx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7,alimiter=limit=0.89,afade=t=out:st={total-1.2:.1f}:d=1.2[a]",
           "-map", "[a]", "-t", f"{total:.2f}", "-c:a", "aac", "-b:a", "160k", f"tmp/v/{name}_a.m4a"])
    M.run(["ffmpeg", "-y", "-i", vid, "-i", f"tmp/v/{name}_a.m4a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", f"videos/{name}.mp4"])
    print("done", name, round(total, 1), "s")
