import sys

readline = sys.stdin.readline
write = sys.stdout.write

n = int(readline())
db = {}

for _ in range(n):
    parts = readline().rstrip('\n').split(' ', 2)
    if parts[0] == 'set':
        key = parts[1]
        value = parts[2] if len(parts) > 2 else ''
        db[key] = value
    else:  # get
        key = parts[1]
        if key in db:
            write(db[key] + "\n")
        else:
            write(f"KE: no key {key} found in the document\n")
