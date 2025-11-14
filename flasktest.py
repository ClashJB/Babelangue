import os
from flask import Flask, render_template, request, jsonify
from BABELANGUE_alpha1 import Deck, translate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Translator page - shows deck list
@app.route("/translator")
def translator():
    deck_files = [f for f in os.listdir("data") if f.endswith(".csv")]
    return render_template("translator.html", decks=deck_files)

# AJAX translation request
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

    deck = Deck(deck_path)       # load deck
    langs = deck.langs           # extract deck languages

    row, src_lang = translate(text, langs)

    row_serializable = {k: str(v) for k, v in row.items()}
    # row is already a dict: { "DE": "...", "FR": "...", ... }
    return jsonify({
        "translations": row_serializable,
        "source_lang": src_lang,
        "target_langs": langs
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
