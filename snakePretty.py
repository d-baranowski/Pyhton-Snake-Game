from turtle import * # Import entire turtle module responsible for drawing graphics 
from random import randint # Import randint function which generates random numbers 
from time import sleep # Import sleep function which makes the program wait for a given ammount of seconds

#Game engine setup
delay(0)
tracer(0, 0)
step = 22
screensize(35 * step, 35 * step)

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

tailLength = 10
previousY = [0,0,0,0,0,0,0,0,0,0]
previousX = [0,0,0,0,0,0,0,0,0,0]

#Head pen setup 
head = Turtle()
head.penup()
head.shape('head_right.gif')
head.speed(0)

#Tail pen setup
tail = Turtle()
tail.penup()
tail.color('blue')
tail.shape('square')
tail.speed(0)

#rocks pen setup
rocks = Turtle()
rocks.penup()
rocks.color('brown')
rocks.shape('rock.gif')
rocks.speed(0)
rocks.hideturtle()
rocksXList = []
rocksYList = []

#Apple pen setup
apple = Turtle()
apple.penup()
apple.shape('apple.gif')
apple.color('red')
apple.hideturtle()

#Apple Variables
appleX = 10
appleY = 10


#Lose message pen setup
hideturtle()
penup()
color("red")

# Node to use with A* Path Finding algorithm. It represents a point on the grid.
class Node:
    # Constructor
    def __init__(self, x,y, parent, previousX, previousY):
        self.x = x
        self.y = y
        self.previousX = list(previousX)
        self.previousY = list(previousY)

        # Storing parent allows to create a chain of nodes that can be interpreted to become a path
        if (parent == None):
            self.parent = self
        else:
            self.parent = parent
            global tailLength
            self.previousX.insert(0, self.parent.x)
            self.previousX = self.previousX[:tailLength]
            self.previousY.insert(0, self.parent.y)
            self.previousY = self.previousY[:tailLength]

    # Overridden equivalence to use with __contains__
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    # Calculates straight line distance between 2 nodes ignoring any obstacles (tail or rocks)
    def getDistance(self, fromNode):
        return abs(self.x - fromNode.x) + abs(self.y - fromNode.y)

    # G score is the distance from start node. It is equal to parent g score + 1
    def setGScore(self, g):
        self.distanceFromStart = g

    # F score is equal to distance from end node + current G score.
    def setFScore(self, endNode):
        self.distanceFromEnd = self.getDistance(endNode)
        self.f = self.distanceFromStart + self.distanceFromEnd

    # Returns nodes that are adjacent to this node that don't contain rocks or tail.
    def getReachableNodes(self):
        # Above this node
        up = Node(self.x, self.y + 1, self, self.previousX, self.previousY)
        # Below this node
        down = Node(self.x, self.y - 1, self, self.previousX, self.previousY)
        # Etc.
        left = Node(self.x - 1, self.y, self, self.previousX, self.previousY)
        right = Node(self.x + 1, self.y, self, self.previousX, self.previousY)
        # Array of adjacent nodes that aren't tail or rock
        reachable = [up, down, left, right]

        # Get global tail positions
        global tailLength

        # Array of nodes that will be removed from reachable array.
        remove = []

        # For every piece of snake tail...
        for i in range(tailLength):
            # Check if any of the reachable nodes...
            for j in range(len(reachable)):
                # is on the same position as the snake tail segment...
                if (reachable[j].x == self.previousX[i] and reachable[j].y == self.previousY[i]):
                    # If it is in the same position as snake tail segment and is not marked to be removed...
                    if not(remove.__contains__(reachable[j])):
                        # Mark it to be removed
                        remove.append(reachable[j])

        # Remove reachable nodes that are marked to be removed.
        for removeNode in remove:
            reachable.remove(removeNode)

        # Get global rock positions
        global rocksXList, rocksYList

        # Reset the list of Nodes that will be removed from reachable array.
        remove = []

        # For every rock on the board...
        for i in range(len(rocksXList)):
            # Check every reachable node...
            for j in range(len(reachable)):
                # If its on the same position as the rock...
                if (reachable[j].x == rocksXList[i] and reachable[j].y == rocksYList[i]):
                    # Etc.
                    if not(remove.__contains__(reachable[j])):
                        remove.append(reachable[j])

        # Remove reachable elements that were on the same positions as rocks.
        for removeNode in remove:
            reachable.remove(removeNode)

        # Return a list of nodes that can be reached from this node that are not rocks or tail.
        return reachable

# Returns the node that is closest to the end node from the list of possible nodes.
def findBestNodeFrom(openNodes):
    # Contains a dictionary of nodes by their F score which is equal to their distance from start + their distance from end.
    nodesByF  = {}

    # If there are any open nodes left...
    if len(openNodes) > 0:
        # Arbitrary high number. This variable will store the minimum value of f amongst all the open nodes.
        minF = 999999

        for node in openNodes:
            # Get current node f value.
            f = node.distanceFromStart + node.distanceFromEnd
            # If its less than the current minimum f value
            if (f < minF):
                # The current value becomes the new minimum.
                minF = f

            # If there are no nodes that have this f value
            if (not(nodesByF.has_key(f))):
                # Create a new list of nodes that have this f value and store it in the dictionary for easy retrieval.
                nodesByF[f] = [node]
            else:
                # If there are already nodes with this value in the dictionary add this node to the existing list.
                nodesByF[f].append(node)

        # If there is more than one node with the minimum f value, pick the node that is closest to the end node.
        if len(nodesByF[minF]) > 1:
            # Arbitrary high number.
            # This variable will store the minimum value of h amongst all the nodes with minimum value of f.
            minH = 99999
            # Arbitrary node from the list.
            # This variable will store the node with the best h value, which is its distance from the end node.
            minHNode = nodesByF[minF][0]
            # For every node amongst nodes with the best F value
            for node in nodesByF[minF]:
                # Get its distance from the end node. (The apple position)
                h = node.distanceFromEnd
                # If its smallest than the current minimum it becomes the minimum.
                if (minH > h):
                    minH = h
                    minHNode = node
            # Return the node with smallest H value from all the nodes with smallest F value.
            return minHNode
        else:
            # If there is only one node with the best F value, return it instead.
            return nodesByF[minF][0]
    # If there are no open nodes left return none to signal that there doesn't exist a a path to the apple currently.
    return None

# Find the node that contains the apple using A* https://www.youtube.com/watch?v=-L-WgKMFuhE&t=211s
alternate = 0;

def getNodeChain():
    global previousX, previousY, score, alternate
    # Start node represents the snake head
    startNode = Node(x,y, None, previousX, previousY)

    if (score > 50 and score < 100):
        alternate = (alternate + 1) % 2
    if (score > 100 and score < 150):
        alternate = (alternate + 1) % 3
    if (score > 150):
        alternate = (alternate + 1) % 4
    if (score > 200):
        alternate = (alternate + 1) % 5

    if (alternate == 0):
        # End node represents the apple
        endNode = Node(appleX, appleY, None,previousX, previousY)
    elif(alternate == 1):
        endNode = Node(-18, -15, None, previousX, previousY)
    elif(alternate == 2):
        endNode = Node(-18, 15, None, previousX, previousY)
    elif(alternate == 3):
        endNode = Node(18, -15, None, previousX, previousY)
    elif(alternate == 4):
        endNode = Node(18, 15, None, previousX, previousY)


    # Start node is 0 squares away from itself.
    startNode.setGScore(0)
    # Calculate start nodes distance from the end node.
    startNode.setFScore(endNode)

    # Nodes that possibly can be our next move.
    openNodes = [startNode]

    # Nodes that we have checked already.
    closedNodes = []

    # Current node.
    activeNode = startNode
    nodeCount  = 1
    # While there are open nodes left.
    while len(openNodes) > 0:
        # If the activeNode is at the same position as the endNode, we have found our path!
        if ((activeNode.x == endNode.x and activeNode.y == endNode.y)):
            return activeNode

        # Mark current node as explored.
        openNodes.remove(activeNode)
        closedNodes.append(activeNode)

        # For every node that we can move to from the current node...
        for node in activeNode.getReachableNodes():
            # If its not explored yet.
            if closedNodes.__contains__(node):
                continue

            # Set its distance from start node to be one greater than the current node.
            node.setGScore(activeNode.distanceFromStart + 1)
            # Calculate its distance from the end node.
            node.setFScore(endNode)

            # Add it to the nodes that we can potentially explore.
            if not(openNodes.__contains__(node)):
                openNodes.append(node)

        # Find the best node (one closest to the end node) among the potential nodes.
        newActive = findBestNodeFrom(openNodes)
        nodeCount = nodeCount + 1

        if (nodeCount > 150):
            return activeNode
        

        # If there are no more potential moves left return the path we discovered so far, so the snake moves a bit
        # and potentially move its tail enough to make it possible to reach the apple.
        if (newActive == None ):
            return startNode
        # Make it the next active node and start from the top.
        activeNode = newActive

    return activeNode

# Get a path that we can understand from the node.
def getPath(activeNode,path):
    # Node from which we arrived to the activeNode
    parent = activeNode.parent

    # If the activeNode is the start node...
    if activeNode.distanceFromStart > 0:
        # ...otherwise, add new step to the path.
        # If previous node's(parent's) x is less than this node x it means that we need to go right
        # to reach current node from the parent
        if (parent.x < activeNode.x):
            path.append('right')
        # Otherwise we need to go left.
        elif (parent.x > activeNode.x):
            path.append('left')
        # Etc.
        elif (parent.y > activeNode.y):
            path.append('down')
        elif (parent.y < activeNode.y):
            path.append('up')
        getPath(parent, path)

    # ...Return the path...
    # The path will be backwards, since we start from the apple and go all the way back to snake head, so we need to
    # reverse it.
    return list(reversed(path))


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

onAutoPilot = True
def toggleAutoPilot():
    global onAutoPilot
    onAutoPilot = not onAutoPilot

#Path Finding
currentPath = getPath(getNodeChain(), [])
pathStep = 0

#Bind movement functions to keyboard keys    
onkey(moveUp,'Up')
onkey(moveDown,'Down')
onkey(moveLeft,'Left')
onkey(moveRight,'Right')
onkey(toggleAutoPilot, 'a')
listen()

#Setup our rocks
setupHorizontalWall(-21,21,18)
setupHorizontalWall(-21,21,-18)
setupVerticalWall(-18,18,21)
setupVerticalWall(-18,18,-21)

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

    if (onAutoPilot):
        #Change direction according to path
        if not(pathStep < (len(currentPath))):
            currentPath = getPath(getNodeChain(), [])
            pathStep = 0

        if len(currentPath) > 0:
            if (currentPath[pathStep] == 'up'):
                moveUp()
            elif (currentPath[pathStep] == 'down'):
                moveDown()
            elif (currentPath[pathStep] == 'left'):
                moveLeft()
            elif (currentPath[pathStep] == 'right'):
                moveRight()

    #Calculate new x and y positions
    x = x + xChange
    y = y + yChange

    #Move head pen to new x and y position
    head.setposition(x * step,y * step)

    if (onAutoPilot):
        pathStep = pathStep + 1

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
        currentPath = getPath(getNodeChain(), [])
        pathStep = 0
        
    #Draw apple code
    apple.setposition(appleX * step, appleY * step)
    apple.stamp()
        

    update()
    if not onAutoPilot:
        sleep(0.1)

# Once you lose, close the game after 5 seconds. 
sleep(5)
bye()
