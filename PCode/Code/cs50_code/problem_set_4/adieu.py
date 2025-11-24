import inflect

p = inflect.engine()

names = []
output = "Adieu, adieu, to "

while True:
    try:
        names.append(input("Name: "))
    except (EOFError):
        break

output += p.join(names)
print(output)