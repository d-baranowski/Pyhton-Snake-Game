#!/usr/bin/env python -u
xChange = 0
yChange = 0



def moveLeft():
    global xChange
    global yChange
    global head

    # If not moving right
    if not (xChange == 1 and yChange == 0):
        xChange = -1
        yChange = 0

print "X: {0} Y: {1}".format(x, y)
print "Moving left now."
moveLeft()
print "X: {0} Y: {1}".format(x, y)
        
def moveRight():
    global xChange
    global yChange
    global head

    # If not moving left
    if not (xChange == -1 and yChange == 0):
        xChange = 1
        yChange = 0