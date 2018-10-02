from app import app, db
from app.models import User, Post
from subprocess import call
import os

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

port = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
