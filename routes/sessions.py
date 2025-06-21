# routes/sessions.py
from flask import Blueprint, redirect, url_for
from models import Session

sessions_bp = Blueprint('sessions', __name__)

@sessions_bp.route("/")
def home():
    return redirect(url_for("sessions.new_session"))

@sessions_bp.route('/session/new')
def new_session():
    s = Session.create()
    return redirect(url_for('players.new_player', scode=s.code))

