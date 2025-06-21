# routes/api.py
from flask import Blueprint, jsonify, request, Response, abort, render_template, stream_with_context
from models import Session, Player, LogEntry, db
import time

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/session/<string:scode>/logs')
def get_logs(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    entries = (LogEntry.query
               .filter_by(session_id=sess.id)
               .order_by(LogEntry.id)
               .all())
    return jsonify([
        {"role": e.role, "content": e.content}
        for e in entries
    ])

@api_bp.route('/session/<string:scode>/start', methods=['POST'])
def start_game(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    entry = LogEntry(role='DM', content='The adventure begins!', session_id=sess.id)
    db.session.add(entry)
    db.session.commit()
    return ("", 204)

@api_bp.route('/session/<string:scode>/players')
def get_players(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    return jsonify([
        {"code": p.code, "name": p.name}
        for p in sess.players
    ])

@api_bp.route('/session/<string:scode>/player/<string:pcode>/message', methods=['POST'])
def player_message(scode, pcode):
    sess = Session.query.filter_by(code=scode).first_or_404()
    player = Player.query.filter_by(code=pcode, session_id=sess.id).first_or_404()
    content = request.form.get('content', '').strip()
    if not content:
        abort(400, "Empty message")
    entry = LogEntry(
        role=player.name,
        content=f'<p>{content}</p>',
        session_id=sess.id
    )
    db.session.add(entry)
    db.session.commit()
    return ("", 204)

@api_bp.route('/session/<string:scode>/logs/stream')
def stream_logs(scode):
    sess = Session.query.filter_by(code=scode).first_or_404()

    def generate():
        last_id = 0
        while True:
            new_entries = (LogEntry.query
                            .filter_by(session_id=sess.id)
                            .filter(LogEntry.id > last_id)
                            .order_by(LogEntry.id)
                            .all())
            if new_entries:
                for e in new_entries:
                    # render JUST this one entry into HTML
                    snippet = render_template('_logs.html', entries=[e]).strip()
                    # strip out any internal newlines so each event is one data: line
                    snippet = snippet.replace("\n", "")
                    yield f"data: {snippet}\n\n"
                last_id = new_entries[-1].id
            time.sleep(2)

    return Response(stream_with_context(generate()),
                    mimetype='text/event-stream')
