items = {}

try:
    while True:
        key = input().lower()
        if key in items:
            items[key] += 1
        else:
            items[key] = 1
    
except (EOFError, ValueError):
    pass


for item in sorted(items):
    print(f"{items[item]} {(item.upper())}")