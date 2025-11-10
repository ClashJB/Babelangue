import deepl

# Load DeepL API key from environment variable
# (Set it in your terminal: export DEEPL_API_KEY="your_key_here")
auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
if not auth_key:
    raise ValueError("Missing DeepL API key. Please set DEEPL_API_KEY in your environment.")

deepl_client = deepl.DeepLClient(auth_key)

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


class CardDeck:
    def __init__(self, name, target_lang):
        self.name = name
        self.cards = {}  # {front_text: back_text}
        self.target_lang = target_lang

    def add_card(self, front_text):
        """Translate text and add to deck as a card."""
        result = deepl_client.translate_text(front_text, target_lang=self.target_lang)
        self.cards[front_text] = result.text

    def display_cards(self):
        for front, back in self.cards.items():
            print(f"{front} → {back}")


def choose_language():
    """Prompt until a valid language is chosen."""
    while True:
        choice = input("What is your answer language?: ")
        if choice in TARGET_LANGUAGES:
            return TARGET_LANGUAGES[choice]
        else:
            print("Supported languages:")
            print(", ".join(TARGET_LANGUAGES.keys()))


def main():
    deck_name = input("Name your deck: ")
    target_lang = choose_language()
    deck = CardDeck(deck_name, target_lang)

    print("Type phrases to translate. Press Ctrl+D (or Ctrl+Z on Windows) to stop.")
    try:
        while True:
            phrase = input("> ")
            deck.add_card(phrase)
    except EOFError:
        pass

    print("\nYour deck:")
    deck.display_cards()


if __name__ == "__main__":
    main()
