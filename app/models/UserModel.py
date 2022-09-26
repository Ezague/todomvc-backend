from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    todos = db.relationship('TodoModel',
        foreign_keys='TodoModel.user_id',
        backref='user',
        lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_access_token(self):
        return create_access_token(identity=self.id)

    def create_refresh_token(self):
        return create_refresh_token(identity=self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'todos': [todo.serialize() for todo in self.todos]
        }