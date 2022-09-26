from logging import basicConfig
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import UserModel

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = UserModel.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False
    return True

@token_auth.verify_token
def verify_token(token):
    user = UserModel.check_token(token) if token else None
    return user is not None