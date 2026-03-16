n = int(input())
degree = 0

while pow(2 , degree) <= n:
    if pow(2,degree) == n:
        print("YES")
        break
    degree += 1
else:
    print("NO")