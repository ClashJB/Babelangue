import pyfiglet
import sys

while True:
    if 1 < len(sys.argv) < 3:
        print()
    else:
        break
        
if len(sys.argv) == 1:
    f = pyfiglet.figlet_format(input("Input: "))
    print(f)


if len(sys.argv) == 3:
    f = pyfiglet.figlet_format(input("Input: "), font=sys.argv[2])
    print(f)