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

print "xChange: {0} yChange: {1}".format(xChange, yChange)
print "Moving left now."
moveLeft()
print "xChange: {0} yChange: {1}".format(xChange, yChange)