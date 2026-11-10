"""Builds hook-first (v2) reel specs into reels.json  (style 'viral' + card shots + DM pill).  python gen_v2.py"""
import json, re
P = dict(
 PHONE="scrolling-on-his-phone|girl-lying-down-chatting-on-her-cell-phone", NPHONE="girl-using-her-cell-phone-at-night",
 WAKE="waking-up-and-drinking-coffee|male-office-worker-yawning", COFFEE="morning-coffee|coffee-and-music-in-the-morning",
 TEA="drinking-tea-on-a-cool-morning", STRETCH="woman-stretching-in-the-morning|silhouette-of-woman-stretching|a-young-man-stretches-his-arms",
 SUNRISE="sunrise|man-walks-on-the-rooftop-with-sunrise", WALKSUN="backlit-woman-walking-at-sunset|family-walking-together-in-nature|nature-walk-as-a-couple",
 WATER="woman-drinks-water-from-her-glass|woman-drinks-from-water-bottle|silhouette-of-man-drinking-water",
 HERBS="woman-cutting-herbs-in-the-kitchen|farmers-market-display-of-fresh-herbs|chopping-up-herbs|adding-herbs-to-a-bowl",
 HONEY="honey-dipper", SPICES="different-spices-with-tags|pepper-mix-spices|oriental-spices",
 MILK="milk-being-poured|continuous-stream-of-pristine-white-milk", YOGA="woman-doing-yoga-on-a-deck|woman-meditating-in-nature|woman-doing-yoga-in-a-park",
 OLDYOGA="older-woman-doing-yoga", RUN="woman-out-for-a-run|man-and-woman-jogging|runner-training-in-a-park",
 SMILE="a-well-groomed-woman-while-laughing|mature-black-woman-smiling|a-girls-face-in-detail-while-smiling", FRIENDS="friends-running-in-the-countryside|friends",
 SLEEP="girl-asleep-on-a-sofa", NIGHT="dark-starry-night|full-moon", FRUIT="a-woman-choosing-fruit|blending-a-fruit-smoothie|fresh-sliced-fruit",
 VEG="fresh-vegetables-on-a-wooden-board|chef-preparing-salad", GYM="people-running-on-treadmills|woman-doing-warm-up-exercises|bodybuilder",
 STAIRS="a-businesswoman-going-upstairs-in-a-hurry", FOOD="pasta-with-cheese-and-herbs|chef-cooking-stir-fry", OFFICE="male-office-worker-yawning|man-walking-into-office-building",
)
def sh(*a):  # "PHONE" -> clip, "@card" -> card
    return [({"card": x[1:]} if x.startswith("@") else {"clip": P[x].split("|")}) for x in a]
CTA_SMALL = "Yeh ek wellness product hai. Results alag-alag ho sakte hain."
def sc(who, say, txt, shots, **k): return dict(v=who, say=say, txt=txt, shots=sh(*shots), **k)
def cta(who, say, txt, shots, big=("FREE 7-DIN CHART", "*CHART LIKHO")):
    return sc(who, say, txt, shots, big=list(big), big_y=330, big_size=100, dm="DM NOW  •  CHART", small=CTA_SMALL)
def reel(name, who, scenes):
    return dict(name=name, scenes=scenes, style="viral", rate="+8%", music=[148, 614, 871], end_card="end_beautilook",
                end_say="फील गुड, लुक गुड, लिव बेटर!", end_cap="Feel Good, Look Good, Live Better!", end_pad=1.0)
def hook(who, say, txt, shots, big): return sc(who, say, txt, shots, big=big, big_y=260, big_size=108)
def card(who, say, txt, shots): return sc(who, say, txt, shots, cap_y=1390)

R = []
w = "f"
R.append(reel("g01_subah3", w, [
 hook(w, "सुबह उठते ही ये तीन गलतियाँ मत करना!", "Subah uthte hi ye *3 *galtiyan mat karna!", ["PHONE", "WAKE"], ["SUBAH UTHTE HI", "*3 GALTIYAN!"]),
 sc(w, "गलती एक: आँख खुलते ही फ़ोन।", "Galti *1: aankh khulte hi *phone.", ["NPHONE", "PHONE"]),
 sc(w, "गलती दो: बिना पानी पिए सीधे चाय।", "Galti *2: bina paani *seedhi chai.", ["COFFEE", "TEA"]),
 sc(w, "गलती तीन: धूप और सैर छोड़ देना।", "Galti *3: *dhoop aur *walk skip.", ["SUNRISE", "STRETCH"]),
 card(w, "इसकी जगह: गुनगुना पानी, तुलसी की बूँदें, और दस मिनट की धूप।", "Iski jagah: *gunguna paani, *tulsi drop, *10 min dhoop.", ["@imm_tulsi", "WATER"]),
 cta(w, "फ्री सात दिन का चार्ट चाहिए? बस चार्ट लिखिए!", "Free *7 din ka chart? Bas *CHART likho!", ["SMILE", "WALKSUN"])]))
w = "m"
R.append(reel("g02_nani3", w, [
 hook(w, "दादी-नानी के ये तीन नुस्खे आज भी काम आते हैं!", "Dadi-Nani ke *3 nuskhe, aaj bhi *kaam ke!", ["HERBS", "SPICES"], ["NANI KE", "*3 NUSKHE!"]),
 sc(w, "एक: रात को गरम दूध में हल्दी।", "*1: raat ko garam doodh mein *haldi.", ["MILK", "HONEY"]),
 sc(w, "दो: सर्दी में तुलसी-अदरक की चाय।", "*2: sardi mein *tulsi-adrak ki chai.", ["TEA", "HERBS"]),
 sc(w, "तीन: रोज़ थोड़ी धूप और सैर।", "*3: roz thodi *dhoop aur *sair.", ["WALKSUN", "SUNRISE"]),
 card(w, "वही हल्दी, अब नैनो रूप में, बेहतर अवशोषण के लिए।", "Wahi *haldi, ab *nano roop mein, *better absorption ke liye.", ["@imm_nano", "SPICES"]),
 cta(w, "घर के बड़ों को भेजिए, और फ्री चार्ट के लिए चार्ट लिखिए!", "Ghar ke *bado ko bhejo, free chart ke liye *CHART likho!", ["FRIENDS", "SMILE"])]))
w = "f"
R.append(reel("g03_slump", w, [
 hook(w, "दोपहर तीन बजे थकान? ये ट्राई करो!", "Dopahar *3 baje *thakaan? Ye try karo!", ["OFFICE", "STAIRS"], ["DOPAHAR 3 BAJE", "*THAKAAN?"]),
 sc(w, "एक: हर घंटे दो मिनट स्ट्रेच।", "*1: har ghante *2 minute *stretch.", ["STRETCH", "YOGA"]),
 sc(w, "दो: पानी पीते रहिए, सिर्फ़ चाय-कॉफ़ी नहीं।", "*2: *paani piyo, sirf chai-coffee nahi.", ["WATER", "COFFEE"]),
 card(w, "तीन: रोज़ का पोषण, पच्चीस से ज़्यादा विटामिन-मिनरल का सपोर्ट।", "*3: roz ka *poshan, *25+ vitamin-mineral ka support.", ["@imm_alkomax", "FRUIT"]),
 cta(w, "उस दोस्त को भेजिए जो हमेशा थका रहता है। चार्ट लिखिए!", "Us dost ko bhejo jo *hamesha thaka rehta hai. *CHART likho!", ["FRIENDS", "RUN"])]))
w = "m"
R.append(reel("g04_neend3", w, [
 hook(w, "रात को नींद नहीं आती? ये तीन गलतियाँ चेक करो!", "Raat ko *neend nahi aati? Ye *3 galtiyan check karo!", ["NPHONE", "NIGHT"], ["NEEND NAHI AATI?", "*YE 3 GALTI CHECK KARO"]),
 sc(w, "एक: सोने से पहले मोबाइल।", "*1: sone se pehle *mobile.", ["PHONE", "NPHONE"]),
 sc(w, "दो: देर रात भारी खाना।", "*2: *der raat *bhaari khana.", ["FOOD", "VEG"]),
 sc(w, "तीन: रोज़ अलग समय पर सोना।", "*3: roz *alag time par sona.", ["SLEEP", "NIGHT"]),
 card(w, "आराम के लिए अश्वगंधा, एक पुरानी आयुर्वेदिक जड़ी-बूटी।", "Aaram ke liye *Ashwagandha, ek *puraani Ayurvedic jadi-booti.", ["@weak_ashwa", "YOGA"]),
 cta(w, "फ्री चार्ट के लिए, चार्ट लिखिए!", "Free chart ke liye, *CHART likho!", ["YOGA", "SMILE"])]))
w = "f"
R.append(reel("g05_sardi5", w, [
 hook(w, "सर्दी में ये पाँच चीज़ें घर में ज़रूर रखिए!", "Sardi mein ye *5 cheezein ghar mein *zaroor rakho!", ["HERBS", "SPICES"], ["SARDI MEIN", "*YE 5 CHEEZEIN"]),
 sc(w, "एक: तुलसी और अदरक।", "*1: *tulsi aur *adrak.", ["HERBS", "TEA"]),
 sc(w, "दो: हल्दी और शहद।", "*2: *haldi aur *shahad.", ["HONEY", "SPICES"]),
 card(w, "पाँचवीं: हिमालयन सी बकथॉर्न, रोज़ की इम्यूनिटी रूटीन के लिए।", "*5: *Himalayan sea buckthorn, roz ki *immunity routine ke liye.", ["@imm_sea", "FRUIT"]),
 cta(w, "बाकी दो जानने के लिए, चार्ट लिखिए!", "Baaki *2 jaanne ke liye, *CHART likho!", ["SMILE", "FRIENDS"])]))
w = "m"
R.append(reel("g06_tees", w, [
 hook(w, "तीस के बाद शरीर ये तीन संकेत देता है!", "*30 ke baad body deti hai ye *3 signals!", ["OFFICE", "STAIRS"], ["30 KE BAAD", "*3 SIGNALS"]),
 sc(w, "एक: जल्दी थक जाना।", "*1: *jaldi thak jaana.", ["STAIRS", "RUN"]),
 sc(w, "दो: खाने में पोषण की कमी।", "*2: khane mein *poshan ki kami.", ["VEG", "FRUIT"]),
 sc(w, "तीन: नींद और एनर्जी का बिगड़ता रूटीन।", "*3: *neend aur *energy ka bigadta routine.", ["NPHONE", "SLEEP"]),
 card(w, "बी-बारह और ओमेगा जैसे पोषक तत्वों का सपोर्ट।", "*B12 aur *Omega jaise poshak tatvon ka support.", ["@nut_b12", "@nut_omega"]),
 cta(w, "अपना चार्ट चाहिए? चार्ट लिखिए!", "Apna chart chahiye? *CHART likho!", ["SMILE", "RUN"])]))
w = "f"
R.append(reel("g07_dhoop", w, [
 hook(w, "रोज़ दस मिनट की धूप, हड्डियों के लिए क्यों ज़रूरी?", "Roz *10 minute *dhoop, *haddiyon ke liye kyun zaroori?", ["SUNRISE", "WALKSUN"], ["ROZ 10 MINUTE", "*DHOOP KYUN?"]),
 sc(w, "धूप से हमारा शरीर विटामिन डी बनाता है।", "Dhoop se body *Vitamin D banati hai.", ["SUNRISE", "WALKSUN"]),
 sc(w, "कैल्शियम के साथ ये हड्डियों को सपोर्ट करता है।", "*Calcium ke saath ye *haddiyon ko support karta hai.", ["STRETCH", "OLDYOGA"]),
 card(w, "रोज़ की रूटीन में कैल्शियम और विटामिन डी तीन।", "Roz ki routine mein *Calcium aur *Vitamin D3.", ["@bone_calcium", "@bone_d3"]),
 cta(w, "घर के बड़ों को भेजिए, और चार्ट लिखिए!", "Ghar ke *bado ko bhejo, aur *CHART likho!", ["FRIENDS", "SMILE"])]))
w = "m"
R.append(reel("g08_protein", w, [
 hook(w, "प्रोटीन सिर्फ़ जिम वालों के लिए नहीं है!", "Protein sirf *gym walon ke liye *nahi hai!", ["GYM", "RUN"], ["PROTEIN SIRF", "*GYM WALON KE LIYE?"]),
 sc(w, "दाल, पनीर, दूध, ये देसी सोर्स हैं।", "*Dal, paneer, doodh: ye *desi sources hain.", ["MILK", "VEG"]),
 sc(w, "पर रोज़ की ज़रूरत पूरी करना कभी मुश्किल होता है।", "Par roz ki zaroorat *poori karna *kabhi mushkil.", ["FOOD", "OFFICE"]),
 card(w, "प्रोटीन पाउडर और स्पिरुलिना जैसे सप्लीमेंट मदद कर सकते हैं।", "*Protein powder aur *Spirulina jaise supplements *madad kar sakte hain.", ["@nut_protein", "@nut_spirulina"]),
 cta(w, "अपना चार्ट चाहिए? चार्ट लिखिए!", "Apna chart chahiye? *CHART likho!", ["GYM", "SMILE"])]))

exec(open("gen_v2_b2.py").read())
exec(open("gen_v2_b3.py").read())
# validate clip patterns against scout lists
names = [l.split("\t")[1] for f in ("scout.txt", "scout2.txt") for l in open(f).read().splitlines() if "\t" in l and not l.startswith("#")]
bad = [(k, p) for k, v in P.items() for p in v.split("|") if not any(re.search(p, n) for n in names)]
print("UNMATCHED PATTERNS:", bad)
old = json.load(open("reels.json")); keep = [r for r in old if r["name"] not in {x["name"] for x in R}]
json.dump(keep + R, open("reels.json", "w"), ensure_ascii=False, indent=1)
print("reels.json:", len(keep + R), "new:", [x["name"] for x in R])
