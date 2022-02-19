import math

class Turret:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        
    def update_pos(self, x, y):
        self.x = x
        self.y = y
        
    def update_angle(self, mouse_x, mouse_y):
        x = 375 - mouse_x
        y = 375 - mouse_y
        self.angle = math.degrees(math.atan2(x, y))

class Tank:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.turret = Turret(x+25, y+25)
         
    def x(self):
        return self.x
    
    def y(self):
        return self.y
    
    def index(self):
        return self.index
    
    def update_pos(self, x, y):
        self.x = x
        self.y = y
        self.turret.update_pos(x+25, y+25)
        
    def update_turret(self, mouse_x, mouse_y):
        self.turret.update_angle(mouse_x, mouse_y)