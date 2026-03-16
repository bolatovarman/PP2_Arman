n = int(input())
words = input().split()

result = [f"{i}:{word}" for i, word in enumerate(words)]
print(" ".join(result))