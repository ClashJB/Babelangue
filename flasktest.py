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

    selected_deck = None
    deck_langs = None
    translations = None
    source_lang = None
    text = None
    saved = False

    if request.method == "POST":
        action = request.form.get("action")  # translate OR save
        selected_deck = request.form.get("deck")
        text = request.form.get("text")

        if not selected_deck:
            return render_template("translator.html", decks=deck_files, error="Please select a deck.")

        deck_path = os.path.join("data", selected_deck)
        deck = Deck(deck_path)
        deck_langs = deck.langs

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
                saved=True
            )

        # --- TRANSLATE ---
        if action == "translate":
            if text:
                row, source_lang = translate(text, deck_langs)
                translations = {lang: str(row[lang]) for lang in deck_langs}
        
        return render_template(
            "translator.html",
            decks=deck_files,
            selected_deck=selected_deck,
            deck_langs=deck_langs,
            translations=translations,
            source_lang=source_lang,
            text=text,
            saved=saved
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
