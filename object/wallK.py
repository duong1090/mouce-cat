class WallK:
    def __init__(self, x, y, width, height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def checkTouching(self, animal):

        checkRight = (animal.x + animal.width) > self.x
        checkLeft = animal.x < (self.x + self.width)
        checkTop = (animal.y + animal.height) > self.y
        checkBottom = animal.y < (self.y + self.height)


        if checkRight and checkLeft and checkTop and checkBottom:
            return True
        else:
            return False
