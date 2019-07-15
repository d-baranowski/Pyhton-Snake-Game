#!/usr/bin/env python -u

from random import randint # Import randint function which generates random numbers
from time import sleep # Import sleep function which makes the program wait for a given ammount of seconds

print "Wait for it..."
sleep(3)
print randint(0, 1000)