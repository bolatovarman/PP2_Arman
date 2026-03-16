import math
class Point:
    def __init__(self,a , b):
        self.x = a
        self.y = b 
    def show(self):
        print(f"({self.x}, {self.y})")
    
    def move(self , new_x , new_y):
        self.x = new_x
        self.y = new_y
    def dist(self , other_point):
        return math.sqrt(pow(other_point.x - self.x , 2) + pow(other_point.y - self.y , 2))     

x1 , y1 = map(int , input().split()) 
x2 , y2 = map(int , input().split())
x3 , y3 = map(int , input().split())   

p1 = Point(x1 , y1)
p1.show()
p1.move(x2 , y2)
p1.show()
p2 = Point(x3 , y3)
print(f"{p1.dist(p2):.2f}")