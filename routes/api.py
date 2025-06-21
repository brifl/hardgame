# routes/api.py
from flask import Blueprint, jsonify
from models import Session, LogEntry, db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/session/<string:scode>/logs')
def get_logs(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    entries = LogEntry.query.filter_by(session_id=sess.id).order_by(LogEntry.id).all()
    return jsonify([{"role": e.role, "content": e.content} for e in entries])

@api_bp.route('/session/<string:scode>/start', methods=['POST'])
def start_game(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    entry = LogEntry(role='DM', content='The adventure begins!', session_id=sess.id)
    db.session.add(entry)
    db.session.commit()
    return ""  # htmx will swap out the button
