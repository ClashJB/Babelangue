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

def add_langs():
    print("Please enter all the languages and finish with ctrl + z.")
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
        try:
            with open(f, "r", encoding="utf-8") as f:
                row_count = sum(1 for _ in f) - 1  # subtract 1 for header
                print("Number of data rows:", row_count)
        except Exception:
            ...
        decks_info.append((f.name, row_count))
    return decks_info

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
    deck = input("How would you like to name your new deck?\n>").strip() + ".csv"
    add_langs()
    with open(deck, "w", newline="", encoding="utf-8") as deck:
        writer = csv.DictWriter(deck, fieldnames= langs)
        writer.writeheader()

        try:
            while True:
                user_input = input(">")
                if not user_input:
                    break

                row, source_lang = translate(user_input, langs)

                print(f"{source_lang} | {user_input}")

                for lang, result in row.items():
                        if lang == source_lang:
                            pass
                        else:
                            print(f"--{lang}--> {result}")
                writer.writerow(row)
        except EOFError:
            sys.exit()

def main():
    startup()

    mode = input("Welcome to BABELANGUE!\nDo you want to [N]ew deck or [L]oad deck?").strip().lower()
    if mode == "l":
        decks_info = list_decks()
        for i, (file, n_row) in enumerate(decks_info, 1):
            print(f"[{i}] {file}  ({n_row} cards)")
    else:
        deck = input("How would you like to name your new deck?\n>").strip() + ".csv"
        add_langs()
        with open(deck, "w", newline="", encoding="utf-8") as deck:
            writer = csv.DictWriter(deck, fieldnames= langs)
            writer.writeheader()

            try:
                while True:
                    user_input = input(">")
                    if not user_input:
                        break

                    row, source_lang = translate(user_input, langs)

                    print(f"{source_lang} | {user_input}")

                    for lang, result in row.items():
                            if lang == source_lang:
                                pass
                            else:
                                print(f"--{lang}--> {result}")
                    writer.writerow(row)
            except EOFError:
                sys.exit()



if __name__ == "__main__":
    main()