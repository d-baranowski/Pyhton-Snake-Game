#!/usr/bin/env python -u
from turtle import *
from time import sleep

#Game engine setup  
hideturtle()
penup()
delay(0)
tracer(0, 0)
step = 22
screensize(35 * step, 35 * step)
setup(width=1.0, height=1.0, startx=None, starty=None)
# END OMIT
#Register Shapes
register_shape("rock.gif")

rocks = Turtle()
rocks.speed(0)
rocks.penup()
rocks.shape('rock.gif')
rocks.hideturtle()
rocksXList = [1,2,3,4,5,6]
rocksYList = [1,2,3,4,5,6]

while(True):
    rocks.clearstamps()
    
    #Draw rocks
    for i in range(len(rocksXList)):
        rocks.setposition(rocksXList[i] * step, rocksYList[i] * step)
        rocks.stamp()
    update()
    sleep(0.05)
# START OMIT