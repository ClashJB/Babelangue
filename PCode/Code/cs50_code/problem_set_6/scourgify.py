import sys
import csv

if len(sys.argv) < 3:
    sys.exit("Too few arguments")
elif len(sys.argv) > 3:
    sys.exit("Too many arguments")

try:
    with open(sys.argv[1], "r") as before:
        with open(sys.argv[2], "w", newline="") as after:
            reader = csv.DictReader(before)
            writer = csv.DictWriter(after, fieldnames=["first", "last", "house"])
            writer.writeheader()
            for row in reader:
                name = row["name"]
                last_name, first_name = name.split(", ")
                writer.writerow({"first": first_name, "last": last_name, "house": row["house"]})
except FileNotFoundError:
    sys.exit(f"Could not read {sys.argv[1]}")