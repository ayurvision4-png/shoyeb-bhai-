# batch v3 (exec'd from gen_v2.py after b4): Indian-people footage (Pexels, scout_px.txt) + face-first quiz structure + two-voice dialogue
P.update(
 FX_POINT="IN_man_point_up", FX_SHOCK="IN_man_shock", FX_EARS="IN_man_ears", FX_EXC="IN_man_excited", FX_NAM="IN_man_namaste",
 FX_THINK="IN_man_think", FX_NO="IN_man_no", FX_YES="IN_woman_thumbs", FX_SHRUG="IN_woman_shrug", FX_PRES="IN_woman_present",
 FX_TALK="IN_woman_talk", FX_STARE="IN_man_stare",
 CHAI_IN="IN_chai_kolkata|IN_chai_cup_clay|IN_chai_pour_clay|IN_chai_stove|IN_chai_brass", MILK_IN="IN_milk_man",
 KIT_IN="IN_kitchen_woman|IN_kitchen_woman2|IN_kitchen_stove", SPICE_IN="IN_spices_pour|IN_herb_grind",
 ROTI_IN="IN_roti_stove|IN_dough_tandoor|IN_puri_fry|IN_puri_kadai", MEAL_IN="IN_family_table|IN_thali_close|IN_man_table|IN_boy_eat|IN_curry_dish",
 BREAKFAST_IN="IN_breakfast_puri|IN_puri_fry", STREET_IN="IN_street_samosa|IN_street_vadapav|IN_street_fry",
 PHONE_IN="IN_elder_phone|IN_teen_laptop", WALK_IN="IN_couple_walk_street|IN_couple_walk_hands|IN_woman_walk_lake|IN_elders_bench_sunset",
 ELDER_IN="IN_elder_face|IN_elder_woman_swing|IN_elders_bench_sunset", YOGA_IN="IN_yoga_woman|IN_yoga_woman2|IN_yoga_man_garden|IN_namaste_women|IN_woman_namaste_smile",
 EVE_IN="IN_diya_kitchen", OFFICE_IN="IN_office_woman|IN_office_man_think|IN_teen_laptop")
NEW3 = {f"s{n:02d}_{s}" for n, s in [(3, "khalipet"), (4, "mobile"), (5, "8glass"), (6, "dhoop"), (7, "nimbu"), (8, "naashta"), (9, "raat"), (10, "roti"), (11, "tehelna"), (12, "neend"), (13, "saunf"), (14, "paani_pehle")]}
R[:] = [r for r in R if r["name"] not in NEW3]
FB = 1000    # big text sits on the torso, never on the face (face-first shots)
CY = 1400    # word captions sit below the big text (no overlap)
def qz(name, w1, w2, hq, hb, hook_shots, react, ans_say, ans_txt, ans_big, ans_shot, tip_say, tip_txt, tip_shots, mid=None, think_shot="FX_THINK"):
    qh = sc(w1, hq[0], hq[1], list(hook_shots), big=hb, big_y=FB, big_size=100, cap_y=CY)
    th = sc(w1, "सोचिए... कमेंट में लिखिए, सच या झूठ!", "Socho... comment mein likho *SACH ya *JHOOTH!", [think_shot], big=["COMMENT KARO", "*SACH YA JHOOTH"], big_y=FB, big_size=96, cap_y=CY)
    an = sc(w2, ans_say, ans_txt, [react, ans_shot], big=ans_big, big_y=FB, big_size=100, cap_y=CY)
    tip = card(w2, tip_say, tip_txt, [mid, tip_shots[0]]) if mid else sc(w2, tip_say, tip_txt, list(tip_shots))
    if tip_shots and tip_shots[0].startswith("@") and not mid: tip = card(w2, tip_say, tip_txt, list(tip_shots))
    cta_sc = sc(w1, QS, QT, ["FX_PRES", "MEAL_IN"], big=["FOLLOW KARO", "*ROZ SACH-JHOOTH"], big_y=FB, big_size=100, cap_y=1390, dm="DM NOW  •  CHART", small="Yeh general jaankari hai, dawai nahi.")
    return reel(name, w1, [qh, th, an, tip, cta_sc])
SJ = "*SACH ya *JHOOTH?"
R.append(qz("s03_khalipet", "m", "f", ("सच या झूठ? खाली पेट चाय पीना ठीक है?", SJ + " Khaali pet chai peena theek hai?"), ["SACH YA JHOOTH?", "*KHAALI PET CHAI?"], ("FX_SHOCK", "CHAI_IN"),
 "FX_POINT", "जवाब: बेहतर है पहले पानी, फिर कुछ हल्का खाना।", "Jawab: *behtar hai pehle *paani, phir kuch halka khana.", ["JAWAB:", "*PEHLE PAANI"], "MILK_IN",
 "चाय में तुलसी-अदरक डालिए, और रूटीन में तुलसी ड्रॉप भी।", "Chai mein *tulsi-adrak daaliye, aur routine mein *Tulsi Drop bhi.", ("@imm_tulsi", "SPICE_IN")))
R.append(qz("s04_mobile", "f", "m", ("सच या झूठ? मोबाइल देखते हुए खाना, ज़्यादा खिला देता है?", SJ + " Mobile dekhte hue khana, *zyada khila deta hai?"), ["SACH YA JHOOTH?", "*MOBILE + KHANA"], ("FX_EARS", "PHONE_IN"),
 "FX_YES", "जवाब: सच! ध्यान भटकता है, तो पेट का पता नहीं चलता।", "Jawab: *SACH! Dhyan bhatakta hai, to *pet ka pata nahi chalta.", ["JAWAB:", "*SACH!"], "MEAL_IN",
 "खाते समय सिर्फ़ खाना, और धीरे-धीरे चबाइए।", "Khaate samay *sirf khana, aur *dheere-dheere chabaiye.", ("MEAL_IN", "KIT_IN")))
R.append(qz("s05_8glass", "m", "f", ("सच या झूठ? सबको रोज़ आठ गिलास पानी ज़रूरी है?", SJ + " Sabko roz *8 glass paani zaroori hai?"), ["SACH YA JHOOTH?", "*8 GLASS PAANI"], ("FX_POINT", "MILK_IN"),
 "FX_SHRUG", "जवाब: ज़रूरत सबकी अलग होती है।", "Jawab: *zaroorat *sabki alag hoti hai.", ["JAWAB:", "*SABKI ALAG"], "YOGA_IN",
 "प्यास सुनिए, थोड़ा-थोड़ा पीते रहिए। पानी की रूटीन के लिए सीएमडी ड्रॉप्स।", "*Pyaas sunie, thoda-thoda piyo. Paani ki routine ke liye *CMD Drops.", ("@dig_cmd", "KIT_IN")))
R.append(qz("s06_dhoop", "f", "m", ("सच या झूठ? धूप सिर्फ़ सर्दी में लेनी चाहिए?", SJ + " Dhoop sirf *sardi mein leni chahiye?"), ["SACH YA JHOOTH?", "*DHOOP SIRF SARDI MEIN?"], ("FX_EXC", "ELDER_IN"),
 "FX_NO", "जवाब: झूठ! हर मौसम में थोड़ी धूप अच्छी है।", "Jawab: *JHOOTH! Har mausam mein *thodi dhoop achhi hai.", ["JAWAB:", "*JHOOTH!"], "WALK_IN",
 "सुबह की हल्की धूप, और कैल्शियम के साथ विटामिन डी तीन।", "Subah ki halki *dhoop, aur *Calcium ke saath *Vitamin D3.", ("@bone_d3", "@bone_calcium")))
R.append(qz("s07_nimbu", "f", "m", ("सच या झूठ? सुबह गुनगुना पानी और नींबू, वज़न घटा देता है?", SJ + " Subah *nimbu paani se *weight ghatta hai?"), ["SACH YA JHOOTH?", "*NIMBU PAANI = WEIGHT?"], ("FX_SHOCK", "KIT_IN"),
 "FX_NO", "जवाब: झूठ! कोई चमत्कार नहीं, पर अच्छी आदत ज़रूर है।", "Jawab: *JHOOTH! Koi *chamatkar nahi, par *achhi aadat zaroor hai.", ["JAWAB:", "*JHOOTH!"], "KIT_IN",
 "असली फ़र्क़ आता है सही खाने, रोज़ की सैर और अच्छी नींद से।", "Asli farq: *sahi khana, roz ki *sair, aur achhi *neend se.", ("WALK_IN", "MEAL_IN")))
R.append(qz("s08_naashta", "m", "f", ("सच या झूठ? वज़न घटाना है तो नाश्ता छोड़ देना चाहिए?", SJ + " Weight ke liye *naashta skip karna chahiye?"), ["SACH YA JHOOTH?", "*NAASHTA SKIP?"], ("FX_POINT", "BREAKFAST_IN"),
 "FX_NO", "जवाब: झूठ! कई लोगों के लिए अच्छा नाश्ता दिन की अच्छी शुरुआत है।", "Jawab: *JHOOTH! Kai logon ke liye *achha naashta din ki shuruaat hai.", ["JAWAB:", "*JHOOTH!"], "BREAKFAST_IN",
 "दलिया, फल या दही जैसा हल्का नाश्ता चुनिए।", "*Daliya, *fal ya *dahi jaisa halka naashta chuniye.", ("MEAL_IN", "MILK_IN")))
R.append(qz("s09_raat", "f", "m", ("सच या झूठ? रात का खाना बहुत देर से खाने में कोई हर्ज नहीं?", SJ + " *Raat ka khana *der se khane mein koi harj nahi?"), ["SACH YA JHOOTH?", "*DER RAAT KA KHANA?"], ("FX_EARS", "EVE_IN"),
 "FX_NO", "जवाब: झूठ! सोने से दो-तीन घंटे पहले हल्का खाना बेहतर माना जाता है।", "Jawab: *JHOOTH! Sone se *2-3 ghante pehle *halka khana behtar maana jaata hai.", ["JAWAB:", "*JHOOTH!"], "MEAL_IN",
 "रात को थोड़ा टहलिए और पानी आराम से पीजिए।", "Raat ko thoda *tehliye, aur *paani aaraam se piyo.", ("WALK_IN", "MILK_IN")))
R.append(qz("s10_roti", "m", "f", ("सच या झूठ? वज़न घटाना है तो रोटी बिल्कुल छोड़ देनी चाहिए?", SJ + " Weight ke liye *roti bilkul chhod deni chahiye?"), ["SACH YA JHOOTH?", "*ROTI CHHODNI HAI?"], ("FX_SHOCK", "ROTI_IN"),
 "FX_NO", "जवाब: झूठ! मात्रा और संतुलन मायने रखता है।", "Jawab: *JHOOTH! *Matra aur *santulan mayne rakhta hai.", ["JAWAB:", "*JHOOTH!"], "ROTI_IN",
 "दाल, सब्ज़ी और सलाद के साथ घर की रोटी, सही मात्रा में।", "*Dal, *sabzi aur *salad ke saath ghar ki roti, sahi matra mein.", ("MEAL_IN", "SPICE_IN")))
R.append(qz("s11_tehelna", "f", "m", ("सच या झूठ? खाने के बाद दस मिनट टहलना अच्छी आदत है?", SJ + " Khane ke baad *10 minute tehalna achhi aadat hai?"), ["SACH YA JHOOTH?", "*KHANE KE BAAD TEHALNA"], ("FX_EXC", "WALK_IN"),
 "FX_YES", "जवाब: सच! हल्की सैर को पाचन के लिए अच्छी आदत माना जाता है।", "Jawab: *SACH! Halki *sair ko *pachan ke liye achhi aadat maana jaata hai.", ["JAWAB:", "*SACH!"], "WALK_IN",
 "पाचन की रूटीन के लिए कामधेनु रस भी देखिए।", "*Pachan ki routine ke liye *Kamdudha Ras bhi dekhiye.", ("WALK_IN", "WALK_IN"), mid="@dig_kamdudha"))
R.append(qz("s12_neend", "m", "f", ("सच या झूठ? कम सोने से भूख ज़्यादा लगती है?", SJ + " *Kam sone se *bhookh zyada lagti hai?"), ["SACH YA JHOOTH?", "*KAM NEEND = ZYADA BHOOKH?"], ("FX_EARS", "OFFICE_IN"),
 "FX_YES", "जवाब: सच! कई शोध में नींद और भूख का संबंध देखा गया है।", "Jawab: *SACH! Kai *shodh mein *neend aur *bhookh ka sambandh dekha gaya hai.", ["JAWAB:", "*SACH!"], "YOGA_IN",
 "रोज़ समय पर सोइए, और सोने से पहले मोबाइल दूर रखिए।", "Roz *samay par soiye, aur sone se pehle *mobile door rakhiye.", ("YOGA_IN", "PHONE_IN")))
R.append(qz("s13_saunf", "f", "m", ("सच या झूठ? खाने के बाद थोड़ा गुड़ या सौंफ़, पुरानी देसी आदत है?", SJ + " Khane ke baad *gud ya *saunf, purani *desi aadat hai?"), ["SACH YA JHOOTH?", "*GUD YA SAUNF?"], ("FX_NAM", "SPICE_IN"),
 "FX_YES", "जवाब: सच! बस मात्रा छोटी रखिए।", "Jawab: *SACH! Bas *matra *chhoti rakhiye.", ["JAWAB:", "*SACH!"], "KIT_IN",
 "थोड़ी सी सौंफ़ या छोटी डली गुड़, ज़रूरत भर।", "Thodi si *saunf ya chhoti dali *gud, *zaroorat bhar.", ("MEAL_IN", "SPICE_IN")))
R.append(qz("s14_paani_pehle", "m", "f", ("सच या झूठ? खाने से पहले पानी पीने से कम भूख लगती है?", SJ + " Khane se pehle *paani peene se *kam bhookh lagti hai?"), ["SACH YA JHOOTH?", "*KHANE SE PEHLE PAANI"], ("FX_POINT", "MILK_IN"),
 "FX_SHRUG", "जवाब: कुछ लोगों के लिए सच! पेट थोड़ा भरा लगता है।", "Jawab: *kuch logon ke liye *SACH! Pet thoda bhara lagta hai.", ["JAWAB:", "*KUCH LOGON KE LIYE SACH"], "MEAL_IN",
 "एक गिलास पानी आराम से, और फिर धीरे-धीरे खाइए।", "Ek glass *paani aaraam se, phir *dheere-dheere khaiye.", ("MEAL_IN", "BREAKFAST_IN")))
