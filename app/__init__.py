from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    jwt.init_app(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    from app.routes import api
    app.register_blueprint(api)
    from app.models import RevokeTokens

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokeTokens.is_jti_blacklisted(jti)

    return app

from app import models