def main():
    user_fraction = input("Fraction: ")
    fraction_percentage = convert(user_fraction)
    gauge_ouput = gauge(fraction_percentage)
    print(gauge_ouput)

def convert(fraction):
    try:
        if not len(fraction.split("/")) == 2:
            raise ValueError
        else:
            x, y = fraction.split("/")
            x = int(x)
            y = int(y)

        if x > y:
            raise ValueError
        elif y == 0:
            raise ZeroDivisionError
        else:
            return round(x / y * 100)
    except (ValueError, ZeroDivisionError, TypeError):
        print("Invalid Input. With fraction formatted like: X/Y  X has to be smaller than Y and Y can't be 0.")
        return False

def gauge(percentage):
    try:
        if percentage == False:
            raise ValueError
        elif 0 <= percentage <= 1:
            return "E"
        elif 99 <= percentage <= 100:
            return "F"
        elif 1 < percentage < 99:
            return f"{int(percentage)}%"
        else:
            raise ValueError
    except (TypeError, ValueError):
        print("Invalid Input. Percentage has to to be between 0 and 100")
        return False
            

if __name__ == "__main__":
    main()