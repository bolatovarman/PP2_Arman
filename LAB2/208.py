n = int(input())
degree = 0

while pow(2 , degree) <= n:
    print(pow(2 , degree) , end=" ")
    degree += 1