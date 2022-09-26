from app.routes import api
from app.models import TodoModel, UserModel
from app import db
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

@api.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    user = UserModel.query.get(user_id)
    return {'data': [todo.serialize() for todo in user.todos]}

@api.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    todo = TodoModel(title=data['title'], user_id=user_id, completed=False)
    db.session.add(todo)
    db.session.commit()
    return {'data': todo.serialize(), 'message': 'Todo created successfully'}

@api.route('/todos/<int:id>', methods=['GET'])
@jwt_required()
def get_todo(id):
    user_id = get_jwt_identity()
    todo = TodoModel.query.get_or_404(id)
    if todo.user_id != user_id:
        return {'message': 'You are not authorized to view this todo'}, 401
    return {'data': todo.serialize()}

@api.route('/todos/<int:id>', methods=['PATCH'])
@jwt_required()
def update_todo(id):
    user_id = get_jwt_identity()
    todo = TodoModel.query.get_or_404(id)
    todo.title = request.json.get('title', todo.title)
    todo.completed = request.json.get('completed', todo.completed)
    if todo.user_id != user_id:
        return {'message': 'You are not authorized to update this todo'}, 401
    db.session.add(todo)
    db.session.commit()
    return {'data': todo.serialize(), 'message': 'Todo updated successfully'}

@api.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    user_id = get_jwt_identity()
    todo = TodoModel.query.get_or_404(id)
    if todo.user_id != user_id:
        return {'message': 'You are not authorized to delete this todo'}, 401
    db.session.delete(todo)
    db.session.commit()
    return {'data': todo.serialize(), 'message': 'Todo deleted successfully.'}