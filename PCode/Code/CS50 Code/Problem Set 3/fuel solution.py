while True:
    fraction = input("Fraction: ").strip()
    try:
        x_str, y_str = fraction.split("/")
        x = int(x_str)
        y = int(y_str)
        if y == 0:
            print("Denominator cannot be zero. Please input using the following format: X/Y")
            continue
        if 0 <= x <= y:
            break
        else:
            print("Please input using the following format: X/Y")
    except (ValueError, ZeroDivisionError):
        print("Please input using the following format: X/Y")

percentage = x / y * 100

if 0 <= percentage <= 1:
    print("E")
elif percentage >= 99:
    print("F")
else:
    print(f"{int(percentage)}%")