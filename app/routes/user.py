from app.routes import api
from app.models import UserModel
from app import db
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = UserModel.query.all()
    return {'users': [user.serialize() for user in users]}

@api.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    userid = get_jwt_identity()
    user = UserModel.query.get_or_404(id)
    if user.id != userid:
        return {'message': 'You are not authorized to view this user'}, 401
    return {'data': user.serialize()}

@api.route('/users/<int:id>/todos', methods=['GET'])
@jwt_required()
def get_user_todos(id):
    userid = get_jwt_identity()
    user = UserModel.query.get_or_404(id)
    if user.id != userid:
        return {'message': 'You are not authorized to view this user'}, 401
    return {'data': [todo.serialize() for todo in user.todos]}

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserModel(username=data['username'])
    user.set_password(data['password'])

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as error:
        return { "message", "Username already exists" }, 400
    finally:
        db.session.rollback()

    return {'data': user.serialize(), 'message': 'User created successfully'}

@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    userid = get_jwt_identity()
    user = UserModel.query.get_or_404(id)
    if user.id != userid:
        return {'message': 'You are not authorized to delete this user'}, 401
    db.session.delete(user)
    db.session.commit()
    return {'data': user.serialize(), 'message': 'User deleted successfully.'}