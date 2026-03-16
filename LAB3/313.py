import math
def isPrime(num):
    if num == 1:
        return False
    for i in range(2 , int(math.sqrt(num)) + 1):
        if num % i == 0 :
            return False
    return True

isPrime_byLambda = lambda num: num > 1 and all(num % i != 0 for i in range(2 , int(math.sqrt(num)) + 1))

numbers = list(map(int , input().split()))
filtered_numbers_obj = filter(isPrime_byLambda, numbers)
filtered_numbers = list(filtered_numbers_obj)
if len(filtered_numbers) == 0:
    print("No primes")
else:
    print(*filtered_numbers)