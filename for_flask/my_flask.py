from flask import make_response
from flask import request

from flask import Flask, jsonify

# curl -i http://localhost:5000/HMC
from for_flask.worker import Worker

app = Flask(__name__)
work = Worker()


# curl -i -H "Content-Type: application/json" -X GET -d '{"qr":"t=20210506T153900&s=263.50&fn=9960440300049147&i=36086&fp=3305237468&n=1", "id":1}' http://localhost:5000/HMC/qr
# http://localhost:5000/HMC/qr?id=1&qr=t=20210506T153900&s=263.50&fn=9960440300049147&i=36086&fp=3305237468&n=1
'''
@app.route('/HMC/qr', methods=['GET'])
def get_task():
    id = request.args.get('id')
    qr = request.args.get('qr')
    if id is None or qr is None:
        return jsonify({'error': 'Bad input'}), 404
    work.add_data(id, qr)
    work.step_inst()
    return jsonify({}, 200)
'''
@app.route('/HMC/qr', methods=['GET'])
def get_task():
    if not request.json or not 'qr' in request.json or not 'id' in request.json:
        make_response(jsonify({'error': 'Bad input'}), 404)
    work.add_data(request.json['id'], request.json['qr'])
    work.step_inst()
    return jsonify({}), 200



if __name__ == '__main__':
    app.run(debug=True)
