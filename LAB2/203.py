n = int(input())
sum = 0
arr = []

arr.extend(map(int, input().split()))

for i in arr:
    sum += i     
        
print(sum)