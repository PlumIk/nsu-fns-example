from flask import Flask, jsonify, abort, request
import logging
from datetime import datetime
import os
import re

app = Flask(__name__)


@app.route('/')
@app.route('/foo', methods=['GET'])
def foo():
    return "Foo!"


@app.route('/admin', methods=['GET'])
def admin_page():
    logging.warning('user request admin page')
    return "admin panel"


@app.route('/nuke', methods=['GET'])
def nuke():
    logging.error('we are f*cked')
    return "bombing target. Stand by.."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099)