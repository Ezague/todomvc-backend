from flask import jsonify, request
from app.routes import api
from app.models import UserModel, RevokeTokens
from flask_jwt_extended import jwt_required, get_jwt

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = UserModel.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    access_token = user.create_access_token()
    refresh_token = user.create_refresh_token()
    return {'access_token': access_token, 'refresh_token': refresh_token}

@api.route('/logout', methods=['POST'])
@jwt_required()
def revoke_token():
    jti = get_jwt()['jti']
    revoked_token = RevokeTokens(jti=jti)
    try:
        revoked_token.add()
        return {'message': 'Access token has been revoked'}
    except:
        return {'message': 'Something went wrong'}, 500