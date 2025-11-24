xyz = input("Expression:").split(" ")
x = int(xyz[0])
y = xyz[1]
z = int(xyz[2])

if y == "+":
    answer = (x + z)
elif y == "-":
    answer = (x - z)
elif y == "*":
    answer = (x * z)
elif y == "/":
    answer = (x / z)
else:
    print("syntax error")

answer = (float(answer))

print(round(answer, 1))
