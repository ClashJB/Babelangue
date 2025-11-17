import deepl

auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
if not auth_key:
    raise ValueError("Missing DeepL API key. Please set DEEPL_API_KEY in your environment.")
deepl_client = deepl.DeepLClient(auth_key)

def make_tri_dict(a, b, c):
    return {
        a: (b, c),
        b: (a, c),
        c: (a, b)
    }

tri_dict = make_tri_dict("EN", "DE", "FR")

results = []

while True:
    try:
        user_input = input("Your input and language formatted like this(Bonjour/FR):")

        prompt, source_langue = user_input.split("/")
        

        lang_1, lang_2 = tri_dict[source_langue]
        
        if source_langue != "EN":
            lang_1 = f"{lang_1}-US"


        result1 = deepl_client.translate_text(prompt,source_lang = source_langue, target_lang= lang_1)
        result2 = deepl_client.translate_text(prompt,source_lang = source_langue, target_lang= lang_2)

        print(f"{result1}/{lang_1}")
        print(f"{result2}/{lang_2}")

        results.append(f"{prompt}/{source_langue}")
        results.append(f"{result1}/{lang_1}")
        results.append(f"{result2}/{lang_2}")

    except EOFError:
        print(results)
        break


