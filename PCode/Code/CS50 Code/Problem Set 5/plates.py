def main():
    plate = input("Plate: ")

    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    if not (2 <= len(s) <= 6):
        return False
    if not s[0].isalpha():
        return False
    if not s[1].isalpha():
        return False

    number_started = False
    for char in s:
        if not number_started:
            if char.isdigit():
                number_started = True
                if char == "0":
                    return False
        if number_started:
            if char.isalpha():
                return False
    return True


if __name__ == "__main__":
    main()