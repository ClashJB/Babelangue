import os
from flask import Flask, render_template, request
from BABELANGUE_alpha1 import Deck, Flashcard, translate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translator", methods=["GET", "POST"])
def translator():
    deck_files = [f for f in os.listdir("data") if f.endswith(".csv")]

    if request.method == "POST":
        deck_name = request.form.get("deck")
        text = request.form.get("text")

        deck_langs = None
        translations = None
        source_lang = None

        if deck_name:
            deck_path = os.path.join("data", deck_name)
            deck = Deck(deck_path)
            deck_langs = deck.langs

            if text:
                row, source_lang = translate(text, deck.langs)
                translations = {lang: str(row[lang]) for lang in deck.langs}

        return render_template(
            "translator.html",
            decks=deck_files,
            selected_deck=deck_name,
            deck_langs=deck_langs,
            source_lang=source_lang,
            translations=translations,
            text=text
        )
    return render_template("translator.html", decks=deck_files)


@app.route("/save_card", methods=["POST"])
def save_card():
    deck_name = request.form.get("deck")
    text = request.form.get("text")

    deck_path = os.path.join("data", deck_name)
    deck = Deck(deck_path)

    row, src_lang = translate(text, deck.langs)
    clean_row = {lang: str(row[lang]) for lang in row}

    deck.cards.append(Flashcard(row=clean_row))
    deck.save()

    return render_template(
        "translator.html",
        decks=[f for f in os.listdir("data") if f.endswith('.csv')],
        selected_deck=deck_name,
        deck_langs=deck.langs,
        saved=True
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
