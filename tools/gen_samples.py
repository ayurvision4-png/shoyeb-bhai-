"""One realistic-anime sample per call (run as a matrix: each job = fresh runner/IP, dodges per-IP free limits).
python tools/gen_samples.py <n 1-8> <outdir>"""
import urllib.request, urllib.parse, os, sys, time
N = int(sys.argv[1]); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
SUBJ = "young Indian woman in a pastel kurta smiling softly, holding a glass of warm water in a sunlit home kitchen, morning light, vertical portrait, upper body"
STY = {
 1: "Makoto Shinkai style cinematic anime film frame, semi-realistic anime face, detailed sparkling anime eyes, glowing sky light, painterly detailed background, masterpiece",
 2: "Studio Ghibli style hand-painted anime, soft watercolor background, gentle warm colors, anime face, cozy",
 3: "modern semi-realistic anime illustration, clean line art, detailed anime eyes, soft cel shading, realistic proportions, high detail, key visual",
 4: "korean webtoon manhwa style semi-realistic digital illustration, elegant detailed face, glossy hair, soft pastel lighting",
 5: "Pixar style 3D animated movie character, realistic skin and hair, big expressive eyes, soft cinematic lighting, 3D render",
 6: "Arcane style painterly realistic anime illustration, textured brush strokes, dramatic rim light, detailed face",
 7: "bold cel-shaded anime like Demon Slayer, strong ink outlines, vivid colors, dynamic anime key art",
 8: "ultra-detailed realistic anime portrait, almost photoreal skin, large anime eyes, shallow depth of field, studio lighting, trending on pixiv",
}
P = SUBJ + ", " + STY[N]
def isimg(b): return b[:3] == b"\xff\xd8\xff" or b[:8] == b"\x89PNG\r\n\x1a\n" or b[:4] == b"RIFF"
def get(url):
    try:
        b = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read()
        if isimg(b): return b
        print("non-image", b[:150], flush=True)
    except Exception as e: print("fail", url[:60], repr(e)[:150], flush=True)
q = urllib.parse.quote(P)
for attempt in range(3):
    for u in (f"https://image.pollinations.ai/prompt/{q}?width=720&height=1280&seed={N*7}&model=flux&nologo=true",
              f"https://image.pollinations.ai/prompt/{q}?width=720&height=1280&seed={N*7}&model=turbo&nologo=true",
              f"https://gen.pollinations.ai/image/{q}?width=720&height=1280&seed={N*7}&model=flux"):
        b = get(u)
        if b: open(f"{OUT}/s{N}.jpg", "wb").write(b); print("ok", N, len(b)); sys.exit(0)
    time.sleep(45)
print("FAILED", N); sys.exit(1)
