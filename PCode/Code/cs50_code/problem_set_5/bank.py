def main():
    print(f"Output: ${value(input("Greeting: "))}")

def value(greeting):
    if greeting.strip().lower() == "hello":
        return 0
    elif greeting.strip().startswith(("H", "h")):
        return 20
    else:
        return 100


# my mother bakes cakes everyday
if __name__ == "__main__":
    main()