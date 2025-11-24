while True:
    fraction = input("Fraction: ").strip()
    fraction = list(fraction)

    y_started = False
    x = []
    y = []
    for char in fraction:
        if not y_started:
            if char.isdigit():
                x.append(char)
            elif char == "/":
                y_started = True
            else:
                print("Please input using the following format: X/Y")
                break
        elif y_started:
            if char.isdigit():
                y.append(char)
            else:
                print("Please input using the following format: X/Y")
                break
    x = "".join(x)
    y = "".join(y)
    x = int(x)
    y = int(y)

    if 0 <= x <= y:
        break
    else:
        print("Please input using the following format: X/Y")

percentage = x / y * 100

if 0 <= percentage <= 1:
    print("E")
elif percentage >= 99:
    print("F")
else:
    print(f"{int(percentage)}%")