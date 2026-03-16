s = input()

vowels = "aeiouAEIOU"

print("Yes" if any(ch in vowels for ch in s) else "No")