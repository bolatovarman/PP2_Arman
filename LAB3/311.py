class Pair:
    def __init__(self, a , b):
        self.a = a
        self.b = b
    
    def add(self , another_Pair):
        return f"{self.a+another_Pair.a} {self.b + another_Pair.b}"
    
a1 , b1 , a2 , b2 = map(int,input().split())
p1 = Pair(a1 , b1)
p2 = Pair(a2 , b2)

print("Result:", p1.add(p2))