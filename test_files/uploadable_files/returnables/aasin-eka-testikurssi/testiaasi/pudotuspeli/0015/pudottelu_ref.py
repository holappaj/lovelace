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
            
        cx = target["x"] + target["w"] / 2
        for other_target in objects[:i]:
            otw = other_target["w"]
            oty = other_target["y"]
            otcx = other_target["x"] + otw / 2
            oth = other_target["h"]
            if target["y"] <= oty + oth:
                if abs(cx - otcx) < min(otw, target["w"]):
                    static = True
                    target["vy"] = 0
                    target["y"] = other_target["y"] + other_target["h"]
                    break
        
        if not static:
            target["vy"] -= DOWNFORCE
            target["y"] += target["vy"]
            