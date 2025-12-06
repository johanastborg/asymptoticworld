from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
import time

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app import routes, models
    app.register_blueprint(routes.bp)

    with app.app_context():
        # Attempt to create tables. In a Cloud Run + gcsfuse env, there might be a delay
        # or transient issues.
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
             db_path = db_uri.replace('sqlite:///', '')
             # Check if directory exists, if not, maybe wait or log warning
             db_dir = os.path.dirname(db_path)
             if not os.path.exists(db_dir):
                 print(f"Warning: Database directory {db_dir} does not exist yet.")

        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
            # Depending on strictness, we might want to fail or retry
            pass

    return app
