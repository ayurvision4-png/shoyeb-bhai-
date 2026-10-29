"""python3 anim/preview.py <reel> <scene_idx> t1 t2 ... -> tmp/prev_<reel>_<idx>.jpg contact sheet (no voice, synthetic lip-sync)"""
import sys, json, os, math
sys.path.insert(0, os.getcwd()); import anim
from PIL import Image
reel, idx, ts = sys.argv[1], int(sys.argv[2]), [float(x) for x in sys.argv[3:]]
R = [r for r in json.load(open("reels.json")) if r["name"] == reel][0]
spec = [s for s in R["scenes"][idx]["shots"] if s.get("anim")][0]["anim"]
pg = anim._page(next(iter(__import__("glob").glob("/usr/share/fonts/**/Montserrat*ExtraBold*.ttf", recursive=True)), None) or next(iter(__import__("glob").glob("/usr/share/fonts/**/Poppins-Bold.ttf", recursive=True)), ""))
amps = [0.5 + 0.5 * math.sin(i * 0.9) for i in range(400)]
pg.evaluate("([s,a,f])=>setup(s,a,f)", [spec, amps, 30]); os.makedirs("tmp", exist_ok=True); ims = []
for t in ts:
    pg.evaluate(f"draw({t})"); p = f"tmp/pv_{len(ims)}.png"; pg.screenshot(path=p); ims.append(Image.open(p).convert("RGB").resize((360, 640)))
sh = Image.new("RGB", (360 * len(ims), 640)); [sh.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]
sh.save(f"tmp/prev_{reel}_{idx}.jpg", quality=88); print("tmp/prev_%s_%d.jpg" % (reel, idx))
