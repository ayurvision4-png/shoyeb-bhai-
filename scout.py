import re, urllib.request
UA={"User-Agent":"Mozilla/5.0"}
slugs="turmeric spices herbs ayurveda yoga meditation woman-yoga running jogging woman-running drinking-water healthy-food fruits vegetables laboratory science molecule nature forest morning sunrise wellness spa massage woman-smiling happy-woman walking stretching gym fitness tea honey leaves flowers mortar health".split()
out=[]
for s in slugs:
    try: h=urllib.request.urlopen(urllib.request.Request(f"https://mixkit.co/free-stock-video/{s}/",headers=UA),timeout=30).read().decode("utf8","ignore")
    except Exception as e: out.append(f"## {s} FAIL {e}"); continue
    items=list(dict.fromkeys(re.findall(r'/free-stock-video/([a-z0-9-]+-(\d+))/',h)))
    out.append(f"## {s}"); out+= [f"{i}\t{n}" for n,i in items[:25]]
open("scout.txt","w").write("\n".join(out))
