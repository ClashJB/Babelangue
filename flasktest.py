import os
from flask import Flask, render_template, request
from BABELANGUE_alpha1 import Deck, Flashcard, translate, target_langues


def expand_languages(d=dict, values=list):
    inverse = {v: k for k, v in d.items()}

    return [inverse[val].capitalize() for val in values if val in inverse]

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/translator", methods=["GET", "POST"])
def translator():
    deck_files = [f for f in os.listdir("data") if f.endswith(".csv")]

    selected_deck = None
    deck_langs = None
    translations = None
    source_lang = None
    text = None
    saved = False

    if request.method == "POST":
        action = request.form.get("action")
        selected_deck = request.form.get("deck")
        text = request.form.get("text")

        if not selected_deck:
            return render_template("translator.html", decks=deck_files, error="Please select a deck.")

        deck_path = os.path.join("data", selected_deck)
        deck = Deck(deck_path)
        deck_langs = deck.langs
        deck_lang_words = expand_languages(target_langues, deck_langs)
        deck_langs_text = f"{', '.join(deck_lang_words[:-1])} and {deck_lang_words[-1]}"

   

        if action == "save":
            clean_row = {}

            for lang in deck_langs:
                clean_row[lang] = request.form.get(f"edited_{lang}")

            deck.cards.append(Flashcard(row=clean_row))
            deck.save()
            saved = True

            return render_template(
                "translator.html",
                decks=deck_files,
                selected_deck=selected_deck,
                deck_langs=deck_langs,
                deck_langs_text=deck_langs_text,
                saved=True
            )

        if action == "translate":
            if text:
                row, source_lang = translate(text, deck_langs)
                translations = {lang: str(row[lang]) for lang in deck_langs}
        
        return render_template(
            "translator.html",
            decks=deck_files,
            selected_deck=selected_deck,
            deck_langs=deck_langs,
            deck_langs_text=deck_langs_text,
            translations=translations,
            source_lang=source_lang,
            text=text,
            saved=saved
        )

    return render_template("translator.html", decks=deck_files)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
