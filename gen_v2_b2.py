# batch 2 (exec'd from gen_v2.py): follow-CTA reels for Nov 24 - Dec 10
P.update(DESK="waking-up-and-drinking-coffee-in-front-of-a-laptop|woman-doing-yoga-in-her-home-office|male-office-worker-yawning",
         CHILD="a-little-girl-smiles-while-riding-the-carnival|a-little-girl-in-a-dress-walking", SKIN="applying-skincare-products|a-beautiful-smiling-woman-with-curly-hair")
FSAY = "रोज़ एक देसी आदत के लिए फ़ॉलो करिए, और फ्री चार्ट के लिए चार्ट लिखिए!"
FTXT = "Roz ek *desi aadat ke liye *FOLLOW karo, free chart ke liye *CHART likho!"
def fcta(w, shots=("SMILE", "FRIENDS"), big=("FOLLOW KARO", "*+ CHART LIKHO"), say=FSAY, txt=FTXT): return cta(w, say, txt, list(shots), big=big)
w = "f"
R.append(reel("h01_wmyth", w, [
 hook(w, "वज़न कंट्रोल की ये तीन बातें गलत हैं!", "Weight control ki ye *3 baatein *galat hain!", ["GYM", "FOOD"], ["WEIGHT KE BAARE MEIN", "*3 GALAT BAATEIN"]),
 sc(w, "गलत एक: भूखे रहना।", "Galat *1: *bhookha rehna.", ["VEG", "FRUIT"]),
 sc(w, "गलत दो: सिर्फ़ जिम, खाना वैसा ही।", "Galat *2: sirf *gym, khana *waisa hi.", ["RUN", "FOOD"]),
 sc(w, "गलत तीन: रात को बिल्कुल न खाना।", "Galat *3: raat ko *bilkul na khana.", ["NIGHT", "PHONE"]),
 card(w, "सही तरीका: संतुलित खाना, रोज़ सैर, और बब्यूटीलुक का नब्बे दिन का रूटीन।", "Sahi tareeka: *balanced khana, roz *walk, *Beautilook ka *90 din routine.", ["@end_beautilook", "WALKSUN"]),
 fcta(w)]))
w = "m"
R.append(reel("h02_chai", w, [
 hook(w, "चाय नहीं छोड़नी? तो ये तीन स्मार्ट बदलाव करो!", "Chai nahi chhodni? Ye *3 *smart badlav karo!", ["TEA", "COFFEE"], ["CHAI NAHI CHHODNI?", "*3 SMART BADLAV"]),
 sc(w, "एक: चीनी कम।", "*1: *cheeni kam.", ["HONEY", "MILK"]),
 sc(w, "दो: तुलसी और अदरक डालिए।", "*2: *tulsi aur *adrak daaliye.", ["HERBS", "SPICES"]),
 sc(w, "तीन: खाली पेट नहीं, कुछ खाकर पीजिए।", "*3: *khaali pet nahi, kuch *khaakar.", ["FRUIT", "WAKE"]),
 card(w, "ऊपर से, रोज़ की रूटीन में नोनी वेलनेस ड्रिंक।", "Upar se, roz ki routine mein *Noni wellness drink.", ["@weak_noni", "WATER"]),
 fcta(w)]))
w = "f"
R.append(reel("h03_khana", w, [
 hook(w, "खाने के बाद ये तीन काम ज़रूर करो!", "Khane ke baad ye *3 kaam *zaroor karo!", ["FOOD", "VEG"], ["KHANE KE BAAD", "*YE 3 KAAM"]),
 sc(w, "एक: दस मिनट टहलिए।", "*1: *10 minute *tehliye.", ["WALKSUN", "RUN"]),
 sc(w, "दो: गुनगुना पानी पीजिए।", "*2: *gunguna paani.", ["WATER", "TEA"]),
 sc(w, "तीन: तुरंत लेटिए मत।", "*3: *turant *letiye mat.", ["SLEEP", "PHONE"]),
 card(w, "पाचन की रूटीन के लिए त्रिफला का सहारा।", "*Pachan routine ke liye *Trifala ka sahara.", ["@dig_trifala", "HERBS"]),
 fcta(w)]))
w = "m"
R.append(reel("h04_detox", w, [
 hook(w, "वीकेंड डिटॉक्स? पहले ये समझ लो!", "Weekend *detox? Pehle ye *samajh lo!", ["FRUIT", "HERBS"], ["WEEKEND DETOX?", "*PEHLE YE SAMAJH LO"]),
 sc(w, "शरीर का अपना सिस्टम है, बस उसे सही आदतें चाहिए।", "Body ka *apna system hai, bas *sahi aadatein chahiye.", ["YOGA", "RUN"]),
 sc(w, "खूब पानी, फल-सब्ज़ियाँ और अच्छी नींद।", "Khoob *paani, *fal-sabziyan aur achhi *neend.", ["WATER", "VEG", "SLEEP"]),
 card(w, "एलोवेरा जूस जैसी चीज़ें रूटीन में मदद कर सकती हैं।", "*Aloe vera juice jaisi cheezein routine mein *madad kar sakti hain.", ["@dig_aloe", "FRUIT"]),
 fcta(w)]))
w = "f"
R.append(reel("h05_bachpan", w, [
 hook(w, "बचपन की ये तीन आदतें हम भूल गए!", "Bachpan ki ye *3 aadatein hum *bhool gaye!", ["CHILD", "FRIENDS"], ["BACHPAN KI", "*3 AADATEIN"]),
 sc(w, "एक: सुबह की धूप।", "*1: subah ki *dhoop.", ["SUNRISE", "WALKSUN"]),
 sc(w, "दो: घर का बना खाना।", "*2: ghar ka bana *khana.", ["HERBS", "VEG"]),
 sc(w, "तीन: शाम को बाहर खेलना।", "*3: shaam ko *bahar khelna.", ["RUN", "FRIENDS"]),
 card(w, "रोज़ के पोषण के लिए वेज ओमेगा।", "Roz ke *poshan ke liye *Veg Omega.", ["@nut_omega", "FRUIT"]),
 fcta(w)]))
w = "m"
R.append(reel("h06_office", w, [
 hook(w, "ऑफिस में बैठे-बैठे अकड़न? ये तीन स्ट्रेच!", "Office mein baithe-baithe *akdan? Ye *3 stretch!", ["DESK", "OFFICE"], ["OFFICE MEIN AKDAN?", "*YE 3 STRETCH"]),
 sc(w, "एक: गर्दन को धीरे से घुमाइए।", "*1: *gardan ko dheere se ghumaiye.", ["STRETCH", "YOGA"]),
 sc(w, "दो: हर घंटे खड़े होइए।", "*2: har ghante *khade hoiye.", ["STAIRS", "WALKSUN"]),
 sc(w, "तीन: कंधे और कमर को खोलिए।", "*3: *kandhe aur *kamar kholiye.", ["STRETCH", "OLDYOGA"]),
 card(w, "हड्डियों और जोड़ों की रूटीन के लिए ऑर्थो सपोर्ट।", "*Haddi aur *jodon ki routine ke liye *Ortho support.", ["@bone_ortho", "SMILE"]),
 fcta(w)]))
w = "f"
R.append(reel("h07_skin", w, [
 hook(w, "सर्दी में स्किन खिंचती है? ये तीन देसी तरीके!", "Sardi mein *skin khichti hai? Ye *3 desi tareeke!", ["SKIN", "SMILE"], ["SARDI MEIN SKIN?", "*3 DESI TAREEKE"]),
 sc(w, "एक: खूब पानी।", "*1: khoob *paani.", ["WATER", "SKIN"]),
 sc(w, "दो: नहाने के बाद तेल या मॉइस्चराइज़र।", "*2: nahane ke baad *tel ya *moisturiser.", ["HONEY", "SMILE"]),
 sc(w, "तीन: रंग-बिरंगे फल और सब्ज़ियाँ।", "*3: *rang-birange fal aur sabziyan.", ["FRUIT", "VEG"]),
 card(w, "अंदर से केयर के लिए बेरी वेलनेस ड्रिंक।", "*Andar se care ke liye *Berry wellness drink.", ["@weak_berry", "SKIN"]),
 fcta(w)]))
w = "m"
R.append(reel("h08_challenge", w, [
 hook(w, "सात दिन का चैलेंज: क्या आप कर पाओगे?", "*7 din ka *challenge: kya aap kar paoge?", ["RUN", "GYM"], ["7 DIN CHALLENGE", "*KYA AAP KAR PAOGE?"]),
 sc(w, "रोज़ आठ गिलास पानी।", "Roz *8 glass *paani.", ["WATER", "TEA"]),
 sc(w, "रोज़ बीस मिनट की सैर।", "Roz *20 minute *walk.", ["WALKSUN", "SUNRISE"]),
 sc(w, "और रात को फ़ोन से दूरी।", "Aur raat ko *phone se *doori.", ["NPHONE", "SLEEP"]),
 card(w, "पानी की रूटीन के लिए सीएमडी ड्रॉप्स।", "*Paani ki routine ke liye *CMD Drops.", ["@dig_cmd", "WATER"]),
 fcta(w, ["FRIENDS", "SMILE"], ("COMMENT KARO", "*CHALLENGE"), "हिम्मत है तो कमेंट में चैलेंज लिखिए, और फ़ॉलो करिए!", "*Himmat hai to comment mein *CHALLENGE likho, aur *FOLLOW karo!")]))
w = "f"
R.append(reel("h09_dosha", w, [
 hook(w, "आपका बॉडी टाइप क्या है? वात, पित्त या कफ?", "Aapka *body type kya hai? *Vata, *Pitta ya *Kapha?", ["YOGA", "HERBS"], ["VATA, PITTA", "*YA KAPHA?"]),
 sc(w, "वात: पतला शरीर, तेज़ दिमाग़।", "*Vata: patla sharir, *tez dimaag.", ["RUN", "STRETCH"]),
 sc(w, "पित्त: गरम मिज़ाज, तेज़ भूख।", "*Pitta: *garam mizaaj, tez bhookh.", ["FOOD", "SPICES"]),
 sc(w, "कफ: शांत स्वभाव, धीमी चाल।", "*Kapha: *shaant swabhav, dheemi chaal.", ["WALKSUN", "SLEEP"]),
 card(w, "हर टाइप की अलग रूटीन, और अश्वगंधा जैसी जड़ी-बूटियाँ।", "Har type ki *alag routine, aur *Ashwagandha jaisi jadi-bootiyan.", ["@weak_ashwa", "HERBS"]),
 fcta(w, ["SMILE", "FRIENDS"], ("COMMENT MEIN", "*APNA TYPE LIKHO"), "अपना टाइप कमेंट में लिखिए, और फ़ॉलो करिए!", "Apna *type comment mein likho, aur *FOLLOW karo!")]))
w = "m"
R.append(reel("h10_roz1", w, [
 hook(w, "रोज़ एक देसी आदत, सिर्फ़ बीस सेकंड में!", "Roz ek *desi aadat, sirf *20 second mein!", ["SUNRISE", "HERBS"], ["ROZ EK", "*DESI AADAT"]),
 sc(w, "सुबह: गुनगुना पानी।", "*Subah: *gunguna paani.", ["WATER", "WAKE"]),
 sc(w, "दोपहर: खाने के बाद टहलना।", "*Dopahar: khane ke baad *tehalna.", ["WALKSUN", "OFFICE"]),
 sc(w, "रात: सोने से पहले फ़ोन दूर।", "*Raat: sone se pehle *phone door.", ["NPHONE", "SLEEP"]),
 card(w, "रूटीन को आसान बनाइए, तुलसी ड्रॉप के साथ।", "Routine ko *aasan banaiye, *Tulsi Drop ke saath.", ["@imm_tulsi", "HERBS"]),
 fcta(w, ["SMILE", "FRIENDS"], ("FOLLOW KARO", "*ROZ 1 AADAT"))]))
