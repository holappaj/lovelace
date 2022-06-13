from operator import itemgetter

GROUND_LEVEL = 0
DOWNFORCE = 1.5

def pudota(objects):
    objects.sort(key=itemgetter("y"))
    for i, target in enumerate(objects):
        static = False
        if target["y"] <= GROUND_LEVEL:
            static = True
            target["vy"] = 0
            target["y"] = GROUND_LEVEL
            continue
            
        for other_target in objects[:i]:
            if target["y"] - target["h"] <= other_target["y"]:
                if abs(target["x"] - other_target["x"]) < min(target["w"], other_target["w"]):
                    static = True
                    target["vy"] = 0
                    target["y"] = other_target["y"] + target["h"]
                    break
        
        if not static:
            target["vy"] -= DOWNFORCE
            target["y"] += target["vy"]
            