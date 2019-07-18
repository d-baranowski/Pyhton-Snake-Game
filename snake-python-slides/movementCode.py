#!/usr/bin/env python -u
from time import sleep # Import sleep function which makes the program wait for a given ammount of seconds
x = 4; y = 0
xChange = 1; yChange = 0

tailLength = 3
previousY = [0,0,0]; previousX = [3,2,1]

while(True):
    #Insert current x at the start of previousX list
    previousX.insert(0,x); previousY.insert(0,y)

    # Move head
    x = x + xChange; y = y + yChange

    #Cut list to size of tail
    previousX = previousX[:tailLength]
    previousY = previousY[:tailLength]

    print "X: {0} Y: {1}".format(x, y)
    print "previousX: %s" % str(previousX)
    print "previousY: %s" % str(previousY)
    sleep(0.5)