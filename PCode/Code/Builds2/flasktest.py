from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Let's hope this will be over soon."

app.run(host="0.0.0.0", port=5001)
