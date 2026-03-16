n = int(input())
arr = list(map(int , input().split()))

# maximum = max(arr)
# minimum = min(arr)

maximum = arr[0]
minimum = arr[0]

for i in range(n):
    if arr[i] > maximum:
        maximum = arr[i]
    if arr[i] < minimum:
        minimum = arr[i]
        
for i in range(n):
    if arr[i] == maximum:
        arr[i] = minimum
        
print(*arr)