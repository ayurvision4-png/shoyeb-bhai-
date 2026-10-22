# products_ds — product photo library (source: source/docscanner.pdf)

Primary photo source for ALL new reels. `products_ds/<product>/NN.jpg` = PDF slides in order (originals, uncropped, ~593–596 px wide).
Page map: `pages.json` (product -> [first_page, last_page], 0-based page index of the PDF).

## Use rules
- Use as `"photo": "products_ds/<product>/NN.jpg"` in reels.json scenes.
- NEVER show slides whose text makes treatment/disease claims: Ayurland "Assists In The Treatment of" slide (index 05 of each Ayurland product), "Fight Chronic Diseases" (ortho_tablet/08), Stop Up-D diabetes slides (05-06), Ortho "Benefits", Nano/other benefit lists. Prefer the hero/name slide, woman/man lifestyle slide, "How to consume", ingredient/herb slides, certification slides.
- No prices anywhere. WhatsApp watermark is added by make_reel.py.

## Ayurland tablet pattern (7 slides each): 01 Why Ayurland, 02 How to consume, 03 Keep environment safe, 04 Why <product>, 05 Assists in treatment (DO NOT USE), 06 Product name + herbs (best hero), 07 Lifestyle person (best hero)
trifala, shivakshar_pachan, saptamrut_loh, punarnavadi_guggulu, pathyadi_kwath, kanchnar_guggulu (slide 03/04 differ), kamdudha_ras, kaishor_guggulu, guduchi_ghan, chandraprabha_vati, ashwagandha_tablet, arjun_ghan, amla_tablet (livepat has 8).

## Products (pages)
veg_omega 0-5 | d3_spray 6-11 | shilajit_gummy 12-17 | protein_powder 18-23 | ortho_tablet 24-31 | nano_curcumin 32-36 | b12_spray 37-43 | pilocare 44-50 | stop_up_d 51-57 | calcium_chewable 58-64 | trifala 65-71 | shivakshar_pachan 72-78 | she_well 79-85 | saptamrut_loh 86-92 | punarnavadi_guggulu 93-99 | pathyadi_kwath 100-106 | livepat 107-114 | kanchnar_guggulu 115-121 | kamdudha_ras 122-128 | kaishor_guggulu 129-135 | guduchi_ghan 136-142 | chandraprabha_vati 143-149 | ashwagandha_tablet 150-156 | arjun_ghan 157-163 | amla_tablet 164-170 | tulsi_drops 171-177 | thyrocare_balance_drink 178-184 | spirulina 185-191 | slim_tea 192-199 | shewell_drink 200-205 | beautilook 206-212 | sea_buckthorn 213-219 | pocket_energy 220-226 | red_aloe_vera 227-232 | do_long 233-237

## Key products
- beautilook (206-212): 01 easy-to-follow routine, 02 structured wellness regime, 03 enriched with pure herbs, 04 designed for modern lifestyles, 05 empower your daily routine, 06 Beautilook Tablet pack hero, 07 3-bottle box hero.
- slim_tea (192-199): 01 Slim Tea hero girl, 02 why us, 03 cup of tea, 04 making a cup (steps), 05 6 selected herbs, 06 ability of 6 herbs, 07 pack + cup, 08 safe & trusted.
- tulsi_drops (171-177): 01 Nourish your body, 02 dosage, 03 benefits list, 04 improves health of, 05 5 types of tulsi, 06 benefits icons, 07 TULSI DROP banner.
- Old library (products/<name>) still has alkomax, berry, boswellia, cmd, detox, livofit, noni, do_long (not in the PDF).
