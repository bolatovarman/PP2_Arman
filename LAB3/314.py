n = int(input())
array = list(map(int,input().split()))
q = int(input())

for i in range(q):
    data = input().split()
    cmd = data[0]
    
    if cmd == "abs":
        array = list(map(lambda current: abs(current) , array))
    elif cmd == "add":
        x = int(data[1])
        array = list(map(lambda current: current + x , array))
    elif cmd == "multiply":
        x = int(data[1])
        array = list(map(lambda current: current * x , array))
    elif cmd == "power":
        x = int(data[1])
        array = list(map(lambda current: current ** x  , array))    
    
print(*array)    
        
