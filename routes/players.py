# routes/players.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import Session, Player

players_bp = Blueprint('players', __name__, template_folder='../templates')

@players_bp.route('/session/<string:scode>/player/new', methods=['GET', 'POST'])
def new_player(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not (1 <= len(name) <= 20):
            error = "Name must be 1–20 characters."
        elif any(p.name == name for p in sess.players):
            error = "That name is already taken."
        else:
            p = Player.create(name, sess.id)
            return redirect(url_for('players.game', scode=scode, pcode=p.code))

    return render_template('new_player.html', session=sess, error=error)

@players_bp.route('/session/<string:scode>/player/<string:pcode>')
def game(scode, pcode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    Player.query.filter_by(code=pcode, session_id=sess.id).first_or_404()
    return render_template('index.html', scode=scode, pcode=pcode)
