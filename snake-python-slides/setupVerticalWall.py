def setupVerticalWall(startY, endY, x):
    global rocks
    global rocksXList
    global rocksYList
    for i in range(startY, endY + 1):
        rocksYList.append(i)
        rocksXList.append(x)