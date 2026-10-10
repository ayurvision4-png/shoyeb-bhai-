FREE VIDEO MAKER (no subscription)
1. Open Google Colab (colab.research.google.com), new notebook.
2. Left sidebar > Files > upload make_videos.py and your 5 product photos (1000153677/679/684/686/688.jpg).
3. In a cell run:  !pip install edge-tts pillow
4. In a cell run:  !python make_videos.py        (one product: !python make_videos.py tulsi_drops)
5. Download the files from the "videos" folder. Post them via Metricool.
Voices: hi-IN-MadhurNeural (male), hi-IN-SwaraNeural (female), both free Microsoft Hindi voices.
Edit the PRODUCTS list in make_videos.py to add more products.
layout_preview_tulsi_silent.mp4 = layout test with no voice (voice needs internet).

pdf2 PERSONAL CARE: also upload one clear photo of each pack, named exactly:
handwash.jpg, intimatewash.jpg, toothpaste.jpg, sanitarypad.jpg
Run only those: !python make_videos.py hand_wash shewell_intimate_wash noni_toothpaste shewell_sanitary_pad
