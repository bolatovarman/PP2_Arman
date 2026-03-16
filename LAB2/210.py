n = int(input())
arr = list(map(int, input().split()))
arr.sort()  # өсу
arr.reverse()

print(*arr)
