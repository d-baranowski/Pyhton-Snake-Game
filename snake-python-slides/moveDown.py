#!/usr/bin/env python -u
xChange = 0
yChange = 0

def moveDown():
    global xChange
    global yChange
    global head

    # If not moving up
    if not (xChange == 0 and yChange == 1):
        xChange = 0
        yChange = -1

print "X: {0} Y: {1}".format(x, y)
print "Moving down now."
moveDown()
print "X: {0} Y: {1}".format(x, y)



def moveLeft():
    global xChange
    global yChange
    global head

    # If not moving right
    if not (xChange == 1 and yChange == 0):
        xChange = -1
        yChange = 0
        
def moveRight():
    global xChange
    global yChange
    global head

    # If not moving left
    if not (xChange == -1 and yChange == 0):
        xChange = 1
        yChange = 0