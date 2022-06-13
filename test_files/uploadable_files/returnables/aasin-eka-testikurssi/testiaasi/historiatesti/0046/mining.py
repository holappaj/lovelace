import random
import sweeperlib

state = {
    "field": []
}

def place_mines(field, tiles, n):
    spots = random.sample(tiles, n)
    for c, r in spots:
        field[r][c] = "x"

def draw_field():
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    for r, row in enumerate(state["field"]):
        for c, tile in enumerate(row):
            sweeperlib.prepare_sprite(tile, c * 40, r * 40)
    sweeperlib.draw_sprites()
    
def main():
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(600, 400)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.start()
    
if __name__ == "__main__":
    field = []
    for row in range(10):
        field.append([])
        for col in range(15):
            field[-1].append(" ")

    state["field"] = field