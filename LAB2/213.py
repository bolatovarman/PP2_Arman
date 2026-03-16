n = int(input())
isPrime = True

for i in range(2, int(pow(n , 0.5))):
    if n % i == 0:
        isPrime = False
        break
    
if isPrime == True:
    print("Yes")
else:
    print("No")