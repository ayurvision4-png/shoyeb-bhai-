"""Download candidate Pexels videos, grab 3 frames each, build contact sheets (one row per clip). mp4s are NOT committed."""
import os, subprocess, json
from PIL import Image, ImageDraw, ImageFont
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
os.makedirs("scout_px/sheets", exist_ok=True); os.makedirs("scout_px/tmp", exist_ok=True)
done = set(open("scout_px/done.txt").read().split()) if os.path.exists("scout_px/done.txt") else set()
req = []
for l in open("pexels_request.txt"):
    p = l.split("#")[0].split()
    if p and p[0].isdigit() and p[0] not in done: req.append((p[0], " ".join(p[1:])))
meta = open("scout_px/meta.tsv", "a"); font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
rows = []
for cid, note in req:
    f = f"scout_px/tmp/{cid}.mp4"
    r = subprocess.run(["curl", "-sSL", "-A", UA, "--max-filesize", "90000000", "--max-time", "150", "-o", f, "https://www.pexels.com/download/video/%s/" % cid], capture_output=True, text=True)
    if not os.path.exists(f) or os.path.getsize(f) < 100000: print("FAIL", cid, r.stderr[:100]); continue
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", f], capture_output=True, text=True)
    try: j = json.loads(pr.stdout); w, h = j["streams"][0]["width"], j["streams"][0]["height"]; dur = float(j["format"]["duration"])
    except Exception: print("probe fail", cid); os.remove(f); continue
    frames = []
    for k, fr in enumerate((0.12, 0.5, 0.85)):
        o = f"scout_px/tmp/{cid}_{k}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur*fr:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=-2:210", o])
        if os.path.exists(o): frames.append(o)
    os.remove(f)
    if frames: rows.append((cid, w, h, dur, note, frames)); meta.write(f"{cid}\t{w}x{h}\t{dur:.1f}\t{note}\n"); meta.flush(); done.add(cid)
    print("ok", cid, w, h, round(dur, 1), flush=True)
per = 7; start = len(os.listdir("scout_px/sheets"))
for n in range(0, len(rows), per):
    chunk = rows[n:n + per]; sheet = Image.new("RGB", (1180, 232 * len(chunk)), (18, 18, 18)); d = ImageDraw.Draw(sheet)
    for ri, (cid, w, h, dur, note, frames) in enumerate(chunk):
        d.text((6, ri * 232 + 2), f"{cid}  {w}x{h}  {dur:.0f}s  {note[:40]}", font=font, fill=(255, 220, 0)); x = 6
        for fp in frames:
            im = Image.open(fp).convert("RGB"); sheet.paste(im, (x, ri * 232 + 22)); x += im.width + 6
    sheet.save(f"scout_px/sheets/sheet_{start + n // per:03d}.jpg", quality=78)
open("scout_px/done.txt", "w").write("\n".join(sorted(done)))
for f in os.listdir("scout_px/tmp"): os.remove(f"scout_px/tmp/{f}")
print("sheets:", sorted(os.listdir("scout_px/sheets")))
