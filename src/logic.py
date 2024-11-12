from random import choice, randint
from .socketio_setup import socketio
import eventlet

def test_function():
    for i in range(10):
        randomNumber = randint(1, 100)
        print(randomNumber)
        socketio.emit('update', randomNumber)
        eventlet.sleep(0.5)