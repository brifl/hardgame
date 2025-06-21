# routes/api.py
from flask import Blueprint, jsonify, request
from models import Session, Player, LogEntry, db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/session/<string:scode>/players')
def get_players(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    return jsonify([{"code": p.code, "name": p.name} for p in sess.players])

@api_bp.route('/session/<string:scode>/player/<string:pcode>/message', methods=['POST'])
def player_message(scode, pcode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    player = Player.query.filter_by(code=pcode, session_id=sess.id).first_or_404()
    content = request.form.get('content', '').strip()
    if content:
        entry = LogEntry(
            role=player.name,
            content=f'<p>{content}</p>',
            session_id=sess.id
        )
        db.session.add(entry)
        db.session.commit()
    return ('', 204)  # no content
