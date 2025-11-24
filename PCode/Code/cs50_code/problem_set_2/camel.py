camel_variable = input("camelCase:")
snake_case = []

for char in camel_variable:
    if char.islower():
        snake_case.append(char)
    elif char.isupper():
        snake_case.append("_")
        snake_case.append(char.lower())
    else:
        print("Something is wrong")
        break
print("".join(snake_case))