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
    dict(name='beautilook', photo='1000153679.jpg', crop=END_CROP, voice=MALE,
         hook=['Subah. Shaam. Raat.', 'Beautilook: 3 step routine'], cta='Pura pack Rs 3999 | 30 din',
         text='सुबह खाली पेट दो टैबलेट, शाम को भूख लगे तब दो टैबलेट, और रात को सोने से पहले एक टैबलेट। तीनों गर्म पानी के साथ। टीमेक्स ब्यूटीलुक का यह सिंपल तीन स्टेप रूटीन है। पूरा पैक सिर्फ़ उनतालीस सौ निन्यानवे रुपये का, यानी तीस दिन के लिए लगभग एक सौ तैंतीस रुपये रोज़। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='tulsi_drops', photo='1000153688.jpg', crop=None, voice=FEMALE,
         hook=['Mausam badla?', 'Ghar ki immunity routine'], cta='Tulsi Drops 20 ml | Rs 300',
         text='मौसम बदलते ही घर में सबकी फ़िक्र? टीमेक्स तुलसी ड्रॉप्स में पाँच तरह की तुलसी है। बड़े चार बूँद, बच्चे दो बूँद, एक गिलास पानी में, दिन में दो बार। बीस मिलीलीटर की बोतल सिर्फ़ तीन सौ रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='cmd_water_drops', photo='1000153686.jpg', crop=None, voice=MALE,
         hook=['Apna paani badlein', 'CMD Mineral Drops'], cta='40 ml | Rs 699',
         text='जो पानी आप रोज़ पीते हैं, उसे और बेहतर बनाइए। टीमेक्स सी एम डी कंसंट्रेटेड मिनरल ड्रॉप्स। दो सौ मिलीलीटर पानी में तीन बूँद, दिन में पाँच बार। यह पानी को अल्कलाइन और मिनरल युक्त बनाने के लिए है। चालीस मिलीलीटर की बोतल सिर्फ़ छह सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='slim_tea', photo='1000153684.jpg', crop=None, voice=FEMALE,
         hook=['Subah ki chai badlein', 'Teamex Slim Tea'], cta='100 gm | Rs 750',
         text='सुबह की चाय में एक छोटा सा बदलाव करके देखिए। टीमेक्स स्लिम टी, हिबिस्कस, सौंफ, दालचीनी, हल्दी, मुलेठी और अदरक के साथ। एक चम्मच चाय एक कप गर्म पानी में डालिए, छानिए और पीजिए। सौ ग्राम का पैक सिर्फ़ सात सौ पचास रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='hand_wash', photo='handwash.png', crop=None, voice=MALE,
         hook=['Roz ka handwash', 'Teamex Hand Wash'], cta='250 ml | Rs 199',
         text='दिन में कितनी बार हाथ धोते हैं? टीमेक्स हैंडवॉश, फ़ोमिंग फ़ॉर्मूला, जो हाथों को साफ़ और मुलायम रखता है। हर तरह की त्वचा के लिए। ढाई सौ मिलीलीटर की बोतल सिर्फ़ एक सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='noni_toothpaste', photo='toothpaste.png', crop=None, voice=MALE,
         hook=['Subah ki taazgi', 'Teamex Noni Toothpaste'], cta='75 gm Rs 99 | 150 gm Rs 170',
         text='सुबह की शुरुआत हर्बल ताज़गी से। टीमेक्स नोनी टूथपेस्ट, नोनी और एलोवेरा के साथ, रोज़ की दाँतों और मसूड़ों की देखभाल के लिए। पचहत्तर ग्राम सिर्फ़ निन्यानवे रुपये का, और डेढ़ सौ ग्राम एक सौ सत्तर रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='shewell_sanitary_pad', photo='sanitarypad.png', crop=None, voice=FEMALE,
         hook=['Mahine ke un dinon mein', 'Shewell Sanitary Pad'], cta='10 pads XL | 8 pads XXL | Rs 199',
         text='उन दिनों में आराम और भरोसा। शीवेल सैनिटरी पैड, कॉटन जैसा नरम एहसास, एक्स्ट्रा लॉन्ग और चौड़ा बैक। दस पैड एक्स एल, या आठ पैड डबल एक्स एल, सिर्फ़ एक सौ निन्यानवे रुपये में। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='beautilook_b', photo='1000153679.jpg', crop=END_CROP, voice=FEMALE,
         hook=['Khana kam karna', 'hal nahi hai'], cta='Pura pack Rs 3999 | 30 din',
         text='वज़न की चिंता में खाना बहुत कम करना हल नहीं है। टीमेक्स ब्यूटीलुक का तीन स्टेप रूटीन, पैक के हिसाब से, सुबह, शाम और रात। साथ में सही खाना और रोज़ की वॉक। नतीजे हर इंसान में अलग होते हैं। पूरा पैक उनतालीस सौ निन्यानवे रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='tulsi_drops_b', photo='1000153688.jpg', crop=None, voice=MALE,
         hook=['Ek chhoti aadat', 'poore parivar ke liye'], cta='Tulsi Drops 20 ml | Rs 300',
         text='घर में सबके लिए एक छोटी सी आदत। टीमेक्स तुलसी ड्रॉप्स, पाँच तरह की तुलसी का अर्क। चाय या पानी में डालिए, बड़े चार बूँद, बच्चे दो बूँद, दिन में दो बार। रोज़ की इम्यूनिटी रूटीन का हिस्सा। बीस मिलीलीटर, सिर्फ़ तीन सौ रुपये। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='cmd_water_drops_b', photo='1000153686.jpg', crop=None, voice=FEMALE,
         hook=['Saada paani bore?', 'Mineral drops try karein'], cta='40 ml | Rs 699',
         text='सादा पानी बोरिंग लगता है? टीमेक्स सी एम डी मिनरल ड्रॉप्स, पानी में मिनरल्स जोड़ने के लिए। दो सौ मिलीलीटर पानी में सिर्फ़ तीन बूँद, दिन में पाँच बार, पैक पर बताए तरीके से। चालीस मिलीलीटर, छह सौ निन्यानवे रुपये। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='slim_tea_b', photo='1000153684.jpg', crop=None, voice=MALE,
         hook=['Chai ke shaukeen?', '6 herbs wali Slim Tea'], cta='100 gm | Rs 750',
         text='चाय के शौकीन हैं? तो इसे आज़माइए। टीमेक्स स्लिम टी, छह जड़ी-बूटियाँ, हिबिस्कस, सौंफ, दालचीनी, हल्दी, मुलेठी और अदरक। एक चम्मच गर्म पानी में डालिए, छानकर पीजिए। सही खाने और वॉक के साथ इसे रोज़ की आदत बनाइए। सौ ग्राम, सात सौ पचास रुपये। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='hand_wash_b', photo='handwash.png', crop=None, voice=FEMALE,
         hook=['Bachchon se bado tak', 'poore ghar ka hand wash'], cta='250 ml | Rs 199',
         text='बच्चों से बड़ों तक, पूरे घर के लिए हैंडवॉश। टीमेक्स हैंडवॉश, जेंटल फ़ोमिंग फ़ॉर्मूला, हाथों को साफ़ और मुलायम रखता है। ढाई सौ मिलीलीटर की बोतल, सिर्फ़ एक सौ निन्यानवे रुपये। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='noni_toothpaste_b', photo='toothpaste.png', crop=None, voice=FEMALE,
         hook=['Noni + Aloe Vera', 'wala toothpaste?'], cta='75 gm Rs 99 | 150 gm Rs 170',
         text='नोनी और एलोवेरा वाला टूथपेस्ट कभी आज़माया है? टीमेक्स नोनी टूथपेस्ट, रोज़ सुबह और रात के ब्रश के लिए। पचहत्तर ग्राम निन्यानवे रुपये, और डेढ़ सौ ग्राम एक सौ सत्तर रुपये। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='shewell_sanitary_pad_b', photo='sanitarypad.png', crop=None, voice=FEMALE,
         hook=['Har mahine ka', 'bharosemand saathi'], cta='XL | XXL | Rs 199',
         text='हर महीने के लिए एक भरोसेमंद साथी। शीवेल सैनिटरी पैड, नरम और आरामदायक, एक्स्ट्रा लॉन्ग साइज़। एक्स एल और डबल एक्स एल उपलब्ध। सिर्फ़ एक सौ निन्यानवे रुपये से। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='noni_drink', photo='noni_drink.png', crop=None, voice=MALE,
         hook=['Subah ka 30 ml', 'Noni Wellness Drink'], cta='1 litre | Rs 1799',
         text='सुबह की शुरुआत एक छोटी सी आदत से। टीमेक्स नोनी वेलनेस ड्रिंक, नोनी, एलोवेरा, आँवला, अश्वगंधा, ब्राह्मी और तुलसी के साथ। बड़े लोग सुबह खाली पेट तीस मिलीलीटर लें। यह इम्यूनिटी और पाचन को सपोर्ट करता है। एक लीटर की बोतल सत्रह सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='sea_buckthorn', photo='sea_buckthorn.png', crop=None, voice=FEMALE,
         hook=['Antioxidant se bharpoor', 'Sea Buckthorn Drink'], cta='1 litre | Rs 1999',
         text='रोज़ की ऊर्जा के लिए सुबह का तीस मिलीलीटर। टीमेक्स सी बकथॉर्न वेलनेस ड्रिंक, एंटीऑक्सीडेंट से भरपूर। तीस मिलीलीटर ड्रिंक को तीस मिलीलीटर गुनगुने पानी में मिलाकर लीजिए। एक लीटर की बोतल उन्नीस सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='red_aloevera', photo='red_aloevera.png', crop=None, voice=MALE,
         hook=['Khane se pehle', 'Red Aloe Vera Drink'], cta='1 litre | Rs 999',
         text='खाने से पहले एक छोटी सी आदत। टीमेक्स रेड एलोवेरा ड्रिंक, पाचन को सपोर्ट करने वाला हर्बल ड्रिंक। बड़े लोग तीस मिलीलीटर, खाने से पहले, दिन में दो बार। एक लीटर की बोतल सिर्फ़ नौ सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='livofit', photo='livofit.png', crop=None, voice=FEMALE,
         hook=['Jigar ko aaram', 'Livo-Fit Wellness Drink'], cta='1 litre | Rs 2299',
         text='भारी खाना, कम नींद, बाहर का खाना। जिगर को थोड़ा आराम दीजिए। टीमेक्स लिवो फ़िट वेलनेस ड्रिंक, रोज़ तीस मिलीलीटर, जैसा पैक पर लिखा है। यह लिवर वेलनेस को सपोर्ट करता है। एक लीटर की बोतल बाईस सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='berry_drink', photo='berry_drink.png', crop=None, voice=MALE,
         hook=['Berries ka swad', 'Berry Wellness Drink'], cta='1 litre | Rs 2499',
         text='बेरीज़ के स्वाद में रोज़ की वेलनेस। टीमेक्स बेरी वेलनेस ड्रिंक, एंटीऑक्सीडेंट से भरपूर। रोज़ तीस मिलीलीटर, बेहतर नतीजों के लिए दिन में दो बार। एक लीटर की बोतल चौबीस सौ निन्यानवे रुपये की। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='biotin_gummy', photo='biotin_gummy.png', crop=None, voice=FEMALE,
         hook=['Baal aur nakhun ke liye', 'Biotin Gummy'], cta='30 gummies | Rs 599',
         text='बाल और नाखून के लिए रोज़ की एक छोटी आदत। टीमेक्स बायोटिन गमी, तीस गमी का पैक। रोज़ एक से दो गमी, जैसा पैक पर लिखा है। स्वाद में भी बढ़िया। दाम सिर्फ़ पाँच सौ निन्यानवे रुपये। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='boswellia', photo='boswellia.png', crop=None, voice=MALE,
         hook=['Seedhiyan chadhte waqt', 'joint comfort ke liye'], cta='30 caps | Rs 999',
         text='सीढ़ियाँ चढ़ते वक़्त घुटनों की फ़िक्र? टीमेक्स बोसवेलिया कैप्सूल, जोड़ों की सेहत को सपोर्ट करता है। एक कैप्सूल खाने से पहले, जैसा पैक पर लिखा है। तीस कैप्सूल का पैक नौ सौ निन्यानवे रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='calcium_chewable', photo='calcium_chewable.png', crop=None, voice=FEMALE,
         hook=['Haddiyon ki roz ki khuraak', 'Calcium Chewable'], cta='60 tabs | Rs 399',
         text='हड्डियों की रोज़ की खुराक। टीमेक्स कैल्शियम च्यूएबल टैबलेट। रोज़ दो टैबलेट, जैसा पैक पर लिखा है। साठ टैबलेट का पैक सिर्फ़ तीन सौ निन्यानवे रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='nano_curcumin', photo='nano_curcumin.png', crop=None, voice=MALE,
         hook=['Haldi ka naya roop', 'Nano Curcumin'], cta='30 caps | Rs 799',
         text='हल्दी का नया रूप। टीमेक्स नैनो करक्यूमिन कैप्सूल, रोज़ की वेलनेस रूटीन के लिए। तीस कैप्सूल का पैक सात सौ निन्यानवे रुपये का। इस्तेमाल का तरीका पैक पर लिखा है। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='spirulina', photo='spirulina.png', crop=None, voice=FEMALE,
         hook=['Superfood ki aadat', 'Spirulina Tablet'], cta='60 tabs | Rs 699',
         text='सुपरफ़ूड की आदत डालिए। टीमेक्स स्पिरुलिना टैबलेट, रोज़ की न्यूट्रिशन के लिए। साठ टैबलेट का पैक छह सौ निन्यानवे रुपये का। इस्तेमाल का तरीका पैक पर लिखा है। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='detox_tablet', photo='detox_tablet.png', crop=None, voice=MALE,
         hook=['Raat ki chhoti aadat', 'Detox Tablet'], cta='30 tabs | Rs 599',
         text='रात की एक छोटी आदत। टीमेक्स डिटॉक्स टैबलेट, रात को एक टैबलेट, जैसा पैक पर लिखा है। तीस टैबलेट का पैक पाँच सौ निन्यानवे रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='deep_sleep_gummy', photo='deep_sleep_gummy.png', crop=None, voice=FEMALE,
         hook=['Raat ko sukoon se', 'Deep Sleep Gummy'], cta='30 gummies | Rs 599',
         text='रात को सुकून से सोने की तैयारी। टीमेक्स डीप स्लीप गमी, रोज़ एक से दो गमी, जैसा पैक पर लिखा है। तीस गमी का पैक पाँच सौ निन्यानवे रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='multivitamin_gummy', photo='multivitamin_gummy.png', crop=None, voice=MALE,
         hook=['Roz ka multivitamin', 'gummy ke andaaz mein'], cta='30 gummies | Rs 599',
         text='रोज़ का मल्टीविटामिन, अब गमी के अंदाज़ में। टीमेक्स मल्टीविटामिन गमी, रोज़ एक से दो गमी, जैसा पैक पर लिखा है। तीस गमी का पैक पाँच सौ निन्यानवे रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
    dict(name='shilajit_gummy', photo='shilajit_gummy.png', crop=None, voice=FEMALE,
         hook=['Din bhar ki taazgi', 'Shilajit Gummy'], cta='30 gummies | Rs 699',
         text='दिन भर की ताज़गी के लिए। टीमेक्स शिलाजीत गमी, खाने के बाद एक गमी, दिन में दो बार, जैसा पैक पर लिखा है। तीस गमी का पैक छह सौ निन्यानवे रुपये का। ऑर्डर के लिए व्हाट्सऐप करें।'),
]

# --- no prices anywhere: strip price sentences from voiceover and "Rs ..." from on-screen text ---
import re
for _p in PRODUCTS:
    _p["text"] = "".join(x + "।" for x in _p["text"].split("।") if x.strip() and "रुपये" not in x)
    _p["cta"] = re.sub(r"\s*\|?\s*Rs\s*\d+", "", _p["cta"]).strip(" |")

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
