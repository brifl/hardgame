# app.py
from flask import Flask
from models import db
from routes.sessions import sessions_bp
from routes.players import players_bp
from routes.api import api_bp

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY="dev",  # override via instance/config in prod
        SQLALCHEMY_DATABASE_URI="sqlite:///rpg.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # init extensions
    db.init_app(app)

    # register blueprints
    app.register_blueprint(sessions_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(api_bp)

    # ensure DB exists
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
