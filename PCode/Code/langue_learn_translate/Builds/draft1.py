import deepl
# Deepl Setup
auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
deepl_client = deepl.DeepLClient(auth_key)

# Defining Dict
deck_1 = {}
target_langues = {
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

# Defining Functions
def setlangue(prompt):
    while True:
        langue = input(prompt)
        if langue in target_langues:
            return target_langues[langue]
        elif not langue in target_langues:
            print("Here is a list of the supported languages: Czech, Danish, German, English (generic), English (British), English (American), Spanish, Spanish (Latin American), Estonian, Finnish, French, Hungarian, Indonesian, Italian, Lithuanian, Latvian, Norwegian Bokmål, Dutch, Polish, Portuguese (generic), Portuguese (Brazilian), Portuguese (European), Romanian, Slovak, Slovenian, Swedish, Turkish, Vietnamese")

def translate(text, target_langue, deck):
    result = deepl_client.translate_text(text, target_lang=target_langue)
    deck[text] = result.text

# Setting first target language
target_langue = setlangue("What is your answer language?: ")

# Real Program

while True:
    try:
        translate(input(), target_langue, deck_1)
    except EOFError:
        break

print(deck_1)

