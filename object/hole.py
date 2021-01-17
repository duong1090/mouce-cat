class Hole:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def checkIn(self, obj):
        checkLeft = obj.x > self.x
        checkRight = obj.x < (self.x + self.width)
        checkTop = obj.y > self.y
        checkBottom = obj.y < (self.y + self.height)
        if (checkLeft and checkRight and checkTop and checkBottom):
            return True
        return False
