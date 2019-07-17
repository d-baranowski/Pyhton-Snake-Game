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

print "xChange: {0} yChange: {1}".format(xChange, yChange)
print "Moving up now."
moveUp()
print "xChange: {0} yChange: {1}".format(xChange, yChange)