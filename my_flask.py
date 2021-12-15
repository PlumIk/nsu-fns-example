from flask import Flask, jsonify, abort, request
import logging
from datetime import datetime
import os
from flask import Flask, jsonify

from for_flask import some_fun
from for_flask.worker import Worker

app = Flask(__name__)
work = None

MAX_NUMBER_OF_FILES = 10

PATH = "/var/log/hmc"


@app.route('/HMC/qr', methods=['POST'])
def get_task():
    if not request or not request.json or not 'qr' in request.json or not 'id' in request.json:
        return jsonify({'status': 'Not Acceptable'}), 400
    if not some_fun.qr_true(request.json['qr']):
        return jsonify({'status': 'Unprocessable Entity'}), 422
    work.add_data(request.json['id'], request.json['qr'])
    return jsonify({'status': 'Ok'}), 200


if __name__ == '__main__':
    some_fun.configuration_of_logger(PATH, MAX_NUMBER_OF_FILES, logging.DEBUG)
    work = Worker()
    app.run(host='0.0.0.0', port=8190)
