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
            if target["y"] + target["vy"] <= oty + oth:
                if abs(cx - otcx) < (otw + target["w"]) / 2:
                    static = True
                    target["vy"] = 0
                    target["y"] = oty + oth
                    break
        
        if not static:
            target["vy"] -= DOWNFORCE
            target["y"] += target["vy"]

            
if __name__ == "__main__":
    test = [{'_id': 67, 'x': 340, 'y': 68, 'w': 21, 'h': 21, 'vy': 0}, {'_id': 68, 'x': 329.5, 'y': 204, 'w': 42, 'h': 42, 'vy': 0}]

    for i in range(100):
        pudota(test)
    
    print(test)
