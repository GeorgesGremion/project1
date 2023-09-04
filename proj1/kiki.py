from app import app, db
from app.models import User, Child


@app.shell_context_processor
def make_shell_context():
        return {'db': db, 'User': User, 'Child': Child}
