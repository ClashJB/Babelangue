import json
import deepl
import pyfiglet
import glob

# Load DeepL API key from environment variable (It's not doing that yet)

auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
if not auth_key:
    raise ValueError("Missing DeepL API key. Please set DEEPL_API_KEY in your environment.")
deepl_client = deepl.DeepLClient(auth_key)


# Defining all available languages since the DeepL API doesn't really do that for me.
TARGET_LANGUAGES = {
    "Czech": "CS",
    "Danish": "DA",
    "German": "DE",
    "English (generic)": "EN",
    "English (British)": "EN-GB",
    "English (American)": "EN-US",
    "Spanish": "ES",
    "Spanish (Latin American)": "ES-419",
    "Estonian": "ET",
    "Finnish": "FI",
    "French": "FR",
    "Hungarian": "HU",
    "Indonesian": "ID",
    "Italian": "IT",
    "Lithuanian": "LT",
    "Latvian": "LV",
    "Norwegian Bokmål": "NB",
    "Dutch": "NL",
    "Polish": "PL",
    "Portuguese (generic)": "PT",
    "Portuguese (Brazilian)": "PT-BR",
    "Portuguese (European)": "PT-PT",
    "Romanian": "RO",
    "Slovak": "SK",
    "Slovenian": "SL",
    "Swedish": "SV",
    "Turkish": "TR",
    "Vietnamese": "VI"
}

def startup():
    print(pyfiglet.figlet_format("BABELANGUE", font="chunky"))
    build = "Draft 3 (This is just a string)"
    print(f"Build: {build}")

class CardDeck:
    def __init__(self, name, target_lang):
        self.name = name
        # store cards as dict of dicts
        # {front_text: {"translation": back_text, "source_lang": lang}}
        self.cards = {}
        self.target_lang = target_lang

    def add_card(self, front_text):
        """Translate text, detect source language, and add to deck."""
        result = deepl_client.translate_text(front_text, target_lang= self.target_lang)
        self.cards[front_text] = {"translation": result.text, "source_lang": result.detected_source_lang}

    def display_cards(self):
        for front, data in self.cards.items():
            print(f"{front} ({data['source_lang']}) → {data['translation']}")

    def save(self, filepath=None):
        """Save deck to a JSON file."""
        if not filepath:
            filepath = f"{self.name}.json"
        data = {
            "name": self.name,
            "target_lang": self.target_lang,
            "cards": self.cards,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Deck saved to {filepath}")

    @classmethod
    def load(cls, filepath):
        """Load deck from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        deck = cls(name=data["name"], target_lang=data["target_lang"])
        deck.cards = data["cards"]
        return deck

    def train(self):
        """Simple training mode: quiz user on the deck."""
        print("\nTraining mode! Press Enter to see the answer, Ctrl+C to quit.\n")
        try:
            for front, data in self.cards.items():
                input(f"Front ({data['source_lang']}): {front}  →  Your answer: ")
                print(f"Back: {data['translation']}\n")
                input("Did you know it? [Y]es or [N]o?").strip().lower()
        except KeyboardInterrupt:
            print("\nTraining stopped.")


def choose_language(prompt):
    """Prompt until a valid language is chosen."""
    while True:
        choice = input(prompt)
        if choice in TARGET_LANGUAGES:
            return TARGET_LANGUAGES[choice]
        else:
            print("Supported languages:")
            print(", ".join(TARGET_LANGUAGES.keys()))

def list_decks():
    """Return list of (filename, number_of_cards)."""
    deck_files = glob.glob("*.json")
    decks_info = []
    for f in deck_files:
        try:
            with open(f, "r", encoding="utf-8") as infile:
                data = json.load(infile)
                num_cards = len(data.get("cards", {}))
        except Exception:
            num_cards = 0
        decks_info.append((f, num_cards))
    return decks_info

def main():
    startup()


        # List available decks with number of cards
    decks_info = list_decks()
    if decks_info:
        print("\nAvailable decks:")
        for i, (f, n) in enumerate(decks_info, 1):
            print(f"[{i}] {f}  ({n} cards)")
    else:
        print("\nNo existing decks found.")

# Reprompt when number isnt in list and reprompt when file not found
    mode = input("Do you want to [N]ew deck or [L]oad deck? ").strip().lower()
    if mode == "l":
        if not decks_info:
            print("No decks to load, please create a new one.")
            return
        choice = input("Enter number of deck to load: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(decks_info):
            filepath = decks_info[int(choice) - 1][0]
        else:
            filepath = input("Enter deck filename: ").strip()
    
        deck = CardDeck.load(filepath)
    else:
        deck_name = input("Name your deck: ")
        target_lang = choose_language("What is your target language?: ")
        deck = CardDeck(deck_name, target_lang)


    while True:
        action = input("\nChoose: [A]dd card, [S]how cards, [T]rain, [Q]uit: ").strip().lower()
        if action == "a":
            print("Enter phrases below and press Ctrl-D (or Ctrl-Z on Windows) to stop")
            phrase_list = []
            while True:
                try:
                    phrase_list.append(input(">"))
                except EOFError:
                    for phrase in phrase_list:
                        deck.add_card(phrase)
                    break
        elif action == "s":
            deck.display_cards()
        elif action == "t":
            deck.train()
        elif action == "q":
            deck.save()
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
