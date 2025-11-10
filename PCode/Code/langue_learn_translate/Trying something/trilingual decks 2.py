import deepl
import csv
import sys

auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
if not auth_key:
    raise ValueError("Missing DeepL API key. Please set DEEPL_API_KEY in your environment.")
deepl_client = deepl.DeepLClient(auth_key)


target_langues = {
    "czech": "CS",
    "danish": "DA",
    "german": "DE",
    "english (generic)": "EN",
    "english (British)": "EN-GB",
    "english": "EN-US",
    "spanish": "ES",
    "spanish (Latin American)": "ES-419",
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
    "portuguese (generic)": "PT",
    "portuguese (Brazilian)": "PT-BR",
    "portuguese (European)": "PT-PT",
    "romanian": "RO",
    "slovak": "SK",
    "slovenian": "SL",
    "swedish": "SV",
    "turkish": "TR",
    "vietnamese": "VI"
}

lang_1, lang_2, lang_3 = input("What are your input languages? ").split(",")
lang_1 = target_langues[lang_1.strip().lower()]
lang_2 = target_langues[lang_2.strip().lower()]
lang_3 = target_langues[lang_3.strip().lower()]


with open("trideck2.csv", "w", newline="") as deck:
    writer = csv.DictWriter(deck, fieldnames=(lang_1, lang_2, lang_3))
    writer.writeheader()

    try:
        while True:
            user_input = input(">")

            result1 = deepl_client.translate_text(user_input, target_lang= lang_1)
            source_lang_1 = result1.detected_source_lang

            result2 = deepl_client.translate_text(user_input, target_lang= lang_2)

            result3 = deepl_client.translate_text(user_input, target_lang= lang_3)

            print(f"Source language = {source_lang_1}")
            
            if source_lang_1 == "EN":
                source_lang_1 = "EN-US"

            if not source_lang_1 in [lang_1, lang_2, lang_3]:
                print("The detected language does not match your deck languages, but we tried our best translating them quand-meme.")
            else:
                print(f"{source_lang_1} | {user_input}")

            for result, lang in zip([result1, result2, result3], [lang_1, lang_2, lang_3]):
                    if lang == source_lang_1:
                        pass
                    else:
                        print(f"--> {result} | {lang}")

            writer.writerow({lang_1 : result1, lang_2 : result2, lang_3 : result3})
    except EOFError:
        sys.exit()