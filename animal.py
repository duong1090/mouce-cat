class Animal:
    def __init__(self, x, y, width, height, speed, image, isMoving, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = image
        self.isMoving = isMoving
        self.direction = direction

    def move(self):
        if (self.direction == 'RIGHT'):
            self.x += self.speed
        elif (self.direction == 'LEFT'):
            self.x -= self.speed
        elif (self.direction == 'UP'):
            self.y -= self.speed
        elif (self.direction == 'DOWN'):
            self.y += self.speed

    def moveTo(self, position):
        self.x = position.x
        self.y = position.y
