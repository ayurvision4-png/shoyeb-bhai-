"""Scout Pexels candidate videos: thumbnails -> contact sheets; test whether mp4 download works from CI."""
import os, subprocess, requests
from PIL import Image, ImageDraw, ImageFont
H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
ids = []
for l in open("pexels_request.txt"):
    l = l.split("#")[0].strip()
    if l: ids.append(l.split()[0])
os.makedirs("scout_px/thumbs", exist_ok=True)
log = open("scout_px/log.txt", "w")
ok = []
for i in ids:
    fn = f"scout_px/thumbs/{i}.jpg"
    if not os.path.exists(fn):
        try:
            r = requests.get(f"https://images.pexels.com/videos/{i}/free-video-{i}.jpg?auto=compress&cs=tinysrgb&dpr=1&w=360", headers=H, timeout=30)
            if r.ok and len(r.content) > 2000: open(fn, "wb").write(r.content)
            else: log.write(f"thumb {i}: HTTP {r.status_code} {len(r.content)}\n")
        except Exception as e: log.write(f"thumb {i}: {e}\n")
    if os.path.exists(fn): ok.append(i)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
for n in range(0, len(ok), 12):
    chunk = ok[n:n + 12]; cw, ch = 240, 400
    sheet = Image.new("RGB", (cw * 6, ch * 2), (20, 20, 20)); d = ImageDraw.Draw(sheet)
    for k, i in enumerate(chunk):
        im = Image.open(f"scout_px/thumbs/{i}.jpg").convert("RGB"); im.thumbnail((cw, ch - 30))
        x, y = (k % 6) * cw, (k // 6) * ch
        sheet.paste(im, (x, y + 30)); d.text((x + 6, y + 4), i, font=f, fill=(255, 220, 0))
    sheet.save(f"scout_px/sheet_{n // 12:02d}.jpg", quality=80)
# mp4 download test on first 3 ids
for i in ids[:3]:
    for url in (f"https://www.pexels.com/download/video/{i}/?fps=25.0&h=1920&w=1080", f"https://www.pexels.com/download/video/{i}/"):
        out = f"scout_px/test_{i}.mp4"
        r = subprocess.run(["curl", "-sSL", "-A", H["User-Agent"], "-o", out, "-w", "%{http_code} %{size_download} %{url_effective}", url], capture_output=True, text=True)
        log.write(f"mp4 {i} {url} -> {r.stdout} {r.stderr[:200]}\n")
        if os.path.exists(out):
            sz = os.path.getsize(out)
            if sz < 200000: os.remove(out)
            else: break
log.close(); print(open("scout_px/log.txt").read())
