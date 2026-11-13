# Story quiz cards (1080x1920), Instagram safe zone: keep content between y=250 and y=1650
from PIL import Image, ImageDraw, ImageFont
import sys
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W,H=1080,1920
def font(s): return ImageFont.truetype(F,s)
def wrap(d,text,f,maxw):
    out=[];cur=""
    for w in text.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: out.append(cur);cur=w
    out.append(cur);return out
def fit(d,text,size,maxw):
    while d.textlength(text,font=font(size))>maxw: size-=2
    return font(size)
def story(fn,myth,when):
    im=Image.new("RGB",(W,H));d=ImageDraw.Draw(im)
    top=(38,18,8);bot=(112,64,22)
    for y in range(H):
        t=y/H;d.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    def center(text,f,y,fill):
        w=d.textlength(text,font=f);d.text(((W-w)/2,y),text,font=f,fill=fill)
    center("TEAMEX",font(60),270,(255,255,255))
    f=font(48);lab="AAJ KA QUIZ";w=d.textlength(lab,font=f)
    d.rounded_rectangle(((W-w)/2-50,380,(W+w)/2+50,380+100),50,fill=(255,214,10));d.text(((W-w)/2,380+20),lab,font=f,fill=(40,20,8))
    y=540
    for l in ["SACH ya","JHOOTH?"]:
        center(l,font(140),y,(255,255,255));y+=170
    y=920;fm=font(76)
    for l in wrap(d,myth,fm,W-200):
        center(l,fm,y,(255,214,10));y+=100
    center("Jawab: "+when,fit(d,"Jawab: "+when,50,W-160),1300,(255,255,255))
    lab="Reply karo: SACH ya JHOOTH";f=fit(d,lab,54,W-260);w=d.textlength(lab,font=f)
    d.rounded_rectangle(((W-w)/2-50,1410,(W+w)/2+50,1410+116),58,fill=(255,214,10));d.text(((W-w)/2,1410+(116-f.size)/2-6),lab,font=f,fill=(40,20,8))
    wm=Image.new("RGBA",(W,H),(0,0,0,0));dw=ImageDraw.Draw(wm)
    t="WhatsApp 7596985205";f=font(40);w=dw.textlength(t,font=f);dw.text(((W-w)/2,1600),t,font=f,fill=(255,255,255,120))
    Image.alpha_composite(im.convert("RGBA"),wm).convert("RGB").save(fn,quality=92)
if __name__=="__main__":
    for fn,myth,when in [("q2_1114","Weight ke liye naashta skip karna chahiye?","aaj shaam 7:30 baje reel mein"),
        ("q2_1115","Mobile dekhte hue khana, zyada khila deta hai?","aaj dopahar 1 baje reel mein"),
        ("q2_1116","Sabko roz 8 glass paani zaroori hai?","aaj dopahar 1 baje reel mein"),
        ("q2_1117","Dhoop sirf sardi mein leni chahiye?","aaj dopahar 1 baje reel mein")]:
        story(f"stories/{fn}.jpg",myth,when)
    print("ok")
