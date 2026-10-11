import re, urllib.request, os
UA={"User-Agent":"Mozilla/5.0"}
out=[]
for s in ["ambient","relaxing","cinematic","meditation","inspirational","soft","piano"]:
    try: h=urllib.request.urlopen(urllib.request.Request(f"https://mixkit.co/free-stock-music/{s}/",headers=UA),timeout=30).read().decode("utf8","ignore")
    except Exception as e: out.append(f"## {s} FAIL {e}"); continue
    out.append(f"## {s}"); out+=list(dict.fromkeys(re.findall(r'https://assets\.mixkit\.co/[^"\' ]+\.mp3',h)))[:15]
    out+=list(dict.fromkeys(re.findall(r'/free-stock-music/([a-z0-9-]+)/',h)))[:20]
open("music.txt","w").write("\n".join(out))
from rembg import remove
from PIL import Image
os.makedirs("cutouts",exist_ok=True)
crops={"1000153684.jpg":(10,120,590,970),"1000153686.jpg":(60,200,480,990),"1000153688.jpg":(100,320,450,850),"1000153679.jpg":(90,40,1090,530)}
for f,c in crops.items():
    im=Image.open(f).convert("RGB").crop(c); remove(im).save("cutouts/"+f.split(".")[0]+".png")
