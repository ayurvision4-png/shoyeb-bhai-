import json,sys
def add(name,lines,clips1,clips4,photos,cap1,caps,kw,music):
    r=json.load(open('reels.json')); r=[x for x in r if x['name']!=name]
    sc=[{"say":lines[0],"cap":cap1,"multi":[[c] for c in clips1]},
        {"say":lines[1],"cap":caps[0],"photo":photos[0]},
        {"say":lines[2],"cap":caps[1],"photo":photos[1]},
        {"say":lines[3],"cap":"DM karo: "+kw,"multi":[[c] for c in clips4]}]
    r.append({"name":name,"capsize":64,"fade":0.4,"music":music,"scenes":sc,"end_cut":["cutouts/1000153679.png"],
      "end_say":"टीमएक्स ब्यूटीलुक। फील गुड, लुक गुड, लिव बेटर!","end_cap":"Feel Good, Look Good, Live Better!"})
    json.dump(r,open('reels.json','w'),ensure_ascii=False,indent=1)
