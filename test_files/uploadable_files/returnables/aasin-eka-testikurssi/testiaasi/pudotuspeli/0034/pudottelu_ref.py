import random
import haravasto as ha

WINDOW_W = 1200
WINDOW_H = 600

GROUND_LEVEL = 0
DOWNFORCE = 1.5

game = {
    "boxes": []
}

def top(box):
    return box["y"] + box["h"]
    

def luo_laatikot(n, alaraja):
    boxes = []
    for i in range(n):
        boxes.append({
            "x": random.randint(0, WINDOW_W - 40),
            "y": random.randint(alaraja, WINDOW_H),
            "w": 40,
            "h": 40,
            "vy": 0
        })
    return boxes
    
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

            
def update(kulunut):
    pudota(game["boxes"])
            

def draw():
    ha.tyhjaa_ikkuna()
    ha.piirra_tausta()
    ha.aloita_ruutujen_piirto()
    for box in game["boxes"]:
        ha.lisaa_piirrettava_ruutu(" ", box["x"], box["y"])
    ha.piirra_ruudut()
    
            
def main():
    ha.lataa_kuvat(".")
    ha.luo_ikkuna(WINDOW_W, WINDOW_H)
    ha.aseta_piirto_kasittelija(draw)
    ha.aseta_toistuva_kasittelija(update)
    ha.aloita()
            
if __name__ == "__main__":
    #game["boxes"] = [{'_id': 67, 'x': 340, 'y': 68, 'w': 40, 'h': 40, 'vy': 0}, {'_id': 68, 'x': 329.5, 'y': 204, 'w': 40, 'h': 40, 'vy': 0}]
    game["boxes"] = luo_laatikot(10, 400)    
    main()

