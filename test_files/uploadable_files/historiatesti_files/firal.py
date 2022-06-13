from turtle import *

def draw_spiral(c, arcs, r, growth, w=1):
    pensize(w)
    color(c)
    for i in range(arcs):
        circle(r + i * growth, 90)

def draw_from_file(fn):
    with open(fn) as f:
        for line in f.readlines():
            if line:
                color, n, r, growh, w = line.split(",")
                draw_spiral(color, int(n), int(r), float(growh), int(w))
                