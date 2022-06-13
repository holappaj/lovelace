from operator import itemgetter

GROUND_LEVEL = 0
DOWNFORCE = 1.5

def top(box):
    return box["y"] + box["h"]
    

def pudota(objects):
    objects.sort(key=top)
    for i, target in enumerate(objects):
        static = False
        if target["y"] <= GROUND_LEVEL:
            static = True
            target["vy"] = 0
            target["y"] = GROUND_LEVEL
            continue
            
        cx = target["x"] + target["w"] / 2
        for other_target in reversed(objects[:i]):
            otw = other_target["w"]
            oty = other_target["y"]
            otcx = other_target["x"] + otw / 2
            oth = other_target["h"]
            if target["y"] <= oty + oth:
                if abs(cx - otcx) < (otw + target["w"]) / 2:
                    static = True
                    target["vy"] = 0
                    target["y"] = other_target["y"] + other_target["h"]
                    break
        
        if not static:
            target["vy"] -= DOWNFORCE
            target["y"] += target["vy"]
            