n = int(input())
nums = list(map(int, input().split()))

result = sorted(set(nums))

print(*result)