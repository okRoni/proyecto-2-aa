from flask import Flask, render_template
from src.socketio_setup import app, socketio
from random import randint
import eventlet # eventlet is an asynchronous framework that works with Flask-SocketIO
from src.logic import test_function

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start-test')
def start_test(data):
    print('Starting test')
    print(data)
    test_function()

if __name__ == '__main__':
    socketio.run(app, debug=True)