import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session, flash
from werkzeug.utils import secure_filename
from BABELANGUE_alpha1 import Deck, Flashcard, translate, target_langues, get_definitions
import glob
from datetime import datetime, timedelta
import random
import secrets
from auth import auth, login_required
import csv
from mistral_test import image_to_csv
import pandas
from pdf2image import convert_from_path

def get_user_folder():
    return f"user_data/{session['username']}"

def expand_languages(d=dict, values=list):
    inverse = {v: k for k, v in d.items()}
    return [inverse[val].capitalize() for val in values if val in inverse]

def lang_code_to_dict_api(lang_code):
    mapping = {
        'EN-US': 'en', 'EN-GB': 'en', 'DE': 'de', 'ES': 'es', 'ES-419': 'es',
        'FR': 'fr', 'IT': 'it', 'PT-PT': 'pt', 'PT-BR': 'pt', 'NL': 'nl',
        'PL': 'pl', 'TR': 'tr', 'CS': 'cs', 'DA': 'da', 'FI': 'fi',
        'HU': 'hu', 'LV': 'lv', 'LT': 'lt', 'RO': 'ro', 'SK': 'sk',
        'SL': 'sl', 'SV': 'sv'
    }
    return mapping.get(lang_code)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Change this to a fixed value in production
app.register_blueprint(auth)

@app.route("/")
def index():
    logged_in = 'username' in session
    username = session.get('username')
    return render_template("index.html", logged_in=logged_in, username=username)

@app.route("/translator", methods=["GET", "POST"])
@login_required
def translator():
    user_folder = get_user_folder()
    deck_files = [f for f in os.listdir(user_folder) if f.endswith(".csv") and not f.startswith("verbs_")]

    selected_deck = request.args.get("deck") or request.form.get("deck")
    
    deck_langs = None
    translations = None
    source_lang = None
    text = None
    saved = False
    deck_langs_text = None

    if selected_deck:
        deck_path = os.path.join(user_folder, selected_deck)
        try:
            deck = Deck(deck_path)
            deck_langs = deck.langs
            deck_lang_words = expand_languages(target_langues, deck_langs)
            deck_langs_text = f"{', '.join(deck_lang_words[:-1])} and {deck_lang_words[-1]}"
        except FileNotFoundError:
            selected_deck = None

    if request.method == "POST":
        action = request.form.get("action")
        selected_deck = request.form.get("deck")
        text = request.form.get("text")

        if not selected_deck or selected_deck == "None":
            return render_template("translator.html", decks=deck_files, error="Please select a deck.")

        deck_path = os.path.join(user_folder, selected_deck)
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

    return render_template(
        "translator.html", 
        decks=deck_files,
        selected_deck=selected_deck,
        deck_langs=deck_langs,
        deck_langs_text=deck_langs_text
    )

@app.route("/get_definitions", methods=["POST"])
@login_required
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
@login_required
def trainer():
    user_folder = get_user_folder()
    deck_files = [d for d in os.listdir(user_folder) if d.endswith(".csv") and not d.startswith("verbs_")]
    verb_files = [d for d in os.listdir(user_folder) if d.endswith(".csv") and d.startswith("verbs_")]
    info = []
    verb_info = []
    deleted_flag = request.args.get("deleted")

    for f in deck_files:
        deck_path = os.path.join(user_folder, f)
        deck = Deck(deck_path)
        name = os.path.splitext(os.path.basename(deck.csv_file))[0]
        langs = deck.langs
        deck_lang_words = expand_languages(target_langues, langs)
        langs_text = f"{', '.join(deck_lang_words[:-1])} and {deck_lang_words[-1]}"
        n_due = deck.n_due
        n_cards = deck.n_cards
        
        info.append((name, langs, n_due, n_cards, langs_text, deck_path))

    for f in verb_files:
        deck_path = os.path.join(user_folder, f)
        deck = Deck(deck_path)
        name = os.path.splitext(os.path.basename(deck.csv_file))[0]
        n_due = deck.n_due
        n_cards = deck.n_cards 

        verb_info.append((name, n_due, n_cards, deck_path))
        
    return render_template(
        "decklist.html", 
        info=info,
        verb_info = verb_info,
        deleted=deleted_flag
    )

@app.route("/deck/<path:deck>", methods=["GET","POST"])
@login_required
def deck_overview(deck):
    user_folder = get_user_folder()
    
    # Security: ensure deck is in user's folder
    deck_path = os.path.join(user_folder, os.path.basename(deck))
    if not deck_path.startswith(user_folder):
        return "Access denied", 403
    
    deck = Deck(deck_path)
    name = os.path.splitext(os.path.basename(deck.csv_file))[0]
    cards = deck.cards
    if not name.startswith("verbs_"):
        langs = deck.langs
        deck_lang_words = expand_languages(target_langues, langs)
        langs_text = f"{', '.join(deck_lang_words[:-1])} and {deck_lang_words[-1]}"
    else:
        langs_text = "This deck doesn't have langs"
    n_due = deck.n_due
    n_cards = deck.n_cards
    progress = []
    n_box = deck.get_progress()
    for n in n_box:
        try:
            progress.append(round((n / n_cards) * 100))
        except ZeroDivisionError:
            progress.append(0)

    if request.method == "POST":
        action = request.form.get("action")
        try:
            card = int(request.form.get("delete_card"))
        except (TypeError, ValueError):
            card = None

        if action =="delete":
            deleted_folder = os.path.join(user_folder, "deleted")
            os.makedirs(deleted_folder, exist_ok=True)
            os.replace(deck.csv_file, os.path.join(deleted_folder, f"{name}.csv"))
            try:
                os.replace(
                    os.path.join(user_folder, f"{name}_lang_order.json"),
                    os.path.join(deleted_folder, f"{name}_lang_order.json")
                )
            except FileNotFoundError:
                pass
            return redirect(url_for("trainer", deleted=True))
        
        if action == "edit":
            return redirect(url_for("deck_edit", deck=os.path.basename(deck.csv_file)))
        
        if action == "export":
            return send_file(deck.csv_file,
                             mimetype="text/csv",
                             as_attachment=True,
                             download_name=f"{name}.csv")
        
        if card:
            deck.cards.pop(card - 1)
            deck.save()

    return render_template(
        "deck.html",
        name=name,
        langs_text=langs_text,
        n_due=n_due,
        n_cards=n_cards,
        n_box=n_box,
        progress=progress,
        cards=cards,
        deck_path=os.path.basename(deck.csv_file),
    )

@app.route("/card/<path:deck>/<card>", methods=["GET", "POST"])
@login_required
def card_view(deck, card):
    user_folder = get_user_folder()
    deck_path = os.path.join(user_folder, os.path.basename(deck))
    
    deck_inst = Deck(deck_path)
    name = os.path.splitext(os.path.basename(deck_inst.csv_file))[0]
    langs = deck_inst.langs
    saved = ""

    try:
        index = int(card)
    except (TypeError, ValueError):
        return "Invalid card index"

    if index < 0 or index >= len(deck_inst.cards):
        return "Card not found 404"

    card = deck_inst.cards[index]
    row = card.card_row

    if request.method == "POST":
        action = request.form.get("action")

        if action == "save":
            for lang in langs:
                deck_inst.cards[index].row[lang] = request.form.get(f"edited_{lang}")

            deck_inst.save()
            saved = "Card saved successfully"
            deck_inst = Deck(deck_path)

    return render_template(
        "card.html",
        card=deck_inst.cards[index],
        name=name,
        langs=langs,
        index=index,
        deck_path=os.path.basename(deck_inst.csv_file),
        saved=saved
    )

@app.route("/train/<path:deck>", methods=["GET", "POST"])
@login_required
def train(deck):
    user_folder = get_user_folder()
    deck_path = os.path.join(user_folder, os.path.basename(deck))
    
    deck_inst = Deck(deck_path)
    name = os.path.splitext(os.path.basename(deck_inst.csv_file))[0]
    deck_path_display = os.path.basename(deck_inst.csv_file)
    n_due = deck_inst.n_due
    due_percentage = int((deck_inst.n_cards - n_due) / deck_inst.n_cards * 100) if deck_inst.n_cards > 0 else 0
    s_langs = deck_inst.order

    if not s_langs:
        s_langs = []

    due_card = None
    for card_inst in deck_inst.cards:
        if datetime.today() >= card_inst.next_review:
            due_card = card_inst
            break
    
    if not due_card:
        return render_template(
            "trainer.html",
            deck_inst=deck_inst,
            name=name,
            deck_path=deck_path_display,
            due_percentage=due_percentage,
            n_due=n_due,
            card_inst=None,
            row=None,
            s_langs=s_langs
        )

    row = due_card.card_row
    card_inst = due_card

    if request.method == "POST":
        action = request.form.get("action")

        if action == "save_langs":
            raw = request.form.getlist('selected_langs')
            seen = set()
            s_langs = [x for x in raw if x and x not in seen and not seen.add(x)]

            if len([lang for lang in s_langs if lang != "no_lang"]) == len(deck_inst.langs) - 1:
                for lang in deck_inst.langs:
                    if not lang in s_langs:
                        missing_lang = lang
                for n, lang in enumerate(s_langs):
                    if lang == "no_lang":
                        s_langs[n] = missing_lang
            
            deck_inst.order = s_langs

        else:
            if action == "know_it":
                card_inst.box += 1
            elif action == "dont_know":
                card_inst.box = 1

            interval_days = {1: 1, 2: 3, 3: 7, 4: 14}.get(card_inst.box, 30)
            card_inst.next_review = datetime.today() + timedelta(days=interval_days)
            card_inst.save_row()
            deck_inst.save()

            return redirect(url_for("train", deck=deck_path_display))

    if s_langs:
        ordered = {}
        for lang in s_langs:
            if lang in row:
                ordered[lang] = row[lang]
        for lang, val in row.items():
            if lang not in ordered:
                ordered[lang] = val
        deck_inst.save()
        row = ordered

    return render_template(
        "trainer.html",
        deck_inst=deck_inst,
        name=name,
        deck_path=deck_path_display,
        due_percentage=due_percentage,
        n_due=n_due,
        card_inst=card_inst,
        row=row,
        s_langs=s_langs
    )

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user_folder = get_user_folder()
    langs = [x.capitalize() for x in target_langues.keys()]

    s_langs = []
    s_langs_text = None
    deck_name = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")
        deck_name = request.form.get("deck_name")
        raw = request.form.getlist('selected_langs')
        seen = set()
        s_langs = [x for x in raw if x and x not in seen and not seen.add(x)]

        if s_langs:
            if len(s_langs) > 1:
                s_langs_text = f"{', '.join(s_langs[:-1])} and {s_langs[-1]}"
            else:
                s_langs_text = s_langs[0]   

        if action == "save":
            if not deck_name and not s_langs:
                error = "Missing deck name and language selection"
            elif not deck_name:
                error = "Missing deck name"
            elif not s_langs:
                error = "Missing language selection"
            elif len(s_langs) < 2:
                error = "Minimum of 2 languages are required"
            else:
                d_langs = []
                for lang in s_langs:
                    d_langs.append(target_langues[lang.lower()])

                filename = os.path.join(user_folder, secure_filename(deck_name) + ".csv")
                deck = Deck(filename, d_langs)
                deck.save()
                return redirect("/trainer")

    return render_template(
        "add.html",
        s_langs=s_langs,
        langs=langs,
        s_langs_text=s_langs_text,
        deck_name=deck_name,
        error=error
    )

@app.route("/import", methods=["GET", "POST"])
@login_required
def import_deck():
    return render_template("import.html")

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    user_folder = get_user_folder()
    
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == "":
        return "No file", 400
    
    filename = secure_filename(file.filename)
    upload_path = os.path.join(user_folder, "uploads", filename)
    os.makedirs(os.path.join(user_folder, "uploads"), exist_ok=True)
    file.save(upload_path)
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".csv":
        deck = Deck(upload_path)  

        if not deck.langs:  
            final_path = os.path.join(user_folder, f"verbs_{deck.name}.csv")
            os.replace(deck.csv_file, final_path)
            deck.csv_file = final_path
            return render_template(
                "import.html",
                no_langs=True
            )
        
        final_path = os.path.join(user_folder, f"{deck.name}.csv")
        os.replace(deck.csv_file, final_path)
        deck.csv_file = final_path

        return redirect(url_for("deck_overview", deck=os.path.basename(final_path)))
    elif extension == ".pdf":
        #image_to_csv(upload_path)
        print(upload_path)
        filename = f"{os.path.splitext(filename)[0]}.png"
        print(filename)

        relative_path = f"{session['username']}/uploads/{filename}"
        print(relative_path)

        images = convert_from_path(upload_path, dpi=300, first_page=1, last_page=1)
        images[0].save(f"{os.path.splitext(upload_path)[0]}.png", "PNG")

        return redirect(url_for("image_to_list",file=relative_path))


        

@app.route("/deckedit/<path:deck>", methods=["GET","POST"])
@login_required
def deck_edit(deck):
    user_folder = get_user_folder()
    deck_path = os.path.join(user_folder, os.path.basename(deck))
    
    deck_inst = Deck(deck_path)

    langs = [x.capitalize() for x in target_langues.keys()]

    s_langs = []

    for lang_word in expand_languages(target_langues, deck_inst.langs):
        s_langs.append(lang_word)
    s_langs_text = None
    deck_name = deck_inst.name
    error = None

    if request.method == "POST":
        action = request.form.get("action")
        deck_name = request.form.get("deck_name")
        raw = request.form.getlist('selected_langs')
        seen = set()
        s_langs = [x for x in raw if x and x not in seen and not seen.add(x)]
        
        if action == "save" or action == "langadd":
            if not deck_name and not s_langs:
                error = "Missing deck name and language selection"
            elif not deck_name:
                error = "Missing deck name"
            elif not s_langs:
                error = "Missing language selection"
            elif len(s_langs) < 2:
                error = "Minimum of 2 languages are required"
            else:
                d_langs = []
                for lang in s_langs:
                    d_langs.append(target_langues[lang.lower()])
                
                new_path = os.path.join(user_folder, secure_filename(deck_name) + ".csv")
                os.replace(deck_inst.csv_file, new_path)
                deck_inst.csv_file = new_path

                deck_inst.langs = d_langs
                deck_inst.save()

                if action == "langadd":
                    deck_inst = Deck(new_path)
                    deck_inst.ergaenzen()
                    deck_inst.save()

                return redirect("/trainer")

    if s_langs:
        if len(s_langs) > 1:
            s_langs_text = f"{', '.join(s_langs[:-1])} and {s_langs[-1]}"
        else:
            s_langs_text = s_langs[0]   

    return render_template(
        "deckedit.html",
        name=deck_inst.name,
        deck_path=os.path.basename(deck_inst.csv_file),
        s_langs=s_langs,
        langs=langs,
        s_langs_text=s_langs_text,
        deck_name=deck_name,
        error=error
    )

@app.route("/imagetolist/<path:file>", methods=["GET","POST"])
@login_required
def image_to_list(file=None):
    deck_langs = []
    file_no_extension = os.path.splitext(file)[0]
    file_extension = os.path.splitext(file)[1]
    user_folder = get_user_folder()
    deleted_folder = os.path.join(user_folder, "deleted")
    os.makedirs(deleted_folder, exist_ok=True)
    full_path = os.path.join("user_data", file)
    filename = os.path.split(file)[1]
    

    if file_extension == ".csv":
        reset_check = filename in os.listdir(deleted_folder)
        langs_check = True

        with open(full_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
            fieldnames = [fieldname.upper().strip() for fieldname in reader.fieldnames]

            for fieldname in fieldnames:
                if fieldname in target_langues.values():
                    deck_langs.append(fieldname)
                else:
                    langs_check = False
                    deck_langs.append("")

        if request.method == "POST":
            action = request.form.get("action")
            try:
                n_column = int(request.form.get("delete_column"))
            except (TypeError, ValueError):
                n_column = None

            selected_langs = []
            for i in range(len(fieldnames)):
                selected_langs.append(
                    request.form.get(f"selected_langs_{i}", fieldnames[i]) 
                )

            print(selected_langs)

            df = pandas.read_csv(full_path)
            df.columns = selected_langs

            if n_column:
                if (len(fieldnames)) > 2:
                    os.replace(full_path, os.path.join(deleted_folder, filename))
                    df.drop(df.columns[n_column], axis=1, inplace=True)
                else:
                    ...
            df.to_csv(full_path, index=False)

            if action == "reset":
                if filename in os.listdir(deleted_folder):
                    os.remove(full_path)
                    os.replace(os.path.join(deleted_folder, filename), full_path)

            if action == "to_deck":
                os.replace(full_path, os.path.join(user_folder, filename))
                return redirect(url_for("deck_overview", deck=os.path.join(user_folder, filename)))

            return redirect(url_for("image_to_list", file=file))

        return render_template(
            "imagetolist.html",
            langs=target_langues,
            fieldnames=fieldnames,
            rows=rows,
            deck_langs=deck_langs,
            reset_check=reset_check,
            langs_check=langs_check
            )
    elif file_extension == ".png":
        if request.method == "POST":
            action = request.form.get("action")
            if action == "into_csv":
                pdf_path = f"{file_no_extension}.pdf"
                csv_path = f"{file_no_extension}.csv"
                image_to_csv(os.path.join("user_data", pdf_path))
                return redirect(url_for("image_to_list", file=csv_path))


        return render_template(
            "imagetolist.html",
            pdf_path=file
        )
    


@app.route("/pdf/<path:filepath>")
@login_required
def serve_pdf(filepath):
    if not filepath.startswith(f"{session['username']}/"):
        return "Access denied", 403
    return send_file(os.path.join("user_data", filepath), mimetype="application/pdf")

    

if __name__ == "__main__":
    import sys
    debug_mode = True #'--debug' in sys.argv
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)