input = input("Input: ")
vowels = ("a","e","i","o","u")

output = []

for char in input:
    if char.lower() not in vowels:
        output.append(char)

output = ("".join(output))
print(f"Output: {output}")