n = int(input())
keys = input().split()
values = input().split()

d = dict(zip(keys, values))

q = input()

print(d.get(q, "Not found"))