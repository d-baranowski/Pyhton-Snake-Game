#!/usr/bin/env python -u
xChange = 0
yChange = 0

def moveUp():
    global xChange
    global yChange

    # If not moving down
    if not (xChange == 0 and yChange == -1):
        xChange = 0
        yChange = 1

print "X: {0} Y: {1}".format(x, y)
print "Moving up now."
moveUp()
print "X: {0} Y: {1}".format(x, y)