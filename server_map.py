from tank import Tank
from shot import Shot

class Map:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.tanks = []
        self.shots = []
        
    def add_tank(self, tank):
        self.tanks.append(tank)
        
    def add_shot(self, shot):
        self.shots.append(shot)
        
    def update_tank(self, index, x, y):
        self.tanks[index].x += x
        self.tanks[index].y += y
        
    def update_shots(self):
        for shot in self.shots:
            shot.move()
            if 0 > shot.x or shot.x > 1574 or 0 > shot.y or shot.y > 1574:
                self.shots.remove(shot)
                
    def tank_pos(self, index):
        return self.tanks[index].x, self.tanks[index].y
    
    def get_all_shots(self):
        return self.shots