"""Face landmarks (MediaPipe FaceLandmarker, 478 pts) for every anime/*.jpg -> anime/landmarks.json + debug overlays. Run on Actions."""
import mediapipe as mp, json, glob, os, cv2, urllib.request
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
urllib.request.urlretrieve(URL, "face_landmarker.task")
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpp.BaseOptions(model_asset_path="face_landmarker.task"), num_faces=2,
    min_face_detection_confidence=0.2, min_face_presence_confidence=0.2, min_tracking_confidence=0.2))
os.makedirs("anime/dbg", exist_ok=True)
RES = {}
LIPS = [61,185,40,39,37,0,267,269,270,409,291,375,321,405,314,17,84,181,91,146,78,13,14,308]
EYES = [33,133,159,145,362,263,386,374]
for f in sorted(glob.glob("anime/*.jpg")):
    im = cv2.imread(f); faces = []
    for s in (2, 3, 1):
        big = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_LANCZOS4)
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(big, cv2.COLOR_BGR2RGB)))
        if r.face_landmarks:
            faces = [[[round(p.x, 5), round(p.y, 5)] for p in lm] for lm in r.face_landmarks]; break
    RES[os.path.basename(f)] = faces
    h, w = im.shape[:2]; dbg = im.copy()
    for fc in faces:
        for i in LIPS: cv2.circle(dbg, (int(fc[i][0]*w), int(fc[i][1]*h)), 2, (0,0,255), -1)
        for i in EYES: cv2.circle(dbg, (int(fc[i][0]*w), int(fc[i][1]*h)), 2, (0,255,0), -1)
    cv2.imwrite("anime/dbg/" + os.path.basename(f), dbg); print(f, len(faces), flush=True)
json.dump(RES, open("anime/landmarks.json", "w"))
