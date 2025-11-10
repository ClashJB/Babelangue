import deepl

auth_key = "7053ad0d-f006-4202-aeb4-b96400b68c58:fx"
deepl_client = deepl.DeepLClient(auth_key)

result = deepl_client.translate_text("Hello, world!", target_lang="FR")
print(result.text)