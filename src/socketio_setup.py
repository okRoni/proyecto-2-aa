from flask import Flask
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__, template_folder='../templates', static_folder='../static')
socketio = SocketIO(app, async_mode='eventlet')