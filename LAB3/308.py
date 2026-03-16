class Account:
    def __init__(self,b):
        self.balance = b
        
    def withdraw(self,amount):
        if amount > self.balance:
            print("Insufficient Funds")
        else:
            self.balance -= amount
            print(self.balance)
            
balance, draw = map(int , input().split())
a1 = Account(balance)
a1.withdraw(draw)