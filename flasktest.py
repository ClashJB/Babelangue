import os
from flask import Flask, render_template, request, jsonify
from BABELANGUE_alpha1 import Deck, Flashcard, translate, target_langues, get_definitions
import glob


def expand_languages(d=dict, values=list):
    inverse = {v: k for k, v in d.items()}
    return [inverse[val].capitalize() for val in values if val in inverse]


# DeepL APU code to freedictionary API format
def lang_code_to_dict_api(lang_code):
    mapping = {
        'EN-US': 'en',
        'EN-GB': 'en',
        'DE': 'de',
        'ES': 'es',
        'ES-419': 'es',
        'FR': 'fr',
        'IT': 'it',
        'PT-PT': 'pt',
        'PT-BR': 'pt',
        'NL': 'nl',
        'PL': 'pl',
        'TR': 'tr',
        'CS': 'cs',
        'DA': 'da',
        'FI': 'fi',
        'HU': 'hu',
        'LV': 'lv',
        'LT': 'lt',
        'RO': 'ro',
        'SK': 'sk',
        'SL': 'sl',
        'SV': 'sv'
    }
    return mapping.get(lang_code)


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


@app.route("/get_definitions", methods=["POST"])
def get_definitions_route():
    """Fetch definitions for a word in a specific language"""
    data = request.json
    word = data.get('word')
    lang_code = data.get('lang')
    
    if not word or not lang_code:
        return jsonify({'error': 'Missing word or language'}), 400
    
    api_lang = lang_code_to_dict_api(lang_code)
    
    try:
        definitions = get_definitions(word, api_lang)
        return jsonify({'definitions' : definitions})
    except Exception as e:
        return jsonify({'error': f'Could not fetch definitions: {str(e)}'}), 500

@app.route("/trainer")
def trainer():
    deck_files = glob.glob("*.csv")
    info = []

    for f in deck_files:
        deck = Deck(f)
        name = deck.csv_file
        langs = deck.langs
        deck_lang_words = expand_languages(target_langues, langs)
        langs_text = f"{', '.join(deck_lang_words[:-1])} and {deck_lang_words[-1]}"
        n_due = deck.n_due
        n_cards = deck.n_cards
        
        info.append((name, langs, n_due, n_cards, langs_text))
        
    return render_template(
        "trainer.html", 
        info=info
        )
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)