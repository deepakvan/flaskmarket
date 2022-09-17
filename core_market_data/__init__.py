from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
loginmanager=LoginManager()

db = SQLAlchemy()
bcrypt=Bcrypt()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hellohello123@'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market.db"
    db.init_app(app)
    bcrypt.init_app(app)
    loginmanager.init_app(app)



    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(views, url_prefix="/")

    from .models import Items,User
    create_database(app)

    @loginmanager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    loginmanager.login_view='auth.login_page'
    loginmanager.login_message_category='info'

    return app


def create_database(app):
    if not os.path.exists('core_market_data//market.db'):
        db.create_all(app=app)
        print("Db Created")