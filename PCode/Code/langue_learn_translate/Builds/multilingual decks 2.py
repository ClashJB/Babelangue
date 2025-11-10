import deepl
import csv
import sys
import re
import pyfiglet
import glob

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
deck = "multideck1.csv"


def startup():
    print(pyfiglet.figlet_format("BABELANGUE", font="chunky"))
    build = sys.argv[0]
    print(f"Build: {build}")
    print("Welcome to BABELANGUE!")

def add_langs():
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

def fix_langs(source_lang):
    if source_lang == "EN":
        return "EN-US"
    elif source_lang == "PT":
        return "PT-PT"
    else:
        return source_lang

def list_decks():
    deck_files = glob.glob("*.csv")
    decks_info = []
    for f in deck_files:
        langs = get_langs(f)
        try:
            with open(f, "r", encoding="utf-8") as f:
                row_count = sum(1 for _ in f) - 1
                
        except Exception:
            ...
        
        decks_info.append((f.name, row_count, langs))
    return decks_info

def print_decklist(decks_info):
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

def new_deck_mode():
    deck = input("How would you like to name your new deck?\nName: ").strip() + ".csv"
    langs = add_langs()
    return deck, langs

def add_cards_mode(deck, langs, new_deck= False):
    if new_deck == True:
        filemode = "w"
    elif new_deck == False:
        filemode = "a"
    with open(deck, filemode, newline="", encoding="utf-8") as deck:
        writer = csv.DictWriter(deck, fieldnames= langs)
        if new_deck:
            writer.writeheader()
        try:
            while True:
                user_input = input(">")
                if not user_input:
                    break

                row, source_lang = translate(user_input, langs)

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
                    
                    edit_lang = input("Edit: ")
                    if not edit_lang:
                        break
                    elif edit_lang in langs:
                        row[edit_lang] = input(f"Edit card side (current: {row[edit_lang]}): ")
                writer.writerow(row)
        except EOFError:
            sys.exit()

def get_langs(file):
    with open(file , mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames

def print_cards(file):
    with open(file, mode="r", newline="") as deck:
        reader = csv.DictReader(deck)
        for i, row in enumerate(reader):
            print(f"Card {i}:")
            for lang, result in row.items():
                print(f"    {lang} | {result}")
                
def main():
    startup()
    while True:
        deck_mode = input("\n[N]ew deck | [L]oad deck | [Q]uit Program\nInput: ").strip().lower()

# Existing Deck mode:
        if deck_mode == "l": 
            decks_info = list_decks()
            print_decklist(decks_info)
            while True:
                try:
                    choice = int(input("\nWhich file do you want to open?\nEnter a number: "))
                    deck = decks_info[choice - 1][0]
                    print(deck)
                    break
                except (ValueError):
                    print("Please enter a number.")
                except IndexError:
                    print(f"Number is out of range. Choose number from 1 to {len(decks_info)}")

            while True:
                mode = input("\nEnter your mode. [A]dd cards | [S]how cards | [T]rain deck | [Q]uit deck\nMode: ").strip().lower()
                if mode == "a":
                    langs = get_langs(deck)
                    add_cards_mode(deck, langs)
                elif mode == "q":
                    break
                elif mode == "s":
                    print(deck)
                    print_cards(deck)

# New Deck mode:
        elif deck_mode == "n": 
            deck, langs = new_deck_mode()
            add_cards_mode(deck, langs, new_deck= True)
        else:
            sys.exit()


if __name__ == "__main__":
    main()


# Edit existing cards???
    # In [S]how cards: 'To edit card, enter its number: '
    # When translating: 'Enter result lang to edit result: '  CHECK
# add deck langs to load deck output???  CHECK
# Non-translate mode
# Train mode
    # feedback system (maybe from 0-1)
    # False responses are asked again at the end
# EOFError and in general the exception policy of the program.
# empty .csv files break the list, because they don't have fieldnames
# Error message when decks don't have cards or enter edit mode directly