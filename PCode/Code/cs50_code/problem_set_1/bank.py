greeting = input("Greeting:")

if greeting.strip().startswith(("Hello", "hello")):
    print("$0")
elif greeting.strip().startswith(("H", "h")):
    print("$20")
else:
    print("$100")