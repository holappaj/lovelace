import math

def calculate_square_area(side):
    return side ** 2

def calculate_sector_area(r, a):
    return math.pi * r ** 2 * a / 360

def calculate_catheti(h):
    return h / (2 ** 0.5)

def calculate_figure_area(x):
    small_sq = calculate_square_area(x)
    side = calculate_catheti(x)
    triangle = calculate_square_area(side) / 2
    small_sector = calculate_sector_area(side, 45)
    large_sq = calculate_square_area(side * 2)
    large_sector = calculate_sector_area(side * 2, 270)
    return small_sq + small_sector + triangle + large_sq + large_sector

key = float(input(": "))
print(":", round(calculate_figure_area(key), 4))