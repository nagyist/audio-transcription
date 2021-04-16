import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'the index page', 200


@app.route('/add', methods=['POST'])
def add():
    """ adds a new transcription """
    pass

