class StringHandler:
    def __init__(self): 
        pass 
    def getString(self):
        self.word = input() 
    def printString(self):
        print(self.word.upper())
        
s1 = StringHandler() 
s1.getString() 
s1.printString() 