import sys
from tabulate import tabulate
import csv

menu_table = []

try:
    if sys.argv[1].strip().endswith(".csv"):
        filename = sys.argv[1].strip()
    else:
        sys.exit()
except IndexError:
    sys.exit()

with open(filename) as menu:
    menureader = csv.reader(menu)
    for row in menureader:
        menu_table.append(row)
    print(tabulate(menu_table, tablefmt="grid"))