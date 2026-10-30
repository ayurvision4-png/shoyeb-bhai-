"""One scene image per call: python tools/gen_img.py <key> <outdir>  (prompts in tools/scene_prompts.json)"""
import urllib.request, urllib.parse, os, sys, time, json
K, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
J = json.load(open(os.path.join(os.path.dirname(__file__), "scene_prompts.json")))[K]
q = urllib.parse.quote(J["prompt"]); seed = J["seed"]
def isimg(b): return b[:3] == b"\xff\xd8\xff" or b[:8] == b"\x89PNG\r\n\x1a\n" or b[:4] == b"RIFF"
def get(u):
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=200).read()
        if isimg(b): return b
        print("non-image", b[:150], flush=True)
    except Exception as e: print("fail", u[:70], repr(e)[:150], flush=True)
for attempt in range(3):
    for w, h in ((1080, 1920), (720, 1280)):
        for m in ("flux", "turbo"):
            b = get(f"https://image.pollinations.ai/prompt/{q}?width={w}&height={h}&seed={seed}&model={m}&nologo=true")
            if b: open(f"{OUT}/{K}.jpg", "wb").write(b); print("ok", K, w, h, len(b)); sys.exit(0)
    time.sleep(45)
print("FAILED", K); sys.exit(1)
