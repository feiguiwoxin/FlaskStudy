from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_moment import Moment
from flask_login import LoginManager
from config import myconfig
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown

db = SQLAlchemy()
pagedown = PageDown()
moment = Moment()
bootstrap = Bootstrap()
loginmanager = LoginManager()
loginmanager.session_protection = 'basic'
loginmanager.login_view = "auth.login"
loginmanager.login_message = "请先登录，谢谢"
from app.models import AnonymousUser
loginmanager.anonymous_user = AnonymousUser
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(myconfig)

    db.init_app(app)
    pagedown.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app