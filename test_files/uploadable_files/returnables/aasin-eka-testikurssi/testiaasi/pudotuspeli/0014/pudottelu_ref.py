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
            otx = other_target["x"]
            otw = other_target["w"]
            oty = other_target["y"]
            oth = other_target["h"]
            if target["y"] <= oty + oth:
                if otx < target["x"] < otx + otw\
                or otx < target["x"] + target["w"] < otx + otw:
                    static = True
                    target["vy"] = 0
                    target["y"] = other_target["y"] + other_target["h"]
                    break
        
        if not static:
            target["vy"] -= DOWNFORCE
            target["y"] += target["vy"]
            