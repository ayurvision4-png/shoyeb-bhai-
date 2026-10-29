"""python3 anim/samples.py -> tmp/sheetA.jpg, tmp/sheetB.jpg: numbered style samples of the same scene (Chai vs Paani)"""
import sys, os, math, glob, json, copy
sys.path.insert(0, os.getcwd()); import anim, viral
from PIL import Image, ImageDraw, ImageFont
FONT = viral.FONT; pg = anim._page(FONT)
def A(kind, id, x, y, s, **k): d = dict(kind=kind, id=id, x=x, y=y, s=s); d.update(k); return d
base = [A("cup", "c", 320, 870, .72, name="CHAI BHAI", mood="smug", fx=[dict(t=1.2, pose="fist")]),
        A("glass", "g", 770, 870, .72, name="PAANI DIDI", mood="neutral", look=[-1, 0]),
        A("label", "vs", 540, 790, 1, txt="VS", fs=70, w=130, **{"in": .3})]
OPT = [
 (1, "Cute flat cartoon", dict(actors=base, bg=["#ff9a3c", "#c2410c"], rays=True, speaker="c")),
 (2, "Soft 3D clay", dict(actors=base, look="clay", bg=["#7fd1c7", "#2f8f95"], rays=True, speaker="c")),
 (3, "Sticker pop", dict(actors=base, look="sticker", speaker="c")),
 (4, "Whiteboard doodle", dict(actors=base, look="doodle", dots=0, speaker="c")),
 (5, "Neon night glow", dict(actors=base, look="neon", stars=True, speaker="c")),
 (6, "Comic pop-art", dict(actors=base, look="comic", dots=0, speaker="c")),
 (7, "Human characters", dict(bg=["#1d6f6a", "#0a3d44"], rays=True, speaker="h1", actors=[
     A("human", "h1", 310, 860, .7, female=True, mood="happy", name="RIYA", fx=[dict(t=0, pose="wave")]),
     A("human", "h2", 780, 860, .7, female=False, mood="smug", name="RAJ", look=[-1, 0]),
     A("label", "l1", 310, 625, 1, txt="CHAI", fs=70, col="#ffb347", **{"in": .2}), A("label", "l2", 780, 625, 1, txt="PAANI", fs=70, col="#7fd6ff", **{"in": .4}),
     A("label", "vs", 545, 625, 1, txt="VS", fs=70, w=130, **{"in": .6})])),
 (8, "Text + icon motion", dict(bg=["#ff6b35", "#7a1f9e"], rays=True, speaker=None, actors=[
     A("cup", "c", 300, 960, .8, noface=True, **{"in": .2}), A("glass", "g", 790, 960, .8, noface=True, **{"in": .5}),
     A("label", "t1", 270, 400, 1, txt="CHAI", fs=100, col="#ffd400", **{"in": .2}), A("label", "t2", 790, 400, 1, txt="PAANI", fs=100, col="#7fd6ff", **{"in": .5}),
     A("label", "vs", 545, 540, 1, txt="VS", fs=100, w=190, col="#fff", **{"in": .8}),
     A("star", "s1", 150, 700, .6, float=1, **{"in": 1.0}), A("sparkle", "s2", 930, 1120, .6, **{"in": 1.2})])),
]
amps = [0.5 + 0.5 * math.sin(i * 0.9) for i in range(400)]
os.makedirs("tmp/s", exist_ok=True); tiles = []
f1 = ImageFont.truetype(FONT, 120); f2 = ImageFont.truetype(FONT, 62)
for n, name, spec in OPT:
    pg.evaluate("([s,a,f])=>setup(s,a,f)", [spec, amps, 30]); pg.evaluate("draw(1.7)")
    p = f"tmp/s/o{n}.png"; pg.screenshot(path=p); im = Image.open(p).convert("RGBA")
    st = viral.static_layer({} if n == 8 else {"big": ["SUBAH PEHLE", "*CHAI YA PAANI?"], "big_y": 280, "big_size": 108}, f"tmp/s/st{n}.png"); im.alpha_composite(Image.open(st))
    im.alpha_composite(Image.open(viral.chunk_png(viral.parse_words("Pehle *paani, phir *chai"), f"tmp/s/c{n}.png")), (0, 1250))
    d = ImageDraw.Draw(im); d.ellipse((40, 40, 250, 250), fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=10)
    w = d.textlength(str(n), font=ImageFont.truetype(FONT, 150)); d.text((145 - w / 2, 62), str(n), font=ImageFont.truetype(FONT, 150), fill=(200, 30, 30, 255))
    tw = d.textlength(name, font=f2); d.rounded_rectangle(((1080 - tw) / 2 - 40, 1650, (1080 + tw) / 2 + 40, 1650 + 110), 55, fill=(0, 0, 0, 200)); d.text(((1080 - tw) / 2, 1650 + 20), name, font=f2, fill=(255, 255, 255, 255))
    tiles.append(im.convert("RGB").resize((540, 960)))
for nm, grp in (("A", tiles[:4]), ("B", tiles[4:])):
    sh = Image.new("RGB", (1080 + 12, 960 * 2 // 1 * 1), (20, 20, 20)); sh = Image.new("RGB", (1092, 1932), (20, 20, 20))
    for i, t in enumerate(grp): sh.paste(t, ((i % 2) * 552, (i // 2) * 972))
    sh.save(f"tmp/sheet{nm}.jpg", quality=90); print(f"tmp/sheet{nm}.jpg")
