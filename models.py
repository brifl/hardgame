# models.py
from flask_sqlalchemy import SQLAlchemy
from utils import generate_code

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'session'
    id   = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), unique=True, index=True, nullable=False)
    players = db.relationship('Player', backref='session', lazy=True)
    logs    = db.relationship('LogEntry', backref='session', lazy=True)

    @staticmethod
    def create():
        # generate a unique code
        while True:
            c = generate_code()
            if not Session.query.filter_by(code=c).first():
                break
        s = Session(code=c)
        db.session.add(s)
        db.session.flush()
        # initial system message
        s.logs.append(LogEntry(role='system', content='New game created.'))
        db.session.commit()
        return s

class Player(db.Model):
    __tablename__ = 'player'
    id         = db.Column(db.Integer, primary_key=True)
    code       = db.Column(db.String(6), unique=True, index=True, nullable=False)
    name       = db.Column(db.String(20), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

    @staticmethod
    def create(name, session_id):
        while True:
            c = generate_code()
            if not Player.query.filter_by(code=c).first():
                break
        p = Player(code=c, name=name, session_id=session_id)
        db.session.add(p)
        db.session.commit()
        return p

class LogEntry(db.Model):
    __tablename__ = 'log_entry'
    id         = db.Column(db.Integer, primary_key=True)
    role       = db.Column(db.String(16), nullable=False)    # e.g. 'DM', 'Alice'
    content    = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
