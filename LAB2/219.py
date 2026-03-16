n = int(input())
movies = {}
for i in range(n):
    movie, amount = input().split()
    amount = int(amount)
    if movie not in movies:
        movies[movie] = amount
    else:
        movies[movie] += amount
        
for key in sorted(movies):
    print(f"{key} {movies[key]}")     