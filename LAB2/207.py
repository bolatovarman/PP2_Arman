n = int(input())
arr = list(map(int,input().split()))
maximum = arr[0]
maximum_position = 1
for i in range(1 , n):
    if arr[i] > maximum:
        maximum = arr[i]
        maximum_position = i + 1
        
print(maximum_position)
