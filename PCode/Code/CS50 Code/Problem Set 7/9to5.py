import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    regualar_expression = re.search(r"([0-9]|1[0-2])(?::([0-5][0-9]))? (AM|PM) to ([0-9]|1[0-2])(?::([0-5][0-9]))? (AM|PM)", s)

    matches = []

    for n in [1,2,3,4,5,6]:
        match = regualar_expression.group(n)
        if match == "PM":
            match = 12
        elif match == "AM":
            match = 0
        elif not match:
            match = 0
        else:
            match = int(match)

        matches.append(match)


    return f"{matches[0] + matches[2]:02}:{matches[1]:02} to {matches[3] + matches[5]:02}:{matches[4]:02}"


if __name__ == "__main__":
    main()

"""
9:00 AM to 5:00 PM
9 AM to 5 PM
9:00 AM to 5 PM
9 AM to 5:00 PM
"""