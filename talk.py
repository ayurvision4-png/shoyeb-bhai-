"""Talking / moving AI stills.  render(spec, wav, secs, out, fps, W, H)
spec: {"img": "anime/a1.jpg", "face": 0|1|None, "cam": [[t_frac, zoom, fx, fy], ...], "seed": 1}
 - mouth opens with the voice envelope (landmark-driven warp + dark mouth interior), eyes blink, head sways and nods,
   camera snaps between keyframes. Landmarks come from anime/landmarks.json (tools/landmarks.py, MediaPipe, run on Actions)."""
import json, math, os, subprocess, wave
import cv2, numpy as np

_LM = {}
def landmarks(path):
    if not _LM:
        _LM.update(json.load(open(os.path.join(os.path.dirname(path) or ".", "landmarks.json"))))
    return _LM.get(os.path.basename(path), [])

def envelope(wav, fps, n):
    try:
        w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
    except Exception:
        return [0.0] * n
    hop = max(1, sr // fps)
    r = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(max(1, len(x) // hop))])
    p = np.percentile(r, 92) + 1e-9; e = np.clip(r / p, 0, 1); e[e < .12] = 0
    out, c = [], 0.0
    for v in e:
        c = v if v > c else c * .55 + v * .45; out.append(float(c))
    return (out + [0.0] * n)[:n]

L_EYE = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
R_EYE = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
L_UP, L_LO = [33, 246, 161, 160, 159, 158, 157, 173, 133], [133, 155, 154, 153, 145, 144, 163, 7, 33]
R_UP, R_LO = [362, 398, 384, 385, 386, 387, 388, 466, 263], [263, 249, 390, 373, 374, 380, 381, 382, 362]

def smooth(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)

def render(spec, wav, secs, out, fps, W, H):
    im = cv2.imread(spec["img"]); oh, ow = im.shape[:2]
    ch = int(oh * 0.955); im = im[:ch]                              # drop generator corner mark
    ZM = 1.5; S = max(W / ow, H / ch) * ZM
    big = cv2.resize(im, (int(ow * S) + 1, int(ch * S) + 1), interpolation=cv2.INTER_LANCZOS4)
    bh, bw = big.shape[:2]; base = big.copy(); work = big.copy()
    fi = spec.get("face"); face = None
    if fi is not None:
        fl = sorted(landmarks(spec["img"]), key=lambda f: -(max(p[0] for p in f) - min(p[0] for p in f)))       # biggest face first
        if len(fl) > fi: face = np.array([[p[0] * ow * S, p[1] * oh * S] for p in fl[fi]])
    n = int(round(secs * fps)); env = envelope(wav, fps, n + 8)
    cam = spec.get("cam") or ([[0, 1.0, 0.36]] if face is not None else [[0, 1.0, 0.5, 0.4]])
    fc = face.mean(axis=0) if face is not None else None
    rng = np.random.RandomState(spec.get("seed", 1)); blinks, t = [], 0.9 + rng.rand()
    while t < secs: blinks.append(t); t += 2.4 + rng.rand() * 1.8
    if face is not None:
        mw = float(np.hypot(*(face[291] - face[61])))
        eh = [float(np.hypot(*(face[a] - face[b]))) for a, b in ((159, 145), (386, 374))]
        eyes_open = min(eh) > 0.045 * mw
        def lid_skin(EY):
            ec = face[EY].mean(axis=0); ew = float(np.hypot(*(face[EY[0]] - face[EY[8]]))); y = int(face[EY][:, 1].max() + 0.5 * ew); x = int(ec[0])
            return np.median(base[y - 4:y + 5, x - 4:x + 5].reshape(-1, 3), axis=0) * 0.84
        skin = [lid_skin(L_EYE), lid_skin(R_EYE)]
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                          "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(n):
        tt = f / fps; a = env[f]; a = min(1.0, a ** 0.8) * (0.88 + 0.12 * math.sin(2 * math.pi * 6.5 * tt))
        if face is not None:
            # ---- mouth
            mc = (face[13] + face[14]) / 2; ym = float(mc[1]); xm = float(mc[0])
            x0, x1, y0, y1 = int(xm - 1.5 * mw), int(xm + 1.5 * mw), int(ym - 1.1 * mw), int(ym + 1.9 * mw)
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, bw), min(y1, bh)
            roi = base[y0:y1, x0:x1]; gx, gy = np.meshgrid(np.arange(x0, x1, dtype=np.float32), np.arange(y0, y1, dtype=np.float32))
            s = a * 0.55 * mw; sg = 0.45 * mw
            wx = np.exp(-(((gx - xm) / sg) ** 2))
            wl = np.where(gy >= ym, np.exp(-(((gy - ym) / (0.95 * mw)) ** 2)), 0.0)
            wu = np.where(gy < ym, np.exp(-(((ym - gy) / (0.30 * mw)) ** 2)), 0.0)
            dy = (s * wl - 0.16 * s * wu) * wx
            warped = cv2.remap(roi, gx - x0, (gy - dy) - y0, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            if s > 0.8:
                top = ym - 0.16 * s * wx; bot = ym + s * wx                                          # gap between the lips, column by column
                m = np.clip((gy - top) / 1.0 + 0.5, 0, 1) * np.clip((bot - gy) / 1.0 + 0.5, 0, 1) * (wx > 0.12)
                m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), max(0.7, 0.012 * mw))[..., None]
                yy = ((gy - top) / np.maximum(bot - top, 1.0))[..., None]; xx = np.abs(gx - xm)[..., None] / mw
                col = np.zeros(warped.shape, np.float32); col[:] = (32, 22, 62)                      # dark mouth interior (BGR)
                tg = np.clip((0.24 - yy) / 0.08, 0, 1) * np.clip((0.27 - xx) / 0.08, 0, 1)           # upper teeth
                tn = np.clip((yy - 0.55) / 0.2, 0, 1) * np.clip((0.26 - xx) / 0.08, 0, 1)            # tongue
                col = col * (1 - tg) + np.array([196, 208, 222], np.float32) * tg
                col = col * (1 - 0.6 * tn) + np.array([85, 95, 205], np.float32) * 0.6 * tn
                warped = (warped.astype(np.float32) * (1 - m) + col * m).astype(np.uint8)
            work[y0:y1, x0:x1] = warped
            # ---- blink
            bl = 0.0
            for b0 in blinks:
                u = tt - b0
                if 0 <= u < 0.17: bl = max(bl, u / 0.07 if u < 0.07 else 1 - (u - 0.07) / 0.10)
            work_eyes = eyes_open
            for (EY, UP, LO, sk) in ((L_EYE, L_UP, L_LO, skin[0]), (R_EYE, R_UP, R_LO, skin[1])):
                ex0, ex1 = int(min(face[i][0] for i in EY)) - 6, int(max(face[i][0] for i in EY)) + 6
                ey0, ey1 = int(min(face[i][1] for i in EY)) - 10, int(max(face[i][1] for i in EY)) + 6
                work[ey0:ey1, ex0:ex1] = base[ey0:ey1, ex0:ex1]
                if bl > 0.02 and work_eyes:
                    up = face[UP]
                    ys_lo = np.interp(up[:, 0], *zip(*sorted((face[i][0], face[i][1]) for i in LO)))
                    upn = up.copy(); upn[:, 1] = up[:, 1] + bl * (ys_lo - up[:, 1])
                    poly = np.vstack([up + np.array([0, -2.0]), upn[::-1] + np.array([0, 1.0])]).astype(np.int32)
                    mk = np.zeros((ey1 - ey0, ex1 - ex0), np.float32); cv2.fillPoly(mk, [poly - np.array([ex0, ey0])], 1.0, cv2.LINE_AA)
                    mk = cv2.GaussianBlur(mk, (0, 0), 2.0)[..., None]
                    patch = work[ey0:ey1, ex0:ex1].astype(np.float32)
                    patch = patch * (1 - mk) + np.array(sk, np.float32) * mk
                    cv2.polylines(patch, [(upn - np.array([ex0, ey0])).astype(np.int32)], False, (25, 25, 40), max(1, int(0.03 * mw)), cv2.LINE_AA)
                    work[ey0:ey1, ex0:ex1] = np.clip(patch, 0, 255).astype(np.uint8)
        # ---- camera: keyframes with quick snap, sway, nod
        tf = tt / secs; v = np.array((list(cam[0]) + [0, 0])[1:4], float)
        for kf in cam[1:]:
            u = smooth((tf - kf[0]) * secs / 0.14)
            if u > 0: v = v + (np.array((list(kf) + [0, 0])[1:4], float) - v) * u
        z = v[0] * (1.05 + 0.04 * tf + 0.006 * math.sin(2 * math.pi * 0.25 * tt)); k = z / ZM; hx, hy = W / (2 * k), H / (2 * k)
        if fc is not None: cx, cy = fc[0], fc[1] - (v[1] - 0.5) * H / k          # face lands at screen height v[1]
        else: cx, cy = v[1] * bw, v[2] * bh
        cx = min(max(cx, hx), bw - hx); cy = min(max(cy, hy), bh - hy)
        M = cv2.getRotationMatrix2D((cx, cy), 0.6 * math.sin(2 * math.pi * 0.33 * tt), k)
        M[0, 2] += W / 2 - cx + 5 * math.sin(2 * math.pi * 0.21 * tt); M[1, 2] += H / 2 - cy - 4 * a
        p.stdin.write(cv2.warpAffine(work, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).tobytes())
    p.stdin.close(); p.wait()
