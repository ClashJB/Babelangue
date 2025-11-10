import csv
from datetime import datetime, timedelta
import pandas

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


print(datetime.now())


class Flashcard:
    def __init__(self, row):
        self.row = row  # e.g. {"EN": "house", "FR": "maison"}
        self.box = 1

class Deck:
    def __init__(self, csv_file):
        self.cards = self.load_from_csv(csv_file)
        self.csv_file = csv_file

    def load_from_csv(self, csv_file):
        with open(csv_file, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return [Flashcard(row) for row in reader]

        
    def deck_information(self, fieldnames, next_review):
        n_cards = 0
        n_due = 0
        for card in self.cards:
            try:
                if card.row["last_review"]:
                   last_review = pandas.to_datetime(card.row["last_review"])
            except KeyError:
                card.row["last_review"] = datetime(1069, 4, 2, 0, 34, 12)
            try:
                if card.row["next_review"]:
                    next_review = pandas.to_datetime(card.row["next_review"])
            except KeyError:
                card.row["next_review"] = datetime.today()
            try:
                if not card.row["box"]:
                    pass
            except KeyError:
                card.row["box"] = 1

            n_cards += 1
            if datetime.now() >= next_review:
                n_due += 1
        return n_cards, n_due
                



    def train(self, from_lang, to_lang):
        langs = self.get_langs()
        fieldnames = ["next_review", "last_review", "box"] + langs
        with open (self.csv_file, "w", newline="", encoding="utf-8") as deck:
            writer = csv.DictWriter(deck, fieldnames)
            writer.writeheader()
        for card in self.cards:
            try:
                if card.row["last_review"]:
                   last_review = pandas.to_datetime(card.row["last_review"])
            except KeyError:
                card.row["last_review"] = datetime(1069, 4, 2, 0, 34, 12)
            try:
                if card.row["next_review"]:
                    next_review = pandas.to_datetime(card.row["next_review"])
            except KeyError:
                card.row["next_review"] = datetime.today()
                next_review = datetime.today()
            try:
                if not card.row["box"]:
                    pass
            except KeyError:
                card.row["box"] = 1

            if not datetime.now() >= next_review:
                with open (self.csv_file, "a", newline="", encoding="utf-8") as deck:
                    writer = csv.DictWriter(deck, fieldnames)
                    print(card.row)
                    writer.writerow(card.row)
            else:
                q = card.row[from_lang]
                a = card.row[to_lang]
                print(f"{from_lang}: {q}")
                if not input("Show other side: (Press Enter)"):
                    print(f"answer: {a}")
                guess = input("Did you know it? ([Y]es or [N]o?)").strip().lower()
                if guess.lower() == "y":
                    print("Good job!")
                    card.row["box"] = int(card.row["box"]) + 1
                else:
                    print("Don't worry you'll get it next time.")
                    card.row["box"] = 1

                # schedule next review
                interval_days = {1: 1, 2: 3, 3: 7, 4: 14}.get(card.box, 30)
                card.row["next_review"] = datetime.today() + timedelta(days=interval_days)
                
                with open (self.csv_file, "a", newline="", encoding="utf-8") as deck:
                    writer = csv.DictWriter(deck, fieldnames)
                    writer.writerow(card.row)
                
                print(card.row)
  
  
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
    from_lang = "EN-US"
    #from_lang = input("from which language do you want to learn? ")
    to_lang = "DE"
    #to_lang = input("What will be your answer language? ")

    deck = Deck(csv_file)

    deck.train(from_lang= from_lang, to_lang= to_lang)

main()
    

