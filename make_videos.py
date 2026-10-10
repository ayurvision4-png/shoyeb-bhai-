"""Teamex free video maker. Needs: ffmpeg, Python, Pillow, edge-tts (pip install edge-tts pillow).
Put this file and your 5 product photos in one folder, then run: python make_videos.py
Output: videos/<name>.mp4  (1080x1920, Hindi voiceover, centered WhatsApp watermark, Beautilook end card)."""
import asyncio, os, subprocess, sys
from PIL import Image, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
WATERMARK = "WhatsApp 7596985205"
FONT = os.environ.get("FONT", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
MALE, FEMALE = "hi-IN-MadhurNeural", "hi-IN-SwaraNeural"
END_PHOTO, END_CROP = "1000153679.jpg", (90, 40, 1090, 530)  # 3 Beautilook bottles

PRODUCTS = [
    dict(name="beautilook", photo="1000153679.jpg", crop=END_CROP, voice=MALE,
         hook=["Subah. Shaam. Raat.", "Beautilook: 3 step routine"], cta="Pura pack Rs 3999 | 30 din",
         text="सुबह खाली पेट दो टैबलेट, शाम को भूख लगे तब दो टैबलेट, और रात को सोने से पहले एक टैबलेट। तीनों गर्म पानी के साथ। टीमेक्स ब्यूटीलुक का यह सिंपल तीन स्टेप रूटीन है। पूरा पैक सिर्फ़ उनतालीस सौ निन्यानवे रुपये का, यानी तीस दिन के लिए लगभग एक सौ तैंतीस रुपये रोज़। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="tulsi_drops", photo="1000153688.jpg", crop=None, voice=FEMALE,
         hook=["Mausam badla?", "Ghar ki immunity routine"], cta="Tulsi Drops 20 ml | Rs 300",
         text="मौसम बदलते ही घर में सबकी फ़िक्र? टीमेक्स तुलसी ड्रॉप्स में पाँच तरह की तुलसी है। बड़े चार बूँद, बच्चे दो बूँद, एक गिलास पानी में, दिन में दो बार। बीस मिलीलीटर की बोतल सिर्फ़ तीन सौ रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="cmd_water_drops", photo="1000153686.jpg", crop=None, voice=MALE,
         hook=["Apna paani badlein", "CMD Mineral Drops"], cta="40 ml | Rs 699",
         text="जो पानी आप रोज़ पीते हैं, उसे और बेहतर बनाइए। टीमेक्स सी एम डी कंसंट्रेटेड मिनरल ड्रॉप्स। दो सौ मिलीलीटर पानी में तीन बूँद, दिन में पाँच बार। यह पानी को अल्कलाइन और मिनरल युक्त बनाने के लिए है। चालीस मिलीलीटर की बोतल सिर्फ़ छह सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="slim_tea", photo="1000153684.jpg", crop=None, voice=FEMALE,
         hook=["Subah ki chai badlein", "Teamex Slim Tea"], cta="100 gm | Rs 750",
         text="सुबह की चाय में एक छोटा सा बदलाव करके देखिए। टीमेक्स स्लिम टी, हिबिस्कस, सौंफ, दालचीनी, हल्दी, मुलेठी और अदरक के साथ। एक चम्मच चाय एक कप गर्म पानी में डालिए, छानिए और पीजिए। सौ ग्राम का पैक सिर्फ़ सात सौ पचास रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।"),
    # ---- pdf2 Personal Care (put these 4 photos in the same folder; crop=None uses the whole photo) ----
    dict(name="hand_wash", photo="handwash.jpg", crop=None, voice=MALE,
         hook=["Har baar haath dhoyein", "mulayam bhi rakhein"], cta="Hand Wash 250 ml | Rs 199",
         text="बार-बार हाथ धोने के बाद भी हाथ मुलायम चाहिए? टीमेक्स हैंडवॉश, जेंटल फोमिंग फ़ॉर्मूला, ग्लिसरीन और विटामिन ई के साथ, हर स्किन टाइप के लिए। एक से दो बूँद गीले हाथों पर लीजिए, झाग बनाइए और धो लीजिए। दो सौ पचास मिलीलीटर की बोतल सिर्फ़ एक सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="intimate_wash", photo="intimatewash.jpg", crop=None, voice=FEMALE,
         hook=["Roz ki intimate hygiene", "gentle care ke saath"], cta="SheWell Intimate Wash 100 ml | Rs 299",
         text="रोज़ की इंटिमेट हाइजीन के लिए एक जेंटल क्लींज़र। शीवेल इंटिमेट वॉश, सोया एक्सट्रैक्ट, सी बकथॉर्न और टी ट्री ऑयल के साथ। सिर्फ़ बाहरी इस्तेमाल के लिए, कुछ बूँदें लगाइए और साफ़ पानी से धो लीजिए। सौ मिलीलीटर की बोतल दो सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="noni_toothpaste", photo="tooth.jpg", crop=None, voice=MALE,
         hook=["Noni + Aloe Vera", "herbal toothpaste"], cta="75 gm Rs 99 | 150 gm Rs 170",
         text="रोज़ दो बार ब्रश, हर्बल तरीके से। टीमेक्स नोनी टूथपेस्ट, नोनी और एलोवेरा के साथ, ताज़गी भरे दिन के लिए। दो से तीन ग्राम, यानी पूरी ब्रश की लंबाई, सुबह और रात। पचहत्तर ग्राम सिर्फ़ निन्यानवे रुपये का, और डेढ़ सौ ग्राम एक सौ सत्तर रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="shewell_pad", photo="pad.jpg", crop=None, voice=FEMALE,
         hook=["Un dino mein bhi", "comfort aur confidence"], cta="Shewell Pads | Rs 199",
         text="पीरियड्स के दिनों में आराम और भरोसा चाहिए? टीमेक्स शीवेल सैनिटरी पैड, कॉटन जैसा नर्म एहसास, एक्स्ट्रा लॉन्ग और चौड़ा बैक, ताकि पूरे दिन बेफ़िक्र रहें। एक्स एल और डबल एक्स एल साइज़ में, दाम सिर्फ़ एक सौ निन्यानवे रुपये से। ऑर्डर के लिए व्हाट्सऐप करें।"),
    # ---- pdf2 Personal Care (add your own photo of each pack; crop=None uses the whole photo) ----
    dict(name="hand_wash", photo="handwash.jpg", crop=None, voice=MALE,
         hook=["Roz ka handwash", "Teamex Hand Wash"], cta="250 ml | Rs 199",
         text="दिन में कितनी बार हाथ धोते हैं? टीमेक्स हैंडवॉश, फ़ोमिंग फ़ॉर्मूला, जो हाथों को साफ़ और मुलायम रखता है। हर तरह की त्वचा के लिए। ढाई सौ मिलीलीटर की बोतल सिर्फ़ एक सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="shewell_intimate_wash", photo="intimatewash.jpg", crop=None, voice=FEMALE,
         hook=["Roz ki hygiene", "SheWell Intimate Wash"], cta="100 ml | Rs 299",
         text="रोज़ की पर्सनल हाइजीन के लिए। शीवेल इंटिमेट वॉश, सोया एक्सट्रैक्ट, सी बकथॉर्न और टी ट्री ऑयल के साथ, सिर्फ़ बाहरी इस्तेमाल के लिए। सौ मिलीलीटर की बोतल दो सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="noni_toothpaste", photo="toothpaste.jpg", crop=None, voice=MALE,
         hook=["Subah ki taazgi", "Teamex Noni Toothpaste"], cta="75 gm Rs 99 | 150 gm Rs 170",
         text="सुबह की शुरुआत हर्बल ताज़गी से। टीमेक्स नोनी टूथपेस्ट, नोनी और एलोवेरा के साथ, रोज़ की दाँतों और मसूड़ों की देखभाल के लिए। पचहत्तर ग्राम सिर्फ़ निन्यानवे रुपये का, और डेढ़ सौ ग्राम एक सौ सत्तर रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।"),
    dict(name="shewell_sanitary_pad", photo="sanitarypad.jpg", crop=None, voice=FEMALE,
         hook=["Mahine ke un dinon mein", "Shewell Sanitary Pad"], cta="10 pads XL | 8 pads XXL | Rs 199",
         text="उन दिनों में आराम और भरोसा। शीवेल सैनिटरी पैड, कॉटन जैसा नरम एहसास, एक्स्ट्रा लॉन्ग और चौड़ा बैक। दस पैड एक्स एल, या आठ पैड डबल एक्स एल, सिर्फ़ एक सौ निन्यानवे रुपये में। ऑर्डर के लिए व्हाट्सऐप करें।"),
]

os.makedirs("videos", exist_ok=True); os.makedirs("tmp", exist_ok=True)

def run(cmd): subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout
    return float(out.strip())

def prep(photo, crop, tag):
    im = Image.open(photo).convert("RGB")
    if crop: im = im.crop(crop)
    bg = im.copy(); s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1))
    l, t = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((l, t, l + W, t + H)).filter(ImageFilter.GaussianBlur(45))
    ImageEnhance.Brightness(bg).enhance(0.45).save(f"tmp/{tag}_bg.png")
    s = min(900 / im.width, 1150 / im.height)
    fw, fh = int(im.width * s) // 2 * 2, int(im.height * s) // 2 * 2
    ImageEnhance.Contrast(im.resize((fw, fh))).enhance(1.08).save(f"tmp/{tag}_fg.png")
    return fw, fh

def tts(text, voice, out):
    try:
        import edge_tts
        asyncio.run(edge_tts.Communicate(text, voice, rate="-5%").save(out))
    except Exception as e:  # no internet / edge-tts missing: silent placeholder so layout can be tested
        print("TTS unavailable, using silence:", e)
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(len(text) / 13), out])

def dt(text, tag, i, y, size, alpha=1.0, box=False):
    path = f"tmp/{tag}_t{i}.txt"; open(path, "w", encoding="utf-8").write(text)
    extra = ":box=1:boxcolor=black@0.45:boxborderw=18" if box else ""
    return (f"drawtext=fontfile={FONT}:textfile={path}:fontsize={size}:fontcolor=white@{alpha}:"
            f"borderw=3:bordercolor=black@0.5:x=(w-text_w)/2:y={y}{extra}")

def segment(tag, fw, fh, secs, audio, hook, cta, zoom, out):
    n = int(secs * FPS)
    z = (f"zoompan=z='min(zoom+0.0006,1.12)':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={fw}x{fh}:fps={FPS}"
         if zoom else f"loop=loop={n}:size=1,fps={FPS}")
    texts = [dt(h, tag, i, 150 + i * 90, 62, box=True) for i, h in enumerate(hook)]
    if cta: texts.append(dt(cta, tag, 9, H - 260, 54, box=True))
    texts.append(dt(WATERMARK, tag, 8, "(h-text_h)/2", 58, alpha=0.38))
    fc = f"[1:v]{z}[fg];[0:v][fg]overlay=(W-w)/2:(H-h)/2-40,{','.join(texts)},format=yuv420p[v]"
    cmd = ["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", f"tmp/{tag}_bg.png", "-i", f"tmp/{tag}_fg.png"]
    cmd += (["-i", audio] if audio else ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"])
    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-af", "apad,aresample=44100,aformat=channel_layouts=stereo",
            "-t", str(secs), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", out]
    run(cmd)

end_fw, end_fh = prep(END_PHOTO, END_CROP, "end")
segment("end", end_fw, end_fh, 3, None, ["Teamex Beautilook"], "Order: WhatsApp karein", False, "tmp/end.mp4")

only = sys.argv[1:]
for p in PRODUCTS:
    if only and p["name"] not in only: continue
    tag = p["name"]; fw, fh = prep(p["photo"], p["crop"], tag)
    audio = f"tmp/{tag}.mp3"; tts(p["text"], p["voice"], audio)
    secs = duration(audio) + 0.6
    segment(tag, fw, fh, secs, audio, p["hook"], p["cta"], True, f"tmp/{tag}_main.mp4")
    open(f"tmp/{tag}_list.txt", "w").write(f"file '{tag}_main.mp4'\nfile 'end.mp4'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"tmp/{tag}_list.txt", "-c", "copy", f"videos/{tag}.mp4"])
    print("done:", f"videos/{tag}.mp4", f"{secs + 3:.1f}s")
