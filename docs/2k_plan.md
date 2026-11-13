# Free Reel Factory + 2K Followers Plan (goal: 2,000 IG followers by Dec 10, 2026)

Start: ~223 followers on Nov 10. Needs ~+1,780 in 30 days (~60/day). Ambitious: we maximise odds, no guarantee. Check progress every Monday; if the pace is under 25/day by Nov 24, double down on what worked (see "Weekly review").

## 1. Free reel factory (zero Claude tokens, zero credits)
- Repo: github.com/ayurvision4-png/shoyeb-bhai- . Workflow `make-reels` (GitHub Actions, free) renders reels on every push that touches `reel_request.txt`, `reels.json` or `make_reel.py`.
- Engine: `viral.py` (style "viral") = Mixkit stock b-roll + edge-tts Hindi voices (male hi-IN-MadhurNeural / female hi-IN-SwaraNeural) + ffmpeg. Output: `reels2/<name>.mp4`, public raw URL `https://raw.githubusercontent.com/ayurvision4-png/shoyeb-bhai-/main/reels2/<name>.mp4` (Metricool can schedule directly from it).
- Recipe v2 (hook-first): hook text in the top third from frame 0, voice starts at 0 s, cut every 1.5-2.5 s, product card (cards/*.jpg) from ~second 8, yellow "DM NOW - CHART" pill + disclaimer on the CTA scene, Beautilook end card with "Feel Good, Look Good, Live Better!", centred "WhatsApp 7596985205" watermark all through, progress bar, whoosh SFX, music under voice. No prices.
- To make new reels: add a `reel(...)` block in `gen_v2.py` (Hindi `say` for the voice, Hinglish `txt` for captions, `*word` = yellow highlight, shots = b-roll tags or `@card_name`), run `python gen_v2.py`, put the names in `reel_request.txt`, push. ~10 min later the mp4 appears in `reels2/`.
- Voices alternate male/female per reel. Style/hook type changes every day.

## 2. What makes a reel travel (2026 sources: TrueFutureMedia, Socialchamp, Later, eClincher)
- Ranking signals: watch time first, then DM shares (sends) and saves; likes/comments are weaker. So every reel ends with a send trigger ("us dost ko bhejo...") and a save trigger.
- Hook in the first 1.7-3 s; on-screen text for sound-off viewers; 15-25 s reels with a complete loop.
- Hashtags: only 3-5 very relevant ones (categorisation, not discovery). Keyword-rich first line of the caption (first 125 characters show before "more"): "Morning routine", "Ayurveda", "health tips Hindi", "immunity".
- Caption: short (under ~40 words), one action (save / send / comment CHART).
- Reels reach non-followers; carousels convert existing followers (40-60% mix suggested) - we keep the existing carousel days and add reels.
- Trial Reels show the reel only to non-followers first; sources say they cannot always be scheduled by third-party tools, so post manually from the app when possible (3-5 per week).
- Post 1-2 reels a day at 08:00 / 13:00 / 19:30-21:00 IST.

## 3. Hook formulas (rotate; each must be TRUE to the content)
1. Mistake list: "Subah uthte hi ye 3 galtiyan mat karna"
2. Nostalgia: "Dadi-Nani ke 3 nuskhe, aaj bhi kaam ke"
3. Relatable time-stamp: "Dopahar 3 baje thakaan? Ye try karo"
4. Age/stage: "30 ke baad body deti hai ye 3 signals"
5. Myth-bust: "Protein sirf gym walon ke liye nahi hai"
6. Number list: "Sardi mein ye 5 cheezein ghar mein zaroor rakho"
7. Why-question: "Roz 10 minute dhoop, haddiyon ke liye kyun zaroori?"
8. Series: "7 Din 7 Aadatein - Day N" (builds return viewers; Nov 11 audit: series got views but no follows, use sparingly)
9. Quiz (best performer in the Nov 11 audit): "Sach ya Jhooth? <myth>" -> "Comment karo SACH ya JHOOTH" -> answer -> one desi tip -> Follow + CHART CTA. Built in gen_v2_b3.py (s01-s06). Pattern: hook text top third + "COMMENT KARO" beat at ~5 s + answer beat; first comment repeats the question.
Rules: soft "supports" wording, no disease names or cure claims in public reels, no prices, disclaimer on the CTA scene.

## 4. Caption template
`<Hook line with keyword> + emoji` / `Save + send trigger to a specific person` / `Comment CHART or DM Now for the free 7-din routine chart` / `WhatsApp 7596985205` / disclaimer / 5 hashtags. First comment = a one-tap question (e.g. "Aap kaunsi galti karte ho? 1, 2 ya 3 likho").

## 5. Daily 15-minute routine for Shoaib (the part only a human can do)
1. After each reel goes live: reply to every comment within 10 min (the first hour matters most) and send the reel link to 10-20 WhatsApp contacts/customers (sends = reach). Post it on WhatsApp Status too.
2. Add the reel to your Instagram Story ("Add to story") and use a poll sticker ("Haan / Nahi").
3. Leave 10 genuine comments on 10 Ayurveda/wellness reels in Hindi (not links) - this brings profile visits.
4. Pin the 3 best reels; keep bio: "Ayurveda + wellness routines | Free 7-din chart: DM CHART | WhatsApp 7596985205" (remove medical claims / FDA / 100%).
5. Optional: set up ManyChat free plan for comment-to-DM automation on keyword CHART.

## 5b. Nov 11 audit additions
Full audit and manual list: ig-audit-nov11.md. Key points: seed every reel in the first hour (WhatsApp contacts + Status), post a Story with a poll daily, fix the foreign-follower mix, prefer myth/quiz and cultural-POV hooks, avoid condition names and dosing lines in public captions, giveaway reel gv01 on hold for Shoaib's approval.

## 6. Weekly review (Monday)
Use Metricool analytics: IGRE28 (3-second view rate) and IGRE24 (average watch time) per reel. Keep the hook types with 3-s rate above ~40% and average watch above ~6 s; drop the rest. Followers: Instagram profile count on Monday vs previous Monday.

## 7. Schedule of v2 reels (Metricool brand 7187460)
See `claude/reel-schedule.md` (updated Nov 10).
