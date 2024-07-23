from flask import Flask
from .config import Config
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from .routes import attendance
        app.register_blueprint(attendance.bp)
        
        db.create_all()

    return app
