import re, urllib.request
UA={"User-Agent":"Mozilla/5.0"}
slugs="washing-hands hand-washing brushing-teeth toothbrush smile bathroom sleeping bed night sleep bedroom hair hair-care woman-hair stairs climbing hiking knee walking-upstairs milk calcium berries strawberries blueberries aloe-vera plant green-juice smoothie juice breakfast kitchen salad dinner yoga-stretching energy morning-routine cotton women-health period girl-smiling cup-of-tea ginger lemon capsules pills vitamins gummies candy turmeric spices herbs ayurveda yoga meditation woman-yoga running jogging woman-running drinking-water healthy-food fruits vegetables laboratory science molecule nature forest morning sunrise wellness spa massage woman-smiling happy-woman walking stretching gym fitness tea honey leaves flowers mortar health".split()
out=[]
for s in slugs:
    try: h=urllib.request.urlopen(urllib.request.Request(f"https://mixkit.co/free-stock-video/{s}/",headers=UA),timeout=30).read().decode("utf8","ignore")
    except Exception as e: out.append(f"## {s} FAIL {e}"); continue
    items=list(dict.fromkeys(re.findall(r'/free-stock-video/([a-z0-9-]+-(\d+))/',h)))
    out.append(f"## {s}"); out+= [f"{i}\t{n}" for n,i in items[:25]]
open("scout2.txt","w").write("\n".join(out))
