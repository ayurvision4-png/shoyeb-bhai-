"""Generate realistic-anime sample images with free generators (Pollinations first, AI Horde fallback). Run on Actions (open internet).
python tools/gen_samples.py <outdir>"""
import urllib.request, urllib.parse, json, os, sys, time, threading, base64
OUT = sys.argv[1] if len(sys.argv) > 1 else "samples/anime"; os.makedirs(OUT, exist_ok=True)
STYLE = "semi-realistic anime illustration, highly detailed, beautiful detailed eyes, realistic proportions, soft cinematic lighting, masterpiece, vertical portrait"
P = [
 "young Indian woman in a pastel kurta smiling warmly, cozy home kitchen in morning sunlight, steaming glass of warm water on the counter",
 "handsome young Indian man in a casual shirt walking in a park at golden sunset, relaxed smile, depth of field",
 "kind elderly Indian grandmother in a cotton saree standing in a sunlit courtyard next to a tulsi plant, warm smile",
 "wise middle-aged Indian ayurvedic vaidya in a white kurta with a gentle smile, wooden table with herbs and clay jars",
 "3D animated movie style realistic character, young Indian woman holding a cup of masala chai, cozy window light, soft bokeh",
 "painterly anime background, Indian village home courtyard at sunrise with a tulsi plant, soft clouds, warm light, no people",
 "cinematic anime night scene, young Indian man lying in bed scrolling his phone at 2 am, blue glow on his face, moon outside the window",
 "cinematic anime Diwali festive table with glowing diyas, rangoli and sweets, warm bokeh lights, smiling Indian family softly out of focus",
]
LOG = open(os.path.join(OUT, "log.txt"), "a")
def log(*a): s = " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
def isimg(b): return b[:3] == b"\xff\xd8\xff" or b[:8] == b"\x89PNG\r\n\x1a\n" or b[:4] == b"RIFF"
def pollinations(prompt, seed):
    for model in ("flux", "turbo"):
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) + f"?width=720&height=1280&seed={seed}&model={model}&nologo=true"
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=150).read()
            if isimg(b): return b
            log("pollinations non-image", model, b[:120])
        except Exception as e: log("pollinations fail", model, repr(e)[:160])
    return None
def horde(prompt, seed):
    H = {"apikey": "0000000000", "Content-Type": "application/json", "Client-Agent": "teamex-samples:1:ayurvision"}
    body = {"prompt": prompt + " ### deformed, bad anatomy, extra fingers, text, watermark, ugly, blurry, nsfw", "nsfw": False, "censor_nsfw": True,
            "params": {"sampler_name": "k_euler_a", "cfg_scale": 7, "width": 512, "height": 896, "steps": 28, "n": 1, "seed": str(seed)},
            "models": ["AlbedoBase XL (SDXL)", "Anything Diffusion", "Deliberate"]}
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request("https://aihorde.net/api/v2/generate/async", json.dumps(body).encode(), H), timeout=60)); rid = r["id"]
    except Exception as e:
        log("horde submit fail", repr(e)[:300]); body.pop("models")
        try: r = json.load(urllib.request.urlopen(urllib.request.Request("https://aihorde.net/api/v2/generate/async", json.dumps(body).encode(), H), timeout=60)); rid = r["id"]
        except Exception as e2: log("horde submit fail2", repr(e2)[:300]); return None
    t0 = time.time()
    while time.time() - t0 < 900:
        time.sleep(8)
        try:
            c = json.load(urllib.request.urlopen(urllib.request.Request(f"https://aihorde.net/api/v2/generate/check/{rid}", headers=H), timeout=60))
            if c.get("done"): break
            if c.get("faulted"): log("horde faulted"); return None
        except Exception as e: log("horde check", repr(e)[:120])
    try:
        s = json.load(urllib.request.urlopen(urllib.request.Request(f"https://aihorde.net/api/v2/generate/status/{rid}", headers=H), timeout=60))
        g = s["generations"][0]["img"]
        b = urllib.request.urlopen(urllib.request.Request(g, headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read() if g.startswith("http") else base64.b64decode(g)
        return b if isimg(b) else None
    except Exception as e: log("horde status fail", repr(e)[:200]); return None
res = {}
for i, p in enumerate(P, 1):
    full = p + ", " + STYLE; b = pollinations(full, 100 + i)
    if b: open(f"{OUT}/s{i}.jpg", "wb").write(b); res[i] = "pollinations"; log(i, "ok pollinations", len(b)); time.sleep(4)
miss = [i for i in range(1, len(P) + 1) if i not in res]
def work(i):
    b = horde(P[i - 1] + ", " + STYLE, 200 + i)
    if b: open(f"{OUT}/s{i}.jpg", "wb").write(b); res[i] = "horde"; log(i, "ok horde", len(b))
    else: log(i, "FAILED all")
ts = [threading.Thread(target=work, args=(i,)) for i in miss]; [t.start() for t in ts]; [t.join() for t in ts]
json.dump(res, open(f"{OUT}/result.json", "w")); log("done", res)
