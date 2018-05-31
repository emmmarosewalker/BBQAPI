from app import db, create_app
from app.models import User, Quality, BBQ

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Quality': Quality,
        'BBQ': BBQ
    }