"""Voice lab 2. usage: python voicelab2.py edge|kokoro|parler|asr"""
import sys, os, subprocess, re, difflib, glob
T = ("सच या झूठ? घी खाने से वज़न बढ़ता है? जवाब है, मात्रा का खेल। दाल-सब्ज़ी के साथ थोड़ा सा घी, रोज़ दस मिनट की सैर, "
     "और विटामिन डी के लिए थोड़ी धूप। रोज़ एक देसी आदत के लिए फ़ॉलो कीजिए, और फ्री चार्ट के लिए, कमेंट में, चार्ट लिखिए।")
POLISH = ("highpass=f=85,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.1:g=2.5,"
          "acompressor=threshold=-21dB:ratio=3:attack=6:release=90,loudnorm=I=-16:TP=-1.5:LRA=7")
def run(cmd, **k):
    print(">>", cmd if isinstance(cmd, str) else " ".join(cmd), flush=True); return subprocess.run(cmd, **k)
mode = sys.argv[1]
if mode == "edge":
    os.makedirs("voicelab2/edge", exist_ok=True)
    run("edge-tts --list-voices | grep -E 'hi-IN|en-IN|bn-IN' | tee voicelab2/edge/voices.txt", shell=True)
    for g, v in (("m", "hi-IN-MadhurNeural"), ("f", "hi-IN-SwaraNeural")):
        # P0 = EXACTLY what production does today: edge rate +8% then ffmpeg atempo=1.08 (=> ~1.17x)
        run(["edge-tts", "--voice", v, "--rate=+8%", "--text", T, "--write-media", f"tmp_{g}.mp3"])
        run(["ffmpeg", "-v", "error", "-y", "-i", f"tmp_{g}.mp3", "-af", "atempo=1.08", f"voicelab2/edge/P0_{g}_production_now.mp3"])
        # N1 = natural speed (no extra speed-up), light polish
        run(["edge-tts", "--voice", v, "--rate=-4%", "--pitch=-2Hz" if g == "m" else "--pitch=+0Hz", "--text", T, "--write-media", f"tmp_{g}n.mp3"])
        run(["ffmpeg", "-v", "error", "-y", "-i", f"tmp_{g}n.mp3", "-af", POLISH, "-b:a", "128k", f"voicelab2/edge/N1_{g}_natural_polished.mp3"])
    for g, v in (("f", "en-IN-NeerjaNeural"), ("m", "en-IN-PrabhatNeural")):
        run(["edge-tts", "--voice", v, "--rate=-4%", "--text", T, "--write-media", f"tmp_e{g}.mp3"])
        run(["ffmpeg", "-v", "error", "-y", "-i", f"tmp_e{g}.mp3", "-af", POLISH, "-b:a", "128k", f"voicelab2/edge/E1_{g}_enIN_{v.split('-')[2]}.mp3"])
elif mode == "kokoro":
    os.makedirs("voicelab2/kokoro", exist_ok=True)
    import soundfile as sf, numpy as np
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="h")
    for v in ("hf_alpha", "hf_beta", "hm_omega", "hm_psi"):
        try:
            aud = np.concatenate([a for _, _, a in pipe(T, voice=v, speed=0.95)])
            sf.write(f"tmp_k_{v}.wav", aud, 24000)
            run(["ffmpeg", "-v", "error", "-y", "-i", f"tmp_k_{v}.wav", "-af", POLISH, "-b:a", "128k", f"voicelab2/kokoro/K_{v}.mp3"])
        except Exception as e: print("kokoro fail", v, e)
elif mode == "parler":
    os.makedirs("voicelab2/parler", exist_ok=True)
    import torch, soundfile as sf
    from parler_tts import ParlerTTSForConditionalGeneration
    from transformers import AutoTokenizer
    m = ParlerTTSForConditionalGeneration.from_pretrained("ai4bharat/indic-parler-tts")
    tok = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts"); dtok = AutoTokenizer.from_pretrained(m.config.text_encoder._name_or_path)
    descs = {"Rohit_m": "Rohit speaks in a warm, friendly, expressive voice at a moderate pace, very clear audio, no background noise.",
             "Aman_m": "Aman speaks in a confident, energetic voice at a moderate pace, very clear audio, no background noise.",
             "Divya_f": "Divya speaks in a warm, friendly, expressive voice at a moderate pace, very clear audio, no background noise.",
             "Rani_f": "Rani speaks in a cheerful, clear voice at a moderate pace, very clear audio, no background noise."}
    for k, d in descs.items():
        try:
            di = dtok(d, return_tensors="pt"); pi = tok(T, return_tensors="pt")
            g = m.generate(input_ids=di.input_ids, attention_mask=di.attention_mask, prompt_input_ids=pi.input_ids, prompt_attention_mask=pi.attention_mask)
            sf.write(f"tmp_p_{k}.wav", g.cpu().numpy().squeeze(), m.config.sampling_rate)
            run(["ffmpeg", "-v", "error", "-y", "-i", f"tmp_p_{k}.wav", "-af", POLISH, "-b:a", "128k", f"voicelab2/parler/P_{k}.mp3"])
        except Exception as e: print("parler fail", k, e)
elif mode == "asr":
    from faster_whisper import WhisperModel
    wm = WhisperModel("small", device="cpu", compute_type="int8")
    norm = lambda s: re.sub(r"[^ऀ-ॿa-z0-9 ]", "", s.lower().replace("।", " ").replace("़", "")).split()
    ref = norm(T); rows = []
    files = sorted(glob.glob("voicelab2/**/*.mp3", recursive=True) + glob.glob("voicelab/*.mp3"))
    for f in files:
        try:
            segs, info = wm.transcribe(f, language="hi", beam_size=5); txt = " ".join(s.text for s in segs)
            r = difflib.SequenceMatcher(None, ref, norm(txt)).ratio()
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout or 0)
            rows.append((r, f, dur, txt))
        except Exception as e: rows.append((0, f, 0, f"ERR {e}"))
    with open("voicelab2/asr.txt", "w", encoding="utf-8") as o:
        o.write("score  seconds  file\n")
        for r, f, d, t in sorted(rows, reverse=True): o.write(f"{r:.2f}  {d:5.1f}  {f}\n      ASR: {t}\n")
    print(open("voicelab2/asr.txt", encoding="utf-8").read())
