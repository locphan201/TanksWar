import math

class Shot:
    def __init__(self, init_x, init_y, x, y):
        self.x = init_x
        self.y = init_y
        self.speed = 7
        ratio = self.speed / (((y - init_y)**2 + (x - init_x)**2)**0.5)
        self.x_speed = (x - init_x) * ratio
        self.y_speed = (y - init_y) * ratio
        self.angl = math.degrees(math.atan2(self.x_speed, self.y_speed)) +180
        
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
    def angle(self):
        return self.angl