import sys

lines = []
n_lines = 0

try:
    if sys.argv[1].endswith(".py"):
        filename = sys.argv[1]
    else:
        sys.exit()
except IndexError:
    sys.exit()


with open(filename) as file:
    for line in file:
        if line.lstrip().startswith("#"):
            pass
        elif line:
            n_lines += 1
        else:
            pass
print(n_lines)