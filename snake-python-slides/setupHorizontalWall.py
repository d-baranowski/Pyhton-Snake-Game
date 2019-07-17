
def setupHorizontalWall(startX, endX, y):
    global rocks
    global rocksXList
    global rocksYList
    for i in range(startX, endX + 1):
        rocksXList.append(i)
        rocksYList.append(y)