n = int(input())
words = {}
counter = 1
for i in range(n):
    x = input()
    if x not in words:
        words[x] = counter
    counter += 1
    
for key in sorted(words):
    print(f"{key} {words[key]}")
    