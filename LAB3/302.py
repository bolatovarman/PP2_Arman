def isUsual(num):
    for x in(2,3,5):
        while num % x == 0:
            num = num // x
    if num == 1:
        return True
    else:
        return False
    
num = int(input())

if(isUsual(num)):
    print("Yes")
else:
    print("No")