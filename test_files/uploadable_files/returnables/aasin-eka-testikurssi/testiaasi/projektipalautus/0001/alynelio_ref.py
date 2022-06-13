from turtle import *

def piirra_nelio(s, x, y):
    up()
    setx(x)
    sety(y)    
    down()
    if x > 0 and y > 0:
        seth(180)
    elif x > 0:
        seth(90)
    elif y > 0:
        seth(270)
    else:
        seth(0)
        
    forward(s)
    left(90)
    forward(s)
    left(90)
    forward(s)
    left(90)
    forward(s)
    
    
if __name__ == "__main__":
    draw_square(30, 100, 100)    
    draw_square(30, 100, -100)
    draw_square(30, -100, 100)
    draw_square(30, -100, -100)
    
    
    
    done()