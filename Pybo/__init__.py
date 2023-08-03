from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    from . import models

    # 플라스크앱 연결
    app = Flask(__name__)
    # db컨피그
    app.config.from_object(config)

    # db연결
    db.init_app(app)
    migrate.init_app(app, db)

    # 라우트
    from .views import main_views, classification_views, chat_views, question_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(classification_views.bp)
    app.register_blueprint(chat_views.bp)
    app.register_blueprint(question_views.bp)

    return app
