import deepl
import csv
import sys
import pyfiglet
import glob
import pandas
import requests
from datetime import datetime, timedelta

auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
if not auth_key:
    raise ValueError("Missing DeepL API key. Please set DEEPL_API_KEY in your environment.")
deepl_client = deepl.DeepLClient(auth_key)

langs = []
temp_langs = []
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

def startup():
    print(pyfiglet.figlet_format("BABELANGUE", font="chunky"))
    build = sys.argv[0]
    print(f"Build: {build}")
    print("Welcome to BABELANGUE!")

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
            else:
                return 1
        except KeyError:
            return 1

    def get_next_review(self):
        try:
            if self.row["next_review"]:
                return pandas.to_datetime(self.row["next_review"])
            else:
                return datetime(1767, 1, 1)
        except KeyError:
            return datetime.today()

    def get_last_review(self):
        try:
            if self.row["last_review"]:
                return pandas.to_datetime(self.row["last_review"])
            else:
                return datetime(1767, 1, 1)
        except KeyError:
            return datetime(1767, 1, 1)
        
    def save_row(self):
        self.row["box"] = self.box
        self.row["next_review"] = self.next_review
        self.row["last_review"] = self.last_review
        return self.row

class Deck:
    def __init__(self, csv_file, langs=None):
        self.csv_file = csv_file
        if langs:
            self.langs = langs
            self.fieldnames = ["next_review", "last_review", "box"] + self.langs
            self.save()
        else:
            self.langs = self.get_langs()
        self.cards = self.load_from_csv(csv_file)
        self.fieldnames = ["next_review", "last_review", "box"] + self.langs
        self.n_cards, self.n_due = self.learn_information()


    def load_from_csv(self, csv_file):
        with open(csv_file, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return [Flashcard(row) for row in reader]
        

    def get_langs(self):
            with open(self.csv_file , mode="r", newline="") as file:
                reader = csv.DictReader(file)
                langs = []
                for name in reader.fieldnames:
                    if name in target_langues.values():
                        langs.append(name)
                return langs
            
    def learn_information(self):
        n_cards = 0
        n_due = 0
        for card in self.cards:
            n_cards += 1

            if datetime.today() >= card.next_review:
                n_due += 1
        return n_cards, n_due
    
    def print_cards(self):
        for i, card in enumerate(self.cards, start=1):
            print(f"Card {i}:")
            for lang, result in card.row.items():
                if lang in ["next_review", "last_review", "box"]:
                    pass
                else:
                    print(f"    {lang} | {result}")

    
    def save(self):
        with open(self.csv_file, "w", newline="", encoding="utf-8") as deck:
            writer = csv.DictWriter(deck, self.fieldnames)
            writer.writeheader()
            try:
                for card in self.cards:
                    writer.writerow(card.row)
            except AttributeError:
                pass
    
    def train(self, from_langs, to_langs):
        exit_mode = False
        for card in self.cards:
            print(card.box)
            if not datetime.today() >= card.next_review or exit_mode:
                card.save_row()
            else:
                q = []
                a = []
                for lang in from_langs:
                    q.append(f"{lang}: {card.row[lang]}")
                for lang in to_langs:
                    a.append(f"{lang}: {card.row[lang]}")
                
                try:
                    print(f"Front Side: {"   |   ".join(q)}")
                    t_inp = input()
                    if t_inp or not t_inp:
                        print(f" Back Side: {"   |   ".join(a)}")
    
                    guess = input("Did you know it? [Y]es or [No]?").strip().lower()
                    
                    if guess == "y":
                        print("Good job!")
                        card.box += 1
                    elif guess == "x":
                        raise EOFError
                    else:
                        print("Don't worry you'll get it next time.")
                        card.box = 1
                except EOFError:
                    exit_mode = True
                    print("User exists program, but files are saved.")
                # schedule next review
                interval_days = {1: 1, 2: 3, 3: 7, 4: 14}.get(card.box, 30)
                card.next_review = datetime.today() + timedelta(days=interval_days)

                card.save_row()

    def add_cards_mode(self):
        while True:
            user_input = input(">")
            if not user_input:
                self.save()
                break

            row, source_lang = translate(user_input, self.langs)
            
            while True:
                for lang, result in row.items():
                    if lang == source_lang:
                        print(f"{source_lang} | {result}")
                    else:
                        pass
                for lang, result in row.items():
                        if lang == source_lang:
                            pass
                        else:
                            print(f"--{lang}--> {result}")
                
                edit_lang = input("Edit: ").upper()
                if not edit_lang:
                    break
                elif edit_lang in self.langs:
                    row[edit_lang] = input(f"Edit card side (current: {row[edit_lang]}): ")
                elif edit_lang.strip().lower() == "define":
                    if source_lang == "EN-US":
                        source_lang = "EN"
                    definitions = get_definitions(user_input, source_lang.lower())
                    print(definitions)

            self.cards.append(Flashcard(row=row))

    def edit_deck_mode(self):
        self.print_cards()
        while True:
            card_number = input("\nTo edit, enter card number: ").strip()
            if not card_number:
                break
            try:
                card_number = int(card_number) - 1
                if not 0 < card_number <= len(self.cards):
                    raise ValueError
            except ValueError:
                print(f"Please input a number from 1 - {len(self.cards)}")
            
            card = self.cards[card_number]
            card.row
            print(f"Card {card_number + 1}:")
            for lang, result in card.row.items():
                if lang in ["next_review", "last_review", "box"]:
                    pass
                else:
                    print(f"    {lang} | {result}")

            while True:
                lang = input("\nEnter the language of the card side you wish to edit or press [X] to delete card: ").upper()
                if not lang:
                    break
                elif lang == "X":
                    self.cards.pop(card_number)
                    break
                elif lang in self.langs:
                    card.row[lang] = input(f"Edit card side (current: {card.row[lang]} ): ")

def add_langs():  #It's good where it is.
    print("Please enter all the languages.")
    langs = []
    while True:
        try:
            l_input = input("Add a language: ").strip().lower()
            if not l_input and 1 < len(langs):
                break
            if not target_langues[l_input] in langs:
                langs.append(target_langues[l_input])
        except KeyError:
            print("Supported languages are:")
            numbered_langues = {i: lang for i, lang in enumerate(target_langues.keys(), start=1)}
            print(numbered_langues)
            for number, word in numbered_langues.items():
                print(f"{number} | {word}")
            try:
                input_number = int(input("Choose the lang as number: ").strip())
                n_input = numbered_langues[input_number]
                if not target_langues[n_input] in langs:
                    langs.append(target_langues[n_input])
            except ValueError:
                print("Not a number or not in list")
    return langs

def fix_langs(source_lang):  #maybe deck Class
    if source_lang == "EN":
        return "EN-US"
    elif source_lang == "PT":
        return "PT-PT"
    else:
        return source_lang

def decks_info(): #redone & uses classes
    deck_files = glob.glob("*.csv")
    info = []
    if not deck_files:
        return None
    for f in deck_files:
        deck = Deck(f)
        langs = deck.langs
        row_count = len(deck.cards)
        name = deck.csv_file
        
        info.append((name, row_count, langs))
    return info

def print_decklist(decks_info): #Could be put into Deck, but unnecessary
    print("\nDecks found:")
    for i, (file, n_row, langs) in enumerate(decks_info, 1):
        print(f"[{i}] {file}  ({n_row} cards) | {", ".join(langs[:-1])} and {langs[-1]}")

def translate(input, langs):
    row = {}
    for lang in langs:
        result = deepl_client.translate_text(input, target_lang= lang)
        row[lang] = result
        source_lang = fix_langs(result.detected_source_lang)
    if not source_lang in langs:
        print("The detected language does not match your deck languages, but we tried our best translating them quand-meme.")
    return row, source_lang

def get_definitions(word, language):
    url = f"https://freedictionaryapi.com/api/v1/entries/{language}/{word}"
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            return ["Word not found"]
        
        data = response.json()
        
        if isinstance(data, dict) and ("error" in data or "message" in data):
            return [data.get("message", data.get("error", "No definition found"))]
        
        if not isinstance(data, dict) or "entries" not in data:
            return ["No definitions found"]
        
        definitions = []
        
        for entry in data["entries"]:
            part_of_speech = entry.get("partOfSpeech", "unknown")
            
            for sense in entry.get("senses", []):
                definition = sense.get("definition", "")
                if definition:
                    definitions.append(f"{part_of_speech}: {definition}")
        
        return definitions if definitions else ["No definitions found"]
        
    except Exception as e:
        return [f"Error: {str(e)}"]

def new_deck_mode():
    deck = input("How would you like to name your new deck?\nName: ").strip() + ".csv"
    langs = add_langs()
    return deck, langs


def main():
    startup()
    skip_to_load = False
    while True:
        if not skip_to_load:
            deck_mode = input("\n[N]ew deck | [L]oad deck | [Q]uit Program\nInput: ").strip().lower()
        else:
            deck_mode = "l"
            skip_to_load = False

# Existing Deck mode:
        if deck_mode == "l": 
            info = decks_info()
            if not info:
                print("Couldn't find any decks.")
                break
            print_decklist(info)
            while True:
                try:
                    choice = int(input("\nWhich file do you want to open?\nEnter a number: "))
                    deck_choice = info[choice - 1][0]
                    deck = Deck(deck_choice)
                    print(deck.csv_file)
                    break
                except (ValueError):
                    print("Please enter a number.")
                except IndexError:
                    print(f"Number is out of range. Choose number from 1 to {len(info)}")

            while True:
                mode = input("\nEnter your mode. [A]dd cards | [S]how cards | [T]rain deck | Save and [Q]uit deck\nMode: ").strip().lower()
                if mode == "a":
                    langs = deck.langs
                    deck.add_cards_mode()
                elif mode == "q":
                    deck.save()
                    break
                elif mode == "s":
                    print(deck.csv_file)
                    deck.edit_deck_mode()
                    #existing_edit_deck_mode(deck)
                elif mode == "t":
                    for lang in deck.langs:
                        print(lang)

                    from_langs = []
                    to_langs = []

                    while True:
                        if (len(deck.langs) - len(from_langs)) == 1:
                            break
                        from_lang = input("from which language(s) do you want to learn? (end with Enter) ").upper()
                        if not from_lang and len(from_langs) >= 1:
                            break
                        elif from_lang in deck.langs:
                            from_langs.append(from_lang)
                        else:
                            print("Please try again.")

                    while True:
                        if (len(deck.langs) - len(from_langs) - len(to_langs)) == 1:
                            for lang in deck.langs:
                                if not lang in from_langs and not lang in to_langs:
                                    to_langs.append(lang)
                                    stop = True
                                    break
                            if stop:
                                break
                        to_lang = input("What will be your answer language? (end with Enter) ").upper()
                        if not to_lang and len(to_langs) >= 1:
                            break
                        elif to_lang in deck.langs and not to_lang in from_langs:
                            to_langs.append(to_lang)
                        else:
                            print("Please try again.")

                    print(f"Question language(s): {", ".join(from_langs)}")
                    print(f"Answer language(s): {", ".join(to_langs)}")

                    deck.train(from_langs= from_langs, to_langs= to_langs)



# New Deck mode:
        elif deck_mode == "n": 
            deck_name, langs = new_deck_mode()
            deck_name
            deck = Deck(csv_file=deck_name, langs=langs)
            skip_to_load = True
        else:
            sys.exit()


if __name__ == "__main__":
    main()



    # In [S]how cards: 'To edit card, enter its number: KINDA CHECK
    # When translating: 'Enter result lang to edit result: '  CHECK
# add deck langs to load deck output???  CHECK
# Non-translate mode

# ERRORS and more:    
    # EOFError and in general the exception policy of the program.
    # empty .csv files break the list, because they don't have fieldnames
    # Error message when decks don't have cards or enter edit mode directly
    # Tabulate and pandas integration