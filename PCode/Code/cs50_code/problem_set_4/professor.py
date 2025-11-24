import random


def main():
    level = get_level()
    n = 10
    score = 0
    while n != 0:
        x = generate_integer(level)
        y = generate_integer(level)

        for i in range(4):
            try:
                if i == 3:
                    print(f"{x} + {y} = {x + y}")
                else:
                    answer = int(input(f"{x} + {y} = "))
                    if answer == x + y:
                        score += 1
                        n -= 1
                        break
                    elif answer != x + y:
                        print("EEE")
            except ValueError:
                print("EEE")
    print(f"Score: {score}/10")
                              
def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if 0 < level < 4:
                return level
            else:
                raise ValueError
        except ValueError:
            pass

def generate_integer(level):
    if level == 1:
        return random.randrange(9)
    elif level == 2:
        return random.randrange(99)
    else:
        return random.randrange(999)


if __name__ == "__main__":
    main()