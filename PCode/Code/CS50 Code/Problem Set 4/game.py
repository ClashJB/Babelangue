from random import randint

while True:
    try:
        n = int(input("Level: "))
        if n > 1:
            break
    except ValueError:
        pass

r = randint(1, n)

while True:
    try:
        g = int(input("Guess: "))
    except ValueError:
        pass
        
    if g > 0:
        if g < r:
            print("Too Small!")
        elif g > r:
            print("Too Large!")
        else:
            print("Just right!")
            break
    else:
        pass