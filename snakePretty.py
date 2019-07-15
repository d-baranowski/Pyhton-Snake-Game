from random import randint # Import randint function which generates random numbers
from time import sleep # Import sleep function which makes the program wait for a given ammount of seconds
from turtle import * # Import entire turtle module responsible for drawing graphics

#Game engine setup
delay(0)
tracer(0, 0)
step = 22
screensize(35 * step, 35 * step)
setup(width=1.0, height=1.0, startx=None, starty=None)

#Register Shapes
register_shape("apple.gif")
register_shape("rock.gif")
register_shape("head_up.gif")
register_shape("head_down.gif")
register_shape("head_left.gif")
register_shape("head_right.gif")
register_shape("tail_end_up.gif")
register_shape("tail_end_down.gif")
register_shape("tail_end_left.gif")
register_shape("tail_end_right.gif")
register_shape("tail_straight_horizontal.gif")
register_shape("tail_straight_vertical.gif")
register_shape("tail_turn_1.gif")
register_shape("tail_turn_2.gif")
register_shape("tail_turn_3.gif")
register_shape("tail_turn_4.gif")

#Game variables
gameIsRunning = True
score = 0
x = 0
y = 0
xChange = 1
yChange = 0

tailLength = 3
previousY = [0,0,0]
previousX = [-1,-2,-3]

#Head pen setup 
head = Turtle()
head.penup()
head.shape('head_right.gif')
head.speed(0)

#Tail pen setup
tail = Turtle()
tail.penup()
tail.speed(0)

#rocks pen setup
rocks = Turtle()
rocks.penup()
rocks.shape('rock.gif')
rocks.speed(0)
rocks.hideturtle()
rocksXList = []
rocksYList = []

#Apple pen setup
apple = Turtle()
apple.penup()
apple.shape('apple.gif')
apple.hideturtle()

#Apple Variables
appleX = 10
appleY = 10


#Lose message pen setup
hideturtle()
penup()
color("red")

# Bring window to front
rootwindow = getcanvas().winfo_toplevel()
rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
rootwindow.call('wm', 'attributes', '.', '-topmost', '0')

# Move apple function
def moveApple():
    global appleX, appleY
    global x,y
    global previousY, previousX, tailLength

    possibleXandY = []
    for gridx in range(-20, 21):
        for gridy in range(-17, 17):
            possibleXandY.append([gridx,gridy])

    if possibleXandY.__contains__([x,y]):
        possibleXandY.remove([x,y])

    for i in range(tailLength):
        if possibleXandY.__contains__([previousX[i],previousY[i]]):
            possibleXandY.remove([previousX[i],previousY[i]])

    for i in range(len(rocksXList)):
        if possibleXandY.__contains__([rocksXList[i],rocksYList[i]]):
            possibleXandY.remove([rocksXList[i],rocksYList[i]])

    random = randint(0,len(possibleXandY) - 1)
    appleX = possibleXandY[random][0]
    appleY = possibleXandY[random][1]
    

def setupHorizontalWall(startX, endX, y):
    global rocks
    global rocksXList
    global rocksYList
    for i in range(startX, endX + 1):
        rocksXList.append(i)
        rocksYList.append(y)

def setupVerticalWall(startY, endY, x):
    global rocks
    global rocksXList
    global rocksYList
    for i in range(startY, endY + 1):
        rocksYList.append(i)
        rocksXList.append(x)

def printScore():
    global score
    title('Score: ' + str(score))

def displayLoseMessage():
    global gameIsRunning
    global score
    clear()
    gameIsRunning = False
    setposition(-150,0)
    write('You Loose. Your score was: ' + str(score),align="left", font=("Arial", 20, "normal"))

def moveUp():
    global xChange
    global yChange
    global head

    if not (xChange == 0 and yChange == -1):
        head.shape('head_up.gif')
        xChange = 0
        yChange = 1

def moveDown():
    global xChange
    global yChange
    global head

    if not (xChange == 0 and yChange == 1):
        head.shape('head_down.gif')
        xChange = 0
        yChange = -1

def moveLeft():
    global xChange
    global yChange
    global head

    if not (xChange == 1 and yChange == 0):
        head.shape('head_left.gif')
        xChange = -1
        yChange = 0
        
def moveRight():
    global xChange
    global yChange
    global head

    if not (xChange == -1 and yChange == 0):
        head.shape('head_right.gif')
        xChange = 1
        yChange = 0


#Bind movement functions to keyboard keys    
onkey(moveUp,'Up')
onkey(moveDown,'Down')
onkey(moveLeft,'Left')
onkey(moveRight,'Right')

listen()

#Setup our rocks
#setupHorizontalWall(-21,21,18)
#setupHorizontalWall(-21,21,-18)
#setupVerticalWall(-18,18,21)
#setupVerticalWall(-18,18,-21)

#Draw rocks
for i in range(len(rocksXList)):
    rocks.setposition(rocksXList[i] * step, rocksYList[i] * step)
    rocks.stamp()


while(gameIsRunning):
    #Clear previous frame
    head.clearstamps()
    tail.clearstamps()
    apple.clearstamps()

    #Insert current x at the start of previousX list
    previousX.insert(0,x)

    #Cut list to size of tail
    previousX[:tailLength]

    #Repeat for current y
    previousY.insert(0,y)
    previousY[:tailLength]

    #Calculate new x and y positions
    x = x + xChange
    y = y + yChange

    #Move head pen to new x and y position
    head.setposition(x * step,y * step)

    #Hit wall to lose
    for i in range(len(rocksXList)):
        if (x == rocksXList[i] and y == rocksYList[i]):
            displayLoseMessage()

    #Bite tail to lose
    for i in range(tailLength):
        if (x == previousX[i] and y == previousY[i]):
            displayLoseMessage()

    #Draw head
    head.stamp()

    #Draw tail
    for i in range(tailLength):
        tail.setposition(previousX[i] * step, previousY[i] * step)

        currentSegmentX = previousX[i]
        currentSegmentY = previousY[i]
        previousSegmentX = previousX[i - 1]
        previousSegmentY = previousY[i - 1]

        if (i == tailLength -1):
            if (previousSegmentX < currentSegmentX):
                tail.shape("tail_end_left.gif")
                tail.stamp()
            elif (previousSegmentX > currentSegmentX):
                tail.shape("tail_end_right.gif")
                tail.stamp()
            elif (previousSegmentY > currentSegmentY):
                tail.shape("tail_end_up.gif")
                tail.stamp()
            elif (previousSegmentY < currentSegmentY):
                tail.shape("tail_end_down.gif")
                tail.stamp()
        else:
            if (i == 0):
                previousSegmentX = x
                previousSegmentY = y
            else:
                previousSegmentX = previousX[i - 1]
                previousSegmentY = previousY[i - 1]

            nextSegmentX = previousX[i + 1]
            nextSegmentY = previousY[i + 1]

            if (previousSegmentY == nextSegmentY):
                tail.shape("tail_straight_horizontal.gif")
                tail.stamp()
            elif (previousSegmentX == nextSegmentX):
                tail.shape("tail_straight_vertical.gif")
                tail.stamp()
            elif(nextSegmentX > currentSegmentX):
                if (previousSegmentY < nextSegmentY):
                    tail.shape("tail_turn_4.gif")
                    tail.stamp()
                else:
                    tail.shape("tail_turn_1.gif")
                    tail.stamp()
            elif(nextSegmentX < currentSegmentX):
                if (previousSegmentY < nextSegmentY):
                    tail.shape("tail_turn_3.gif")
                    tail.stamp()
                else:
                    tail.shape("tail_turn_2.gif")
                    tail.stamp()
            elif(nextSegmentY > currentSegmentY):
                if (previousSegmentX < nextSegmentX):
                    tail.shape("tail_turn_2.gif")
                    tail.stamp()
                else:
                    tail.shape("tail_turn_1.gif")
                    tail.stamp()
            elif(nextSegmentY < currentSegmentY):
                if (previousSegmentX < nextSegmentX):
                    tail.shape("tail_turn_3.gif")
                    tail.stamp()
                else:
                    tail.shape("tail_turn_4.gif")
                    tail.stamp()
            else:
                tail.shape("square")
                tail.stamp()


    #Eat apple code
    if (x == appleX and y == appleY):
        score = score + 1
        tailLength = tailLength + 1
        moveApple()
        printScore()

    #Draw apple code
    apple.setposition(appleX * step, appleY * step)
    apple.stamp()


    update()
    sleep(0.05)




# Once you lose, close the game after 5 seconds. 
sleep(2)
bye()