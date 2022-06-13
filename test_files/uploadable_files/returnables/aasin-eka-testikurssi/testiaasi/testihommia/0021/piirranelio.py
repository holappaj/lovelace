from turtle import *

def piirra_nelio(pituus, x, y):
    up()
    set(x)
    set(y)
    down()
    if x < 0:
        color("red")
    elif x > 0:
        color("blue")
    begin_fill()
    forward(pituus)
    right(90)
    forward(pituus)
    right(90)
    forward(pituus)
    right(90)
    forward(pituus)
    end_fill()
		
piirra_nelio(40, -100, 100)
piirra_nelio(60, 100, -100)
piirra_nelio(100, -50, -20)
piirra_nelio(80, 90, 30)
done()
    