class Ball:
    def __init__(self):
        self.x = 250 
        self.y = 250
        self.r = 25
        self.step = 20
    
    def move_left(self):
        if self.x > 44:
            self.x -= self.step
    def move_right(self):
        if self.x < 456:
            self.x += self.step
    def move_up(self):
        if self.y > 44:
            self.y -= self.step
    def move_down(self):
        if self.y < 456:
            self.y += self.step
