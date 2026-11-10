# batch 3: engagement-first quiz reels ("Sach ya Jhooth") + giveaway reel (exec'd from gen_v2.py)
def qhook(w, say, txt, shots, big): return sc(w, say, txt, shots, big=big, big_y=260, big_size=108)
def think(w, shots=("SMILE", "FRIENDS")):
    return sc(w, "सोचिए... कमेंट में लिखिए, सच या झूठ!", "Socho... comment mein likho *SACH ya *JHOOTH!", list(shots), big=["COMMENT KARO", "*SACH YA JHOOTH"], big_y=330, big_size=100)
def ans(w, say, txt, shots, big): return sc(w, say, txt, shots, big=big, big_y=300, big_size=104)
QS = "रोज़ के सच-झूठ के लिए फ़ॉलो करिए, और फ्री चार्ट के लिए चार्ट लिखिए!"
QT = "Roz ke *sach-jhooth ke liye *FOLLOW karo, free chart ke liye *CHART likho!"
def qcta(w, shots=("FRIENDS", "SMILE")): return fcta(w, shots, ("FOLLOW KARO", "*ROZ SACH-JHOOTH"), QS, QT)
w = "m"
R.append(reel("s01_ghee", w, [
 qhook(w, "सच या झूठ? घी खाने से वज़न बढ़ता है?", "*SACH ya *JHOOTH? Ghee khane se *weight badhta hai?", ["MILK", "FOOD"], ["SACH YA JHOOTH?", "*GHEE = WEIGHT?"]),
 think(w),
 ans(w, "जवाब: मात्रा का खेल है। ज़्यादा कुछ भी हो, वज़न बढ़ सकता है।", "Jawab: *matra ka khel hai. *Zyada kuch bhi, weight badha sakta hai.", ["FOOD", "VEG"], ["JAWAB:", "*MATRA KA KHEL"]),
 sc(w, "दाल-सब्ज़ी के साथ थोड़ा सा घी, और रोज़ की सैर।", "Dal-sabzi ke saath *thoda ghee, aur roz ki *sair.", ["WALKSUN", "HERBS"]),
 qcta(w)]))
w = "f"
R.append(reel("s02_thanda", w, [
 qhook(w, "सच या झूठ? ठंडा पानी पीने से पेट की चर्बी जमती है?", "*SACH ya *JHOOTH? Thanda paani peene se *pet ki charbi jamti hai?", ["WATER", "FRUIT"], ["SACH YA JHOOTH?", "*THANDA PAANI"]),
 think(w),
 ans(w, "जवाब: झूठ! इसका कोई पक्का प्रमाण नहीं है।", "Jawab: *JHOOTH! Iska koi *pakka praman nahi hai.", ["WATER", "SKIN"], ["JAWAB:", "*JHOOTH!"]),
 sc(w, "सर्दी में गुनगुना पानी कई लोगों को अच्छा लगता है।", "Sardi mein *gunguna paani *kai logon ko achha lagta hai.", ["TEA", "SMILE"]),
 qcta(w)]))
w = "m"
R.append(reel("s03_khalipet", w, [
 qhook(w, "सच या झूठ? खाली पेट चाय पीना ठीक है?", "*SACH ya *JHOOTH? Khaali pet chai peena theek hai?", ["TEA", "COFFEE"], ["SACH YA JHOOTH?", "*KHAALI PET CHAI?"]),
 think(w),
 ans(w, "जवाब: बेहतर है पहले पानी, फिर कुछ हल्का खाना।", "Jawab: *behtar hai pehle *paani, phir kuch halka khana.", ["WATER", "FRUIT"], ["JAWAB:", "*PEHLE PAANI"]),
 card(w, "चाय में तुलसी-अदरक डालिए, और रूटीन में तुलसी ड्रॉप भी।", "Chai mein *tulsi-adrak daaliye, aur routine mein *Tulsi Drop bhi.", ["@imm_tulsi", "HERBS"]),
 qcta(w)]))
w = "f"
R.append(reel("s04_mobile", w, [
 qhook(w, "सच या झूठ? मोबाइल देखते हुए खाना, ज़्यादा खिला देता है?", "*SACH ya *JHOOTH? Mobile dekhte hue khana, *zyada khila deta hai?", ["PHONE", "FOOD"], ["SACH YA JHOOTH?", "*MOBILE + KHANA"]),
 think(w),
 ans(w, "जवाब: सच! ध्यान भटकता है, तो पेट का पता नहीं चलता।", "Jawab: *SACH! Dhyan bhatakta hai, to *pet ka pata nahi chalta.", ["PHONE", "VEG"], ["JAWAB:", "*SACH!"]),
 sc(w, "खाते समय सिर्फ़ खाना, और धीरे-धीरे चबाइए।", "Khaate samay *sirf khana, aur *dheere-dheere chabaiye.", ["FOOD", "SMILE"]),
 qcta(w)]))
w = "m"
R.append(reel("s05_8glass", w, [
 qhook(w, "सच या झूठ? सबको रोज़ आठ गिलास पानी ज़रूरी है?", "*SACH ya *JHOOTH? Sabko roz *8 glass paani zaroori hai?", ["WATER", "RUN"], ["SACH YA JHOOTH?", "*8 GLASS PAANI"]),
 think(w),
 ans(w, "जवाब: ज़रूरत सबकी अलग होती है।", "Jawab: *zaroorat *sabki alag hoti hai.", ["WATER", "GYM"], ["JAWAB:", "*SABKI ALAG"]),
 card(w, "प्यास सुनिए, थोड़ा-थोड़ा पीते रहिए। पानी की रूटीन के लिए सीएमडी ड्रॉप्स।", "*Pyaas sunie, thoda-thoda piyo. Paani ki routine ke liye *CMD Drops.", ["@dig_cmd", "WATER"]),
 qcta(w)]))
w = "f"
R.append(reel("s06_dhoop", w, [
 qhook(w, "सच या झूठ? धूप सिर्फ़ सर्दी में लेनी चाहिए?", "*SACH ya *JHOOTH? Dhoop sirf *sardi mein leni chahiye?", ["SUNRISE", "WALKSUN"], ["SACH YA JHOOTH?", "*DHOOP SIRF SARDI MEIN?"]),
 think(w),
 ans(w, "जवाब: झूठ! हर मौसम में थोड़ी धूप अच्छी है।", "Jawab: *JHOOTH! Har mausam mein *thodi dhoop achhi hai.", ["SUNRISE", "STRETCH"], ["JAWAB:", "*JHOOTH!"]),
 card(w, "सुबह की हल्की धूप, और कैल्शियम के साथ विटामिन डी तीन।", "Subah ki halki *dhoop, aur *Calcium ke saath *Vitamin D3.", ["@bone_d3", "@bone_calcium"]),
 qcta(w)]))
w = "f"
R.append(reel("gv01_giveaway", w, [
 hook(w, "फ्री वेलनेस किट जीतना है?", "*FREE wellness kit jeetna hai?", ["SMILE", "FRIENDS"], ["FREE WELLNESS KIT", "*JEETNA HAI?"]),
 sc(w, "एक: आयुर्विज़न को फ़ॉलो करिए।", "*1: *@ayurvision_02 ko *follow karo.", ["WALKSUN", "SMILE"]),
 sc(w, "दो: कमेंट में किट लिखिए, और दो दोस्तों को टैग करिए।", "*2: comment mein *KIT likho, *2 doston ko tag karo.", ["FRIENDS", "PHONE"]),
 sc(w, "तीन: इस रील को अपनी स्टोरी में शेयर करिए।", "*3: reel ko apni *story mein share karo.", ["PHONE", "SMILE"]),
 sc(w, "विजेता का नाम दस दिसंबर को बताया जाएगा!", "Winner ka naam *10 December ko!", ["FRIENDS", "RUN"], big=["WINNER:", "*10 DECEMBER"], big_y=330, big_size=100, dm="FOLLOW + COMMENT KIT", small="Sirf India, 18+. Is promotion ka Instagram se koi sambandh nahi.")]))
