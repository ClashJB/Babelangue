import os
from flask import Flask, render_template, request, jsonify
from BABELANGUE_alpha1 import Deck, Flashcard, translate  # your BABELANGUE_alpha1.py

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Load the translator page with list of decks
@app.route("/translator")
def translator():
    deck_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    return render_template("translator.html", decks=deck_files)

# Return languages from a selected deck
@app.route("/get_deck_langs")
def get_deck_langs():
    deck_name = request.args.get("deck")
    deck_path = os.path.join("data", deck_name)

    if not os.path.exists(deck_path):
        return jsonify({"error": "Deck not found"}), 404

    deck = Deck(deck_path)
    return jsonify({"langs": deck.langs})

# Translate text using your backend logic
@app.route("/translate_text", methods=["POST"])
def translate_text():
    data = request.get_json()
    text = data.get("text")
    deck_name = data.get("deck")

    if not text or not deck_name:
        return jsonify({"error": "Missing text or deck"}), 400

    deck_path = os.path.join("data", deck_name)
    if not os.path.exists(deck_path):
        return jsonify({"error": "Deck not found"}), 404

    deck = Deck(deck_path)
    langs = deck.langs

    row, src_lang = translate(text, langs)

    # convert Deepl objects to strings
    clean_row = {lang: str(row[lang]) for lang in row}

    return jsonify({
        "translations": clean_row,
        "source_lang": src_lang,
        "langs": langs
    })

# Save translated card into deck
@app.route("/save_card", methods=["POST"])
def save_card():
    data = request.get_json()
    deck_name = data.get("deck")
    row = data.get("row")

    if not deck_name or not row:
        return jsonify({"error": "Missing deck or row data"}), 400

    deck_path = os.path.join("data", deck_name)
    if not os.path.exists(deck_path):
        return jsonify({"error": "Deck not found"}), 404

    deck = Deck(deck_path)

    flashcard = Flashcard(row=row)
    deck.cards.append(flashcard)
    deck.save()

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
