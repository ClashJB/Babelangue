name = input("What is your name? ")
name = name.strip().lower()

if name == "justin biron":
    print("You're the chosen one")
elif name == "justin":
    last_name = input("What's your last name? ")
    if last_name == "biron":
       print("You're the chosen one")
else:
    print("Fuck off!")