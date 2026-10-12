import os, glob
from rembg import remove
from PIL import Image
os.makedirs("cutouts", exist_ok=True)
for f in ["handwash","toothpaste","sanitarypad","noni_drink","sea_buckthorn","red_aloevera","livofit","berry_drink","biotin_gummy","boswellia","calcium_chewable","nano_curcumin","spirulina","detox_tablet","deep_sleep_gummy","multivitamin_gummy","shilajit_gummy"]:
    p=f+".png"
    if os.path.exists(p): remove(Image.open(p).convert("RGB")).save("cutouts/"+f+".png")
