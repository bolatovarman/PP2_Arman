n = int(input())
arr = list(map(int,input().split()))
numbers = set()
for x in arr:
    if x in numbers:
        print("NO")
    else:
        print("YES")
        numbers.add(x)