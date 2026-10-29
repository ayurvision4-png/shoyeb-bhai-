"""Animation shots for viral.py: SVG cartoon scenes (anim/engine.html) rendered frame-by-frame with Chromium,
lip-synced to the scene voice. Called as anim.render(spec, wav, secs, out)."""
import os, shutil, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
_s = {}

def _page(font):
    if "pg" in _s: return _s["pg"]
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    try: br = pw.chromium.launch(args=["--disable-gpu"])
    except Exception: br = pw.chromium.launch(channel="chrome", args=["--disable-gpu"])
    pg = br.new_context(viewport={"width": 1080, "height": 1920}, device_scale_factor=1).new_page()
    os.makedirs("tmp/v", exist_ok=True)
    html = open(os.path.join(HERE, "anim", "engine.html")).read().replace("__FONT__", "file://" + (font or ""))
    path = os.path.abspath("tmp/v/engine.html"); open(path, "w").write(html)
    pg.goto("file://" + path); pg.evaluate("document.fonts.load('800 40px F')"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    _s.update(pw=pw, br=br, pg=pg); return pg

def envelope(wav, fps, n):
    try:
        w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
    except Exception: return [0.0] * n
    hop = sr // fps; r = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(max(1, len(x) // hop))])
    p = np.percentile(r, 92) + 1e-9; e = np.clip(r / p, 0, 1); e[e < .12] = 0
    out, c = [], 0.0
    for v in e: c = v if v > c else c * .55 + v * .45; out.append(float(round(c, 3)))
    return (out + [0.0] * n)[:n]

def render(spec, wav, secs, out, fps=30, font=None):
    pg = _page(font); n = int(round(secs * fps))
    pg.evaluate("([s,a,f])=>setup(s,a,f)", [spec, envelope(wav, fps, n + 4), fps])
    d = f"tmp/v/af_{os.getpid()}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for i in range(n):
        pg.evaluate(f"draw({i / fps:.4f})"); pg.screenshot(path=f"{d}/{i:05d}.jpg", type="jpeg", quality=92)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", f"{d}/%05d.jpg", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-vf", "setsar=1", out], check=True)
    shutil.rmtree(d, ignore_errors=True)
