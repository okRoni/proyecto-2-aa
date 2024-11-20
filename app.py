from flask import Flask, render_template
from src.socketio_setup import app, socketio
from random import randint
import eventlet # eventlet is an asynchronous framework that works with Flask-SocketIO
from src.logic import test_function
from src.entities.player import HumanPlayer
from src.statistics_logger import StatisticsLogger

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start-test')
def start_test(data : dict):
    print('Starting test')
    print(data)
    test_function()

@socketio.on('generate-wins-report')
def generate_wins_report(data: dict):
    logger: StatisticsLogger = StatisticsLogger.get_logger()
    win_percentages: list[float] = logger.get_win_percentage()
    socketio.emit('receive-wins-report', {'win_percentages': win_percentages})

@socketio.on('generate-decisions-report')
def generate_decisions_report(data: dict):
    logger: StatisticsLogger = StatisticsLogger.get_logger()
    success_percentages: list[float] = logger.get_success_percentage()
    socketio.emit('receive-decisions-report', {'success_percentages': success_percentages})

@socketio.on('generate-stand-report')
def generate_stand_report(data: dict):
    logger: StatisticsLogger = StatisticsLogger.get_logger()
    stand_values: list[list[int]] = logger.get_stand_values()
    socketio.emit('receive-stand-report', {
        'croupier': stand_values[0],
        'ai1': stand_values[1],
        'ai2': stand_values[2],
        'human': stand_values[3],
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)