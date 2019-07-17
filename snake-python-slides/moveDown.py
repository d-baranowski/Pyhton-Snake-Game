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

print "xChange: {0} yChange: {1}".format(xChange, yChange)
print "Moving down now."
moveDown()
print "xChange: {0} yChange: {1}".format(xChange, yChange)