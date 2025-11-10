import deepl

auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
deepl_client = deepl.DeepLClient(auth_key)

deck = {}


def translate(text, target_langue, deck):
    result = deepl_client.translate_text(text, target_lang=target_langue)
    deck[text] = result.text



text = input("Input: ")
result = deepl_client.translate_text(text, target_lang="FR")
deck[text] = result.text

print(deck)