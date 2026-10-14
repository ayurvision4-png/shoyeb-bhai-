import urllib.request, zlib, os
os.makedirs("audio", exist_ok=True)
for ln in open("audio_urls.tsv", encoding="utf-8"):
    if "\t" not in ln: continue
    text, url = ln.rstrip("\n").split("\t", 1)
    p = f"audio/{zlib.crc32(text.encode()):08x}.mp3"
    if os.path.exists(p) and os.path.getsize(p) > 1000: continue
    try:
        urllib.request.urlretrieve(url, p); print("ok", p, os.path.getsize(p))
    except Exception as e: print("FAIL", p, e)
