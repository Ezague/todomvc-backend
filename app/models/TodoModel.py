from app import db

class TodoModel(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'{self.id} {self.title} {self.completed}'

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }
