"""Carousel factory: python3 carousel_factory.py [names...]  -> carousel/<name>_1..5.jpg from topics.json.
Renders topics whose slide 1 does not exist yet (dedupe). Original graphics only, no prices/claims."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
F="/usr/share/fonts/truetype/google-fonts/"
def font(sz,b=True):
    for n in (["Poppins-Bold.ttf","Poppins-SemiBold.ttf"] if b else ["Poppins-Medium.ttf","Poppins-Regular.ttf","Poppins-Bold.ttf"]):
        if os.path.exists(F+n): return ImageFont.truetype(F+n,sz)
    return ImageFont.load_default()
W,H=1080,1350
GREEN=(12,61,46); DEEP=(8,40,30); GOLD=(255,212,0); CREAM=(250,246,232); WHITE=(255,255,255)
def base():
    im=Image.new("RGB",(W,H),GREEN); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(GREEN[i]*(1-t)+DEEP[i]*t) for i in range(3)))
    return im,d
def fit(d,t,sz,mw,b=True):
    while sz>24 and d.textlength(t,font=font(sz,b))>mw: sz-=2
    return font(sz,b)
def center(d,y,t,sz,fill,b=True,mw=W-120):
    f=fit(d,t,sz,mw,b); w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
def wrap(d,t,f,mw):
    out,cur=[],""
    for w in t.split():
        x=(cur+" "+w).strip()
        if d.textlength(x,font=f)<=mw: cur=x
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def brand(d):
    center(d,60,"TEAMEX",46,WHITE)
    d.rounded_rectangle([(120,H-120),(W-120,H-52)],radius=34,fill=WHITE); center(d,H-108,"WhatsApp 7596985205",40,DEEP)
def foot(d): center(d,H-190,"Yeh dawai nahi hai. Doctor ki salah zaroor lein.",28,(210,225,215),False)
def cover(t,out):
    im,d=base(); brand(d); c=t["cover"]
    center(d,300,c["l1"],190,GOLD,mw=W-100); center(d,520,c["l2"],130,WHITE,mw=W-100)
    for i,l in enumerate(c["sub"]): center(d,730+i*72,l,52,CREAM,False)
    d.rounded_rectangle([(280,930),(800,1040)],radius=55,fill=GOLD); center(d,950,"SAVE KARO",64,DEEP)
    center(d,1090,"Swipe karo  >>",40,CREAM,False); im.save(out+"_1.jpg",quality=92)
def tips(t,n,rows,start,out):
    im,d=base(); brand(d); center(d,170,f"Aadat {start+1} se {start+len(rows)}",70,GOLD); y=300
    for k,(h,b) in enumerate(rows):
        d.rounded_rectangle([(70,y),(W-70,y+256)],radius=36,fill=WHITE)
        d.ellipse([(95,y+24),(175,y+104)],fill=GOLD); num=str(start+k+1); f=font(50); d.text((135-d.textlength(num,font=f)/2,y+30),num,font=f,fill=DEEP)
        d.text((205,y+30),h,font=fit(d,h,54,W-70-205-20),fill=DEEP)
        for i,l in enumerate(wrap(d,b,font(38,False),W-200)[:3]): d.text((100,y+122+i*44),l,font=font(38,False),fill=(60,75,68))
        y+=272
    foot(d); im.save(out+f"_{n}.jpg",quality=92)
def checklist(t,out):
    im,d=base(); brand(d); center(d,150,"Cheat sheet",76,GOLD); center(d,255,"Screenshot kar lijiye",40,CREAM,False)
    d.rounded_rectangle([(60,330),(W-60,H-230)],radius=36,fill=WHITE); y=360
    for i,(h,b) in enumerate(t["tips"]):
        d.rounded_rectangle([(100,y+6),(150,y+56)],radius=10,outline=GREEN,width=5)
        d.text((180,y+4),h,font=fit(d,h,46,W-180-110),fill=DEEP); y+=124
    foot(d); im.save(out+"_4.jpg",quality=92)
def cta(t,out):
    im,d=base(); brand(d)
    center(d,260,"Kise bhejna hai?",100,GOLD,mw=W-100)
    for i,l in enumerate(["Ek dost ko bhejiye","jise ye chahiye"]): center(d,440+i*85,l,62,WHITE,False)
    for i,l in enumerate(["Poora 7 din chart chahiye?","WhatsApp par CHART likho"]): center(d,700+i*70,l,48,CREAM,False)
    d.rounded_rectangle([(190,930),(890,1040)],radius=55,fill=GOLD); center(d,948,"Follow @ayurvision_02",52,DEEP)
    foot(d); im.save(out+"_5.jpg",quality=92)
if __name__=="__main__":
    T=json.load(open("topics.json")); want=sys.argv[1:]; os.makedirs("carousel",exist_ok=True)
    seen=set()
    for t in T:
        key=t["cover"]["l1"]+t["cover"]["l2"]
        if key in seen: print("DUPLICATE topic",t["name"]); continue
        seen.add(key); out="carousel/"+t["name"]
        if (want and t["name"] not in want) or (not want and os.path.exists(out+"_1.jpg")): continue
        assert len(t["tips"])==6, t["name"]
        cover(t,out); tips(t,2,t["tips"][:3],0,out); tips(t,3,t["tips"][3:],3,out); checklist(t,out); cta(t,out); print("rendered",t["name"])
