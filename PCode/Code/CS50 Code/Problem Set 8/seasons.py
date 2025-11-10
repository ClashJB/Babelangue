from datetime import date, datetime
import inflect

p = inflect.engine()

def main():
    print(9)
    birthday = input("What's your birthday? ")
    birthday = datetime.strptime(birthday, "%Y-%m-%d")
    difference = date.today() - birthday.date()
    minutes = difference.days * 24 * 60
    print(f"You have been on this world for {p.number_to_words(minutes, andword="")} minutes")



...


if __name__ == "__main__":
    main()