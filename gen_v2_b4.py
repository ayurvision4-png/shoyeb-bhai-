# batch 4: weight/habit myth quiz reels (funnel to Beautilook end card), exec'd from gen_v2.py after b3
def mk(name, w, hq, hb, thk, ans_say, ans_txt, ans_big, tip_say, tip_txt, tip_shots, shots_h, shots_a, mid=None):
    sc_tip = (card(w, tip_say, tip_txt, [mid, tip_shots[0]]) if mid else sc(w, tip_say, tip_txt, list(tip_shots)))
    return reel(name, w, [
        qhook(w, hq[0], hq[1], shots_h, hb),
        think(w, thk),
        ans(w, ans_say, ans_txt, shots_a, ans_big),
        sc_tip,
        qcta(w)])
R.append(mk("s07_nimbu", "f",
 ("सच या झूठ? सुबह गुनगुना पानी और नींबू, वज़न घटा देता है?", "*SACH ya *JHOOTH? Subah *nimbu paani se *weight ghatta hai?"), ["SACH YA JHOOTH?", "*NIMBU PAANI = WEIGHT?"], ("PHONE", "SMILE"),
 "जवाब: झूठ! कोई चमत्कार नहीं, पर अच्छी आदत ज़रूर है।", "Jawab: *JHOOTH! Koi *chamatkar nahi, par *achhi aadat zaroor hai.", ["JAWAB:", "*JHOOTH!"],
 "असली फ़र्क़ आता है सही खाने, रोज़ की सैर और अच्छी नींद से।", "Asli farq: *sahi khana, roz ki *sair, aur achhi *neend se.", ("WALKSUN", "SLEEP"), ["WATER", "SUNRISE"], ["WATER", "HERBS"]))
R.append(mk("s08_naashta", "m",
 ("सच या झूठ? वज़न घटाना है तो नाश्ता छोड़ देना चाहिए?", "*SACH ya *JHOOTH? Weight ke liye *naashta skip karna chahiye?"), ["SACH YA JHOOTH?", "*NAASHTA SKIP?"], ("FRIENDS", "SMILE"),
 "जवाब: झूठ! कई लोगों के लिए अच्छा नाश्ता दिन की अच्छी शुरुआत है।", "Jawab: *JHOOTH! Kai logon ke liye *achha naashta din ki shuruaat hai.", ["JAWAB:", "*JHOOTH!"],
 "दलिया, फल या दही जैसा हल्का नाश्ता चुनिए।", "*Daliya, *fal ya *dahi jaisa halka naashta chuniye.", ("FOOD", "MILK"), ["WAKE", "FOOD"], ["FOOD", "FRUIT"]))
R.append(mk("s09_raat", "f",
 ("सच या झूठ? रात का खाना बहुत देर से खाने में कोई हर्ज नहीं?", "*SACH ya *JHOOTH? *Raat ka khana *der se khane mein koi harj nahi?"), ["SACH YA JHOOTH?", "*DER RAAT KA KHANA?"], ("OFFICE", "FRIENDS"),
 "जवाब: झूठ! सोने से दो-तीन घंटे पहले हल्का खाना बेहतर माना जाता है।", "Jawab: *JHOOTH! Sone se *2-3 ghante pehle *halka khana behtar maana jaata hai.", ["JAWAB:", "*JHOOTH!"],
 "रात को थोड़ा टहलिए और पानी आराम से पीजिए।", "Raat ko thoda *tehliye, aur *paani aaraam se piyo.", ("NIGHT", "WATER"), ["NIGHT", "FOOD"], ["NIGHT", "VEG"]))
R.append(mk("s10_roti", "m",
 ("सच या झूठ? वज़न घटाना है तो रोटी बिल्कुल छोड़ देनी चाहिए?", "*SACH ya *JHOOTH? Weight ke liye *roti bilkul chhod deni chahiye?"), ["SACH YA JHOOTH?", "*ROTI CHHODNI HAI?"], ("FRIENDS", "OFFICE"),
 "जवाब: झूठ! मात्रा और संतुलन मायने रखता है।", "Jawab: *JHOOTH! *Matra aur *santulan mayne rakhta hai.", ["JAWAB:", "*JHOOTH!"],
 "दाल, सब्ज़ी और सलाद के साथ घर की रोटी, सही मात्रा में।", "*Dal, *sabzi aur *salad ke saath ghar ki roti, sahi matra mein.", ("FOOD", "VEG"), ["FOOD", "GYM"], ["FOOD", "VEG"]))
R.append(mk("s11_tehelna", "f",
 ("सच या झूठ? खाने के बाद दस मिनट टहलना अच्छी आदत है?", "*SACH ya *JHOOTH? Khane ke baad *10 minute tehalna achhi aadat hai?"), ["SACH YA JHOOTH?", "*KHANE KE BAAD TEHALNA"], ("OFFICE", "SMILE"),
 "जवाब: सच! हल्की सैर को पाचन के लिए अच्छी आदत माना जाता है।", "Jawab: *SACH! Halki *sair ko *pachan ke liye achhi aadat maana jaata hai.", ["JAWAB:", "*SACH!"],
 "पाचन की रूटीन के लिए कामधेनु रस भी देखिए।", "*Pachan ki routine ke liye *Kamdudha Ras bhi dekhiye.", ("WALKSUN", "WALKSUN"), ["FOOD", "WALKSUN"], ["WALKSUN", "SMILE"], mid="@dig_kamdudha"))
R.append(mk("s12_neend", "m",
 ("सच या झूठ? कम सोने से भूख ज़्यादा लगती है?", "*SACH ya *JHOOTH? *Kam sone se *bhookh zyada lagti hai?"), ["SACH YA JHOOTH?", "*KAM NEEND = ZYADA BHOOKH?"], ("NIGHT", "PHONE"),
 "जवाब: सच! कई शोध में नींद और भूख का संबंध देखा गया है।", "Jawab: *SACH! Kai *shodh mein *neend aur *bhookh ka sambandh dekha gaya hai.", ["JAWAB:", "*SACH!"],
 "रोज़ समय पर सोइए, और सोने से पहले मोबाइल दूर रखिए।", "Roz *samay par soiye, aur sone se pehle *mobile door rakhiye.", ("SLEEP", "NIGHT"), ["SLEEP", "NPHONE"], ["SLEEP", "NIGHT"]))
R.append(mk("s13_saunf", "f",
 ("सच या झूठ? खाने के बाद थोड़ा गुड़ या सौंफ़, पुरानी देसी आदत है?", "*SACH ya *JHOOTH? Khane ke baad *gud ya *saunf, purani *desi aadat hai?"), ["SACH YA JHOOTH?", "*GUD YA SAUNF?"], ("SPICES", "HONEY"),
 "जवाब: सच! बस मात्रा छोटी रखिए।", "Jawab: *SACH! Bas *matra *chhoti rakhiye.", ["JAWAB:", "*SACH!"],
 "थोड़ी सी सौंफ़ या छोटी डली गुड़, ज़रूरत भर।", "Thodi si *saunf ya chhoti dali *gud, *zaroorat bhar.", ("SPICES", "HERBS"), ["SPICES", "FOOD"], ["HONEY", "SPICES"]))
R.append(mk("s14_paani_pehle", "m",
 ("सच या झूठ? खाने से पहले पानी पीने से कम भूख लगती है?", "*SACH ya *JHOOTH? Khane se pehle *paani peene se *kam bhookh lagti hai?"), ["SACH YA JHOOTH?", "*KHANE SE PEHLE PAANI"], ("WATER", "FOOD"),
 "जवाब: कुछ लोगों के लिए सच! पेट थोड़ा भरा लगता है।", "Jawab: *kuch logon ke liye *SACH! Pet thoda bhara lagta hai.", ["JAWAB:", "*KUCH LOGON KE LIYE SACH"],
 "एक गिलास पानी आराम से, और फिर धीरे-धीरे खाइए।", "Ek glass *paani aaraam se, phir *dheere-dheere khaiye.", ("WATER", "FOOD"), ["WATER", "FRUIT"], ["WATER", "VEG"]))
