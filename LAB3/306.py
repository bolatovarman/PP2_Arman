class Shape:
    def area():
        return 0
    
class Rectangle(Shape):
    def __init__(self, a , b):
        self.length = a
        self.width = b
    def area(self):  
        return self.length  *  self.width
    
a , b = map(int, input().split())
r1 = Rectangle(a , b) 
print(r1.area())