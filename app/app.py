from flask import Flask, request, jsonify, \
    render_template, redirect, url_for
from flask_cors import CORS
from tasks import save_final, save_interim
from celery import Celery
import os


def create_app():
    app = Flask(__name__)
    app.config['CELERY_BROKER_URL'] = os.environ['CELERY_BROKER_URL']
    CORS(app)  # for development only
    return app


app = create_app()
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],
                include=('tasks',))
celery.conf.update(app.config)

#
# @app.route('/')
# def index():
#     # !! TODO("verify token before enabling transcription")
#     return render_template('transcribe.html')


@app.route('/signin', methods=['POST'])
def signin():
    # !! TODO("verify token before enabling transcription")
    verified = True
    if verified:
        return redirect(url_for('transcribe'))
    else:
        return "Failed login", 401


@app.route('/transcribe')
def transcribe():
    # TODO("this should be a protected endpoint")
    return render_template('transcribe.html')


@app.route('/final', methods=['POST'])
def final():
    """ adds a final transcript """
    content = request.json
    final_transcript = content['final']
    print(f'final: {final_transcript}')
    save_final.delay(final_transcript)
    return jsonify({"res": "tbd"}), 200


@app.route('/interim', methods=['POST'])
def interim():
    """ adds an interim transcript """
    content = request.json
    interim_transcript = content['interim']
    save_interim.delay(interim_transcript)
    print(f'interim: {interim_transcript}')
    return jsonify({"res": "tbd"}), 200

