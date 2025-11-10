vowels = ("a","e","i","o","u")

def main():
    print(f"Output: {shorten(input("Input: "))}")

def shorten(word):
    output = []
    for char in word:
        if char.lower() not in vowels:
            output.append(char)

    output = ("".join(output))
    return output.strip()


if __name__ == "__main__":
    main()