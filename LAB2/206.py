n = int(input())
arr = list(map(int,input().split()))

# maximum = max(arr)
maximum = arr[0]
for i in range(1 , n):
    if arr[i] > maximum:
        maximum = arr[i]
        
print(maximum)
