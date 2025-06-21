# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# --- static test data: a mix of DM & Player messages, with simple HTML markup
logs = [
    {"role": "DM",     "content": "<p>You stand at the mouth of a dimly lit cave.</p>"},
    {"role": "Player", "content": "<p>I light a torch and peer inside.</p>"},
    {"role": "DM",     "content": "<p>The torch casts dancing shadows along dripping walls.</p>"},
    {"role": "Player", "content": "<p>I move forward, careful of loose stones.</p>"},
    {"role": "DM",     "content": "<p>A distant growl echoes—something approaches.</p>"},
]

@app.route("/")
def index():
    # initial page load; logs will be fetched client-side
    return render_template("index.html")

@app.route("/api/logs")
def get_logs():
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
