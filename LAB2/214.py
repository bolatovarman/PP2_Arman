numbers = {}
n = int(input())
arr = list(map(int, input().split()))

for x in arr:
    if x not in numbers:
        numbers[x] = 1
    else:
        numbers[x] += 1
        
max_frequency = max(numbers.values())
arr = []
for key in numbers:
    if max_frequency == numbers[key]:
        arr.append(key)

print(min(arr))