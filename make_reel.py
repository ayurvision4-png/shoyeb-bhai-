"""Reference-style Teamex reels: stock b-roll (Mixkit, free license) + short captions + TEAMEX logo
+ Hindi voice (edge-tts) + soft music + product card + Beautilook end card. No prices.
Usage: python make_reel.py <reel_name> [...]   (reels defined in reels.json)"""
import shutil, zlib, os, sys, json, re, subprocess, asyncio, urllib.request, hashlib, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS, FADE = 1080, 1920, 30, 0.5
WATERMARK = "WhatsApp 7596985205"
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEVA = next((p for p in ["/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
                         "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"] if os.path.exists(p)), LATIN)
MALE, FEMALE = "hi-IN-MadhurNeural", "hi-IN-SwaraNeural"
UA = {"User-Agent": "Mozilla/5.0"}
os.makedirs("tmp", exist_ok=True); os.makedirs("videos", exist_ok=True); os.makedirs("tmp/clips", exist_ok=True)

def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: print("FFMPEG FAIL:", " ".join(c)[:300], r.stderr[-1500:]); raise SystemExit(1)
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
def get(url, binary=False):
    d = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    return d if binary else d.decode("utf8", "ignore")

SCOUT = [l.split("\t") for f in ("scout.txt", "scout2.txt") if os.path.exists(f) for l in open(f).read().splitlines() if "\t" in l and not l.startswith("#")]
def fetch_clip(patterns, seed, used):
    rx = re.compile("|".join(patterns))
    cands = [i for i, n in SCOUT if rx.search(n) and i not in used]
    cands = list(dict.fromkeys(cands))
    if not cands:
        rx = re.compile("woman-meditating-in-nature|sunrise|forest|happy-woman-running|woman-doing-yoga|smiling-woman")
        cands = list(dict.fromkeys(i for i, n in SCOUT if rx.search(n) and i not in used))
    if not cands: raise RuntimeError(f"no clip for {patterns}")
    cid = cands[seed % len(cands)]; used.add(cid)
    for q in ("1080", "720", "360"):
        path = f"tmp/clips/{cid}.mp4"
        try:
            open(path, "wb").write(get(f"https://assets.mixkit.co/videos/{cid}/{cid}-{q}.mp4", True)); return path
        except Exception: continue
    raise RuntimeError(f"download failed {cid}")

CAPSIZE = 62
LIGHT = False
RATE = "-4%"
def tts(text, voice, out):
    import edge_tts, time
    last = None
    for k in range(5):
        try:
            asyncio.run(edge_tts.Communicate(text, voice, rate=RATE).save(out))
            if os.path.getsize(out) > 1000: return
        except Exception as e:
            last = e; print("edge-tts retry", k, str(e)[:80]); time.sleep(3 + 4 * k)
    from gtts import gTTS  # backup voice
    print("using gTTS backup")
    gTTS(text, lang="en", tld="co.in").save(out)

def draw_mixed(d, cx, y, text, size, fill, shadow=True):
    shadow = shadow and fill == 'white'
    fd, fl = ImageFont.truetype(DEVA, size), ImageFont.truetype(LATIN, int(size*0.86))
    runs, cur, kind = [], "", None
    for ch in text:
        k = ch.isascii() and not ch.isspace()
        if ch.isspace(): k = kind if kind is not None else False
        if kind is None or k == kind: cur += ch
        else: runs.append((cur, kind)); cur = ch
        kind = k
    runs.append((cur, kind))
    tw = sum(d.textlength(t, font=fl if k else fd) for t, k in runs); x = cx - tw/2
    for t, k in runs:
        f = fl if k else fd
        if shadow: d.text((x+2, y+2), t, font=f, fill=(0,0,0,170))
        d.text((x, y), t, font=f, fill=fill); x += d.textlength(t, font=f)

def logo_layer(caption, light=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ink = (70, 45, 20) if light else "white"
    for yy in range(0 if light else 420): d.line((0, yy, W, yy), fill=(0, 0, 0, int(120*(1-yy/420))))
    for yy in range(0 if light else 650): d.line((0, H-650+yy, W, H-650+yy), fill=(0, 0, 0, int(150*yy/650)))
    f = ImageFont.truetype(LATIN, 64)
    t = "TEAMEX"; w = d.textlength(t, font=f)
    d.text(((W-w)/2, 120), t, font=f, fill=ink)
    d.text(((W+w)/2+4, 118), "®", font=ImageFont.truetype(LATIN, 24), fill=ink)
    if caption:
        fc = ImageFont.truetype(DEVA, 62)
        lines, cur = [], ""
        for wd in caption.split():
            if d.textlength((cur+" "+wd).strip(), font=fc) > W-160 and cur: lines.append(cur); cur = wd
            else: cur = (cur+" "+wd).strip()
        lines.append(cur)
        y = 1560 - 40*(len(lines)-1)
        for ln in lines: draw_mixed(d, W/2, y, ln, CAPSIZE, ink); y += 84
    fw = ImageFont.truetype(LATIN, 40); w = d.textlength(WATERMARK, font=fw)
    d.text(((W-w)/2, H/2-20), WATERMARK, font=fw, fill=(70,45,20,120) if light else (255,255,255,95))
    return im

def broll_scene(clip, secs, layer_png, out):
    # cover-crop to 9:16, gentle push-in, grade slightly, overlay logo/caption/watermark
    vf = (f"[0:v]scale={W*1.12:.0f}:{H*1.12:.0f}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}:(iw-{W})/2:(ih-{H})/2,fps={FPS},eq=saturation=1.08:contrast=1.04,setsar=1[b];[b][1:v]overlay,format=yuv420p[o]")
    run(["ffmpeg","-y","-stream_loop","-1","-i",clip,"-i",layer_png,"-t",f"{secs:.2f}","-filter_complex",vf,"-map","[o]","-an",
         "-c:v","libx264","-preset","veryfast","-crf","20",out])

def combo_image():
    bg = Image.new("RGB", (W, H), (18, 14, 10))
    glow = Image.new("RGB", (W, H), (0, 0, 0)); ImageDraw.Draw(glow).ellipse((100, 650, 980, 1500), fill=(120, 80, 20))
    bg = Image.blend(bg, glow.filter(ImageFilter.GaussianBlur(220)), 0.8)
    def tile(path, crop, w, h):
        im = Image.open(path).convert("RGB").crop(crop); s = min((w-20)/im.width, (h-20)/im.height)
        im = im.resize((int(im.width*s), int(im.height*s)))
        t = Image.new("RGB", (w, h), (244, 242, 238)); t.paste(im, ((w-im.width)//2, (h-im.height)//2))
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), 36, fill=255); return t, m
    t, m = tile("1000153679.jpg", (90, 40, 1090, 530), 960, 470); bg.paste(t, (60, 330), m)
    for k, (p, c) in enumerate([("1000153684.jpg", (20, 130, 556, 970)), ("1000153686.jpg", (60, 200, 470, 970)), ("1000153688.jpg", (110, 330, 440, 830))]):
        t, m = tile(p, c, 300, 560); bg.paste(t, (60 + k*330, 830), m)
    bg.save("tmp/combo_full.png"); return "tmp/combo_full.png"

def dark_bg():
    if LIGHT:
        bg = Image.new("RGB", (W, H), (247, 240, 227)); gl = Image.new("RGB", (W, H), (255, 255, 255)); ImageDraw.Draw(gl).ellipse((60, 420, 1020, 1480), fill=(214, 232, 190))
        return Image.blend(bg, gl.filter(ImageFilter.GaussianBlur(200)), 0.7)
    bg = Image.new("RGB", (W, H), (14, 11, 8))
    glow = Image.new("RGB", (W, H), (0, 0, 0)); g = ImageDraw.Draw(glow); g.ellipse((60, 520, 1020, 1480), fill=(150, 100, 30))
    return Image.blend(bg, glow.filter(ImageFilter.GaussianBlur(230)), 0.85)

def paste_cut(bg, f, box_w, box_h, cx, top):
    im = Image.open(f).convert("RGBA"); im = im.crop(im.getbbox())
    sc = min(box_w/im.width, box_h/im.height); im = im.resize((int(im.width*sc), int(im.height*sc)), Image.LANCZOS)
    x, y = int(cx - im.width/2), top
    sh = Image.new("RGBA", bg.size, (0,0,0,0)); ImageDraw.Draw(sh).ellipse((x, y+im.height-25, x+im.width, y+im.height+35), fill=(0,0,0,170))
    bg.paste(Image.alpha_composite(bg.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(18))).convert("RGB"))
    bg.paste(im, (x, y), im)

def card_cut(files, out_png):
    bg = dark_bg()
    if len(files) == 1: paste_cut(bg, files[0], 880, 1000, W/2, 340)
    else:
        paste_cut(bg, files[0], 940, 420, W/2, 300)
        n = len(files)-1; slot = W/(n)
        for k, f in enumerate(files[1:]): paste_cut(bg, f, slot-60, 560, slot*k+slot/2, 800)
    bg.save(out_png)

def card_scene(photo, secs, layer_png, out, dark=True, crop=None):
    if isinstance(photo, list):
        card_cut(photo, "tmp/card.png")
        vf = (f"[0:v]scale={W*1.1:.0f}:-2,zoompan=z='1+0.0008*on':d={int(secs*FPS)}:s={W}x{H}:fps={FPS}[b];[b][1:v]overlay,format=yuv420p[o]")
        run(["ffmpeg","-y","-loop","1","-i","tmp/card.png","-i",layer_png,"-t",f"{secs:.2f}","-filter_complex",vf,"-map","[o]","-an","-c:v","libx264","-preset","veryfast","-crf","20",out]); return
    if photo == "COMBO":
        combo_image(); shutil.copy("tmp/combo_full.png", "tmp/card.png")
        vf = (f"[0:v]scale={W*1.1:.0f}:-2,zoompan=z='1+0.0008*on':d={int(secs*FPS)}:s={W}x{H}:fps={FPS}[b];[b][1:v]overlay,format=yuv420p[o]")
        run(["ffmpeg","-y","-loop","1","-i","tmp/card.png","-i",layer_png,"-t",f"{secs:.2f}","-filter_complex",vf,"-map","[o]","-an","-c:v","libx264","-preset","veryfast","-crf","20",out]); return
    im = Image.open(photo).convert("RGB")
    if crop: im = im.crop(crop)
    bg = Image.new("RGB", (W, H), (18, 14, 10))
    glow = Image.new("RGB", (W, H), (0, 0, 0)); g = ImageDraw.Draw(glow); g.ellipse((100, 650, 980, 1500), fill=(120, 80, 20))
    bg = Image.blend(bg, glow.filter(ImageFilter.GaussianBlur(220)), 0.8)
    s = min(980/im.width, 1150/im.height); im = im.resize((int(im.width*s), int(im.height*s)))
    # soften photo background edges with a rounded mask
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.width,im.height), 40, fill=255)
    bg.paste(im, ((W-im.width)//2, 380), m); bg.save("tmp/card.png")
    vf = (f"[0:v]scale={W*1.1:.0f}:-2,zoompan=z='1+0.0008*on':d={int(secs*FPS)}:s={W}x{H}:fps={FPS}[b];[b][1:v]overlay,format=yuv420p[o]")
    run(["ffmpeg","-y","-loop","1","-i","tmp/card.png","-i",layer_png,"-t",f"{secs:.2f}","-filter_complex",vf,"-map","[o]","-an",
         "-c:v","libx264","-preset","veryfast","-crf","20",out])

def make(reel):
    global RATE, CAPSIZE, LIGHT, FADE
    name, voice = reel["name"], reel.get("voice_name") or (MALE if reel.get("voice") == "male" else FEMALE)
    RATE, CAPSIZE, LIGHT, FADE = reel.get("rate", "-4%"), reel.get("capsize", 62), reel.get("theme") == "light", reel.get("fade", 0.5)
    used, scenes, t0 = set(), [], 0.0
    for i, sc in enumerate(reel["scenes"]):
        a = f"tmp/{name}_{i}.mp3"; tts(sc["say"], voice, a); d = dur(a) + 0.15
        layer = f"tmp/{name}_{i}.png"; logo_layer(sc.get("cap", ""), light=LIGHT and "card" in sc).save(layer)
        out = f"tmp/{name}_{i}.mp4"
        extra = FADE if i < len(reel["scenes"]) + 1 else 0
        if sc.get("card"): card_scene(sc["card"], d + extra, layer, out, crop=tuple(sc["crop"]) if sc.get("crop") else None)
        elif sc.get("multi"):
            n = len(sc["multi"]); each = (d + extra) / n; parts = []
            for j, pats in enumerate(sc["multi"]):
                pj = f"tmp/{name}_{i}_{j}.mp4"; broll_scene(fetch_clip(pats, zlib.crc32(f'{name}{i}{j}'.encode()), used), each + 0.05, layer, pj); parts.append(pj)
            open(f"tmp/{name}_{i}.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
            run(["ffmpeg","-y","-f","concat","-safe","0","-i",f"tmp/{name}_{i}.txt","-c","copy",out])
        else: broll_scene(fetch_clip(sc["clips"], zlib.crc32(f'{name}{i}'.encode()), used), d + extra, layer, out)
        scenes.append((out, d, a))
    # end card: Beautilook bottles
    ea = f"tmp/{name}_end.mp3"; tts(reel["end_say"], voice, ea); ed = dur(ea) + 0.8
    elayer = f"tmp/{name}_end.png"; logo_layer(reel.get("end_cap", ""), light=LIGHT).save(elayer)
    card_scene(reel.get("end_cut") or "1000153679.jpg", ed, elayer, f"tmp/{name}_end.mp4", crop=None if reel.get("end_cut") else (90, 40, 1090, 530))
    scenes.append((f"tmp/{name}_end.mp4", ed, ea))
    # video: xfade chain
    inputs, fc, off, prev = [], [], 0.0, "0:v"
    for k, (p, d, a) in enumerate(scenes): inputs += ["-i", p]
    for k in range(1, len(scenes)):
        off += scenes[k-1][1]
        lab = f"x{k}"; fc.append(f"[{prev}][{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}[{lab}]"); prev = lab
    total = off + scenes[-1][1]
    run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(fc),"-map",f"[{prev}]","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",f"tmp/{name}_v.mp4"])
    # audio: voices at scene starts + soft music pad
    ains, af, start = [], [], 0.0
    for k, (p, d, a) in enumerate(scenes):
        ains += ["-i", a]; af.append(f"[{k}:a]adelay={int(start*1000)}|{int(start*1000)},volume=1.6[v{k}]"); start += d
    mus = f"tmp/{name}_mus.mp3"; ok = False
    for mid in reel.get("music", [127, 292, 184]):
        try: open(mus, "wb").write(get(f"https://assets.mixkit.co/music/{mid}/{mid}.mp3", True)); ok = True; break
        except Exception: continue
    if not ok:
        run(["ffmpeg","-y","-f","lavfi","-i",f"sine=f=110:d={total+1}","-f","lavfi","-i",f"sine=f=165:d={total+1}","-filter_complex","[0:a][1:a]amix=inputs=2,lowpass=f=700,volume=0.4[m]","-map","[m]",mus])
    mix = "".join(f"[v{k}]" for k in range(len(scenes)))
    run(["ffmpeg","-y",*ains,"-stream_loop","-1","-i",mus,"-filter_complex",";".join(af)+
         f";{mix}amix=inputs={len(scenes)}:normalize=0,highpass=f=90,acompressor=threshold=-18dB:ratio=3,asplit=2[vo][sc];"
         f"[{len(scenes)}:a]volume=0.5,afade=t=in:d=1.5[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
         f"[vo][md]amix=inputs=2:normalize=0,afade=t=out:st={total-1.5:.1f}:d=1.5[a]",
         "-map","[a]","-t",f"{total:.2f}","-c:a","aac","-b:a","160k",f"tmp/{name}_a.m4a"])
    run(["ffmpeg","-y","-i",f"tmp/{name}_v.mp4","-i",f"tmp/{name}_a.m4a","-c:v","copy","-c:a","copy","-shortest","-movflags","+faststart",f"videos/{name}.mp4"])
    print("done", name, round(total, 1), "s")

if __name__ == "__main__":
    reels = {r["name"]: r for r in json.load(open("reels.json"))}
    for n in sys.argv[1:]: make(reels[n])
