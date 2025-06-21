from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import secrets

# remove ambiguous chars: no 0, O, 1, l, I
ALPHABET = "23456789abcdefghjkmnpqrstuvwxyz"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Models
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logs = db.relationship('LogEntry', backref='session', lazy=True)
    players = db.relationship('Player', backref='session', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(16), nullable=False)        # e.g. "system", "DM", "Alice"
    content = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

# --- Create DB tables once
@app.before_first_request
def init_db():
    db.create_all()

# --- 1) Create new session
@app.route('/session/new')
def new_session():
    s = Session()
    db.session.add(s)
    db.session.commit()
    # initial log
    entry = LogEntry(role='system', content='New game created.', session_id=s.id)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('new_player', sid=s.id))

# --- 2) Name a player in a session
@app.route('/session/<int:sid>/player/new', methods=['GET','POST'])
def new_player(sid):
    sess = Session.query.get_or_404(sid)
    error = None

    if request.method == 'POST':
        name = request.form.get('name','').strip()
        # basic validation
        if not (1 <= len(name) <= 20):
            error = "Name must be 1–20 characters."
        elif Player.query.filter_by(session_id=sid, name=name).first():
            error = "That name is already taken."
        else:
            p = Player(name=name, session_id=sid)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('game', sid=sid, pid=p.id))

    return render_template('new_player.html', session=sess, error=error)

# --- 3) Game view (empty for now except log + “Start game” button)
@app.route('/session/<int:sid>/player/<int:pid>')
def game(sid, pid):
    # ensure both exist
    Session.query.get_or_404(sid)
    Player.query.get_or_404(pid)
    return render_template('index.html', sid=sid, pid=pid)

# --- 4) API: fetch logs for a session
@app.route('/api/session/<int:sid>/logs')
def get_logs(sid):
    Session.query.get_or_404(sid)
    entries = LogEntry.query.filter_by(session_id=sid).order_by(LogEntry.id).all()
    return jsonify([
        {"role": e.role, "content": e.content}
        for e in entries
    ])

@app.route('/api/session/<int:sid>/start', methods=['POST'])
def start_game(sid):
    Session.query.get_or_404(sid)
    entry = LogEntry(role='DM', content='The adventure begins!', session_id=sid)
    db.session.add(entry)
    db.session.commit()
    return ""  # triggers htmx to remove the button

if __name__ == '__main__':
    app.run(debug=True)
