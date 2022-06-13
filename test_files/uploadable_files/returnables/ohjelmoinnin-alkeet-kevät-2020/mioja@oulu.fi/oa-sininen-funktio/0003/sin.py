import math

def convert_to_xy(a, r):
    x = int(round(math.cos(a) * r))
    y = int(round(math.sin(a) * r))
    return x, y

