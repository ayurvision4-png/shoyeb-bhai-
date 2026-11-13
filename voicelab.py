"""Voice lab: same script, several TTS variants (A current, B tuned+polished, C Piper Indian voices) -> voicelab/*.mp3"""
import subprocess, os, sys
os.makedirs("voicelab", exist_ok=True)
A = "सच या झूठ? घी खाने से वज़न बढ़ता है? जवाब: मात्रा का खेल है। दाल-सब्ज़ी के साथ थोड़ा सा घी, और रोज़ की सैर। रोज़ एक देसी आदत के लिए फ़ॉलो करिए, और फ्री चार्ट के लिए चार्ट लिखिए!"
B = "सच या झूठ... घी खाने से, वज़न बढ़ता है? ... जवाब है, मात्रा का खेल। ... दाल, सब्ज़ी के साथ, थोड़ा सा घी, और रोज़ की सैर। ... रोज़ एक देसी आदत के लिए, फ़ॉलो कीजिए। और फ्री चार्ट के लिए, कमेंट में, चार्ट लिखिए।"
POLISH = ("highpass=f=85,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.1:g=2.5,"
          "acompressor=threshold=-21dB:ratio=3:attack=6:release=90,aecho=0.85:0.9:22:0.10,loudnorm=I=-16:TP=-1.5:LRA=7")
def run(cmd, **k):
    print(">>", " ".join(cmd) if isinstance(cmd, list) else cmd); return subprocess.run(cmd, **k)
for g, voice in (("m", "hi-IN-MadhurNeural"), ("f", "hi-IN-SwaraNeural")):
    run(["edge-tts", "--voice", voice, "--rate=+8%", "--text", A, "--write-media", f"voicelab/A_{g}_current.mp3"])
    pitch = "--pitch=-4Hz" if g == "m" else "--pitch=+0Hz"
    run(["edge-tts", "--voice", voice, "--rate=-2%", pitch, "--text", B, "--write-media", f"tmp_B_{g}.mp3"])
    run(["ffmpeg", "-v", "error", "-y", "-i", f"tmp_B_{g}.mp3", "-af", POLISH, "-b:a", "128k", f"voicelab/B_{g}_tuned.mp3"])
base = "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN"
for g, name in (("m", "pratham"), ("f", "priyamvada")):
    onnx = f"piper_{name}.onnx"
    r1 = run(["curl", "-sSL", "-f", "-o", onnx, f"{base}/{name}/medium/hi_IN-{name}-medium.onnx"])
    r2 = run(["curl", "-sSL", "-f", "-o", onnx + ".json", f"{base}/{name}/medium/hi_IN-{name}-medium.onnx.json"])
    if r1.returncode or r2.returncode: print("piper voice missing:", name); continue
    p = run(["piper", "--model", onnx, "--output_file", f"tmp_C_{g}.wav"], input=B.encode())
    if p.returncode == 0:
        run(["ffmpeg", "-v", "error", "-y", "-i", f"tmp_C_{g}.wav", "-af", POLISH, "-b:a", "128k", f"voicelab/C_{g}_piper.mp3"])
