n = int(input())
nums = list(map(int, input().split()))

evens = list(filter(lambda x: x % 2 == 0, nums))

print(len(evens))