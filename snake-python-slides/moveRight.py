def moveRight():
    global xChange
    global yChange
    global head

    if not (xChange == -1 and yChange == 0):
        head.shape('head_right.gif')
        xChange = 1
        yChange = 0