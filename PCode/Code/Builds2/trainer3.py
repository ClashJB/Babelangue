import csv
from datetime import datetime, timedelta
import pandas
import msvcrt

target_langues = {
    "czech": "CS",
    "danish": "DA",
    "german": "DE",
    "british english": "EN-GB",
    "english": "EN-US",
    "spanish": "ES",
    "latino spanish": "ES-419",
    "estonian": "ET",
    "finnish": "FI",
    "french": "FR",
    "hungarian": "HU",
    "indonesian": "ID",
    "italian": "IT",
    "lithuanian": "LT",
    "latvian": "LV",
    "norwegian Bokmål": "NB",
    "dutch": "NL",
    "polish": "PL",
    "brazilian portuguese": "PT-BR",
    "portuguese": "PT-PT",
    "romanian": "RO",
    "slovak": "SK",
    "slovenian": "SL",
    "swedish": "SV",
    "turkish": "TR",
    "vietnamese": "VI"
}


print(datetime.today())


class Flashcard:
    def __init__(self, row):
        self.row = row
        self.box = self.get_box()
        self.next_review = self.get_next_review()
        self.last_review = self.get_last_review()

    def get_box(self):
        try:
            if self.row["box"]:
                return int(self.row["box"])
        except KeyError:
            return 1

    def get_next_review(self):
        try:
            if self.row["next_review"]:
                return pandas.to_datetime(self.row["next_review"])
        except KeyError:
            return datetime.today()

    def get_last_review(self):
        try:
            if self.row["last_review"]:
                return pandas.to_datetime(self.row["last_review"])
        except KeyError:
            return datetime(1767, 1, 1)
        
    def save_row(self):
        self.row["box"] = self.box
        self.row["next_review"] = self.next_review
        self.row["last_review"] = self.last_review
        return self.row

class Deck:
    def __init__(self, csv_file):
        self.cards = self.load_from_csv(csv_file)
        self.csv_file = csv_file
        self.langs = self.get_langs()
        self.fieldnames = ["next_review", "last_review", "box"] + self.langs
        self.n_cards, self.n_due = self.deck_information()


    def load_from_csv(self, csv_file):
        with open(csv_file, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return [Flashcard(row) for row in reader]


    def deck_information(self):
        n_cards = 0
        n_due = 0
        for card in self.cards:
            n_cards += 1
            if datetime.today() >= card.next_review:
                n_due += 1
        return n_cards, n_due
            

    def train(self, from_langs, to_langs):
        with open (self.csv_file, "w", newline="", encoding="utf-8") as deck:
            writer = csv.DictWriter(deck, self.fieldnames)
            writer.writeheader()
        exit_mode = False
        for card in self.cards:
            if not datetime.today() >= card.next_review or exit_mode:
                with open (self.csv_file, "a", newline="", encoding="utf-8") as deck:
                    writer = csv.DictWriter(deck, self.fieldnames)
                    writer.writerow(card.save_row())
            else:
                q = []
                a = []
                for lang in from_langs:
                    q.append(f"{lang}: {card.row[lang]}")
                for lang in to_langs:
                    a.append(f"{lang}: {card.row[lang]}")
                
                try:
                    print(f"Front Side: {"   |   ".join(q)}")
                    msvcrt.getch()
                    print(f" Back Side: {"   |   ".join(a)}")
                    guess = msvcrt.getch()
                    if guess == b"x":
                        raise EOFError
            
                    if guess == b" ":
                        print("Good job!")
                        card.box += 1
                    else:
                        print("Don't worry you'll get it next time.")
                        card.box = 1
                except EOFError:
                    exit_mode = True
                    print("User exists program, but files are saved.")
                # schedule next review
                interval_days = {1: 1, 2: 3, 3: 7, 4: 14}.get(card.box, 30)
                card.next_review = datetime.today() + timedelta(days=interval_days)
                
                with open (self.csv_file, "a", newline="", encoding="utf-8") as deck:
                    writer = csv.DictWriter(deck, self.fieldnames)
                    writer.writerow(card.save_row())
                
  
  
    def get_langs(self):
        with open(self.csv_file , mode="r", newline="") as file:
            reader = csv.DictReader(file)
            langs = []
            for name in reader.fieldnames:
                if name in target_langues.values():
                    langs.append(name)
            return langs




def main():
    csv_file = "Vocabulary1.csv"
    #csv_file = input("what is the name of your file? ")
    deck = Deck(csv_file)

    print("Available languages:")
    langs = deck.get_langs()
    for lang in langs:
        print(lang)

    from_langs = []
    to_langs = []

    while True:
        if (len(langs) - len(from_langs)) == 1:
            break
        from_lang = input("from which language(s) do you want to learn? (end with Enter) ").upper()
        if not from_lang and len(from_langs) >= 1:
            break
        elif from_lang in langs:
            from_langs.append(from_lang)
        else:
            print("Please try again.")

    while True:
        if (len(langs) - len(from_langs) - len(to_langs)) == 1:
            for lang in langs:
                if not lang in from_langs and not lang in to_langs:
                    to_langs.append(lang)
                    stop = True
                    break
            if stop:
                break
        to_lang = input("What will be your answer language? (end with Enter) ").upper()
        if not to_lang and len(to_langs) >= 1:
            break
        elif to_lang in langs and not to_lang in from_langs:
            to_langs.append(to_lang)
        else:
            print("Please try again.")

    print(f"Question language(s): {", ".join(from_langs)}")
    print(f"Answer language(s): {", ".join(to_langs)}")

    deck.train(from_langs= from_langs, to_langs= to_langs)

main()
    

