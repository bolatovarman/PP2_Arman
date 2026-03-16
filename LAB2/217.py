numbers = {}
n = int(input())
for i in range(n):
    x = input()
    if x in numbers:
        numbers[x] += 1
    else:
        numbers[x] = 1
counter = 0
for key in numbers:
    if numbers[key] == 3:
        counter+=1
        
print(counter)