from app import create_app, db
from app.models import UserModel, TodoModel

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'UserModel': UserModel, 'TodoModel': TodoModel}