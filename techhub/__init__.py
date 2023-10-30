from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from techhub.models import db

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile("config.py", silent=True)
    db.init_app(app)
    migrate = Migrate(app,db)
    socketio = SocketIO(app)
    csrf.init_app(app)
    return app, socketio
app, socketio = create_app()




from techhub import admin_routes, user_routes
from techhub.forms import *
