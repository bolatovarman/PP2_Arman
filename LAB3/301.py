a = input()
isValid = True

for x in a:
    if int(x) % 2 != 0:
        isValid = False
        
if isValid:
    print("Valid")
else:
    print("Not valid")