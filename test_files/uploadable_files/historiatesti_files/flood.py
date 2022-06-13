#import sweeperlib
import timeit


def floodfill(planet, init_x, init_y):
    area = [(init_x, init_y)]
    if planet[init_y][init_x] == "x":
        return
    while area:
        x, y = area.pop()
        planet[y][x] = "0"
        for r, row in enumerate(planet[max(0, y - 1):y + 2], start=max(0, y - 1)):
            for c, tile in enumerate(row[max(0, x - 1):x + 2], start=max(0, x - 1)):
                if tile == " " and (c, r) not in area:
                    area.append((c, r))

def floodfill_set(planet, init_x, init_y):
    area = {(init_x, init_y)}
    if planet[init_y][init_x] == "x":
        return
    while area:
        x, y = area.pop()
        planet[y][x] = "0"
        for r, row in enumerate(planet[max(0, y - 1):y + 2], start=max(0, y - 1)):
            for c, tile in enumerate(row[max(0, x - 1):x + 2], start=max(0, x - 1)):
                if tile == " ":
                    area.add((c, r))

def floodfill_recur(planet, x, y):
    if planet[y][x] == "x":
        return
    planet[y][x] = "0"
    for r, row in enumerate(planet[max(0, y - 1):y + 2], start=max(0, y - 1)):
        for c, tile in enumerate(row[max(0, x - 1):x + 2], start=max(0, x - 1)):
            if tile == " ":
                floodfill_recur(planet, c, r)
                    
def draw_field():
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    for r, row in enumerate(state["field"]):
        for c, tile in enumerate(row):
            sweeperlib.prepare_sprite(tile, c * 40, r * 40)
    sweeperlib.draw_sprites()

def main(planet):
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(len(planet[0]) * 40, len(planet) * 40)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.start()
   
if __name__ == "__main__":
    planet = [
        [" ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x", " "], 
        [" ", " ", "x", "x", " ", " ", " ", "x", " ", " ", " ", "x", " "], 
        [" ", "x", "x", " ", " ", " ", " ", "x", " ", " ", "x", "x", " "], 
        ["x", "x", "x", "x", "x", " ", " ", "x", " ", "x", " ", " ", " "], 
        ["x", "x", "x", "x", " ", " ", " ", " ", "x", " ", "x", " ", " "], 
        [" ", " ", "x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " "]
    ]
    #floodfill(planet, 4, 2)
    #main(planet)
    print(timeit.timeit("floodfill(planet, 4, 2)", setup="from __main__ import floodfill, planet"))
    print(timeit.timeit("floodfill_set(planet, 4, 2)", setup="from __main__ import floodfill_set, planet"))
    print(timeit.timeit("floodfill_recur(planet, 4, 2)", setup="from __main__ import floodfill_recur, planet"))
    