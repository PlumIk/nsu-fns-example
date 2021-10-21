from flask import abort
from flask import make_response
from flask import request

from flask import Flask, jsonify
from idna import unicode
# curl -i http://localhost:5000/HMC
from nalog_python import NalogRuPython
from worker import Worker

app = Flask(__name__)
work = Worker()


# curl -i -H "Content-Type: application/json" -X GET -d '{"qr":"t=20210506T153900&s=263.50&fn=9960440300049147&i=36086&fp=3305237468&n=1", "id":1}' http://localhost:5000/HMC/qr
@app.route('/HMC/qr', methods=['GET'])
def get_task():
    if not request.json or not 'qr' in request.json or not 'id' in request.json:
        make_response(jsonify({'error': 'Bad input'}), 404)
    work.add_data(request.json['id'], request.json['qr'])
    work.step_inst()
    return jsonify({}), 200


'''
# http://localhost:5000/HMC/1
@app.route('/HMC/<int:task_id>', methods=['GET'])
def get_task(task_id):
    i = 0
    while i < len(tasks):
        if (tasks[i].get('id') == task_id):
            return jsonify({'task': tasks[i]})
        i += 1
    abort(404)


# make_response(jsonify({'error': 'Not found'}), 400)

# http://localhost:5000/HMC
@app.route('/HMC', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# curl -i -H "Content-Type: application/json" -X POST -d '{DATA("title":"Read a book")}' http://localhost:5000/HMC
@app.route('/HMC', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


'''
if __name__ == '__main__':
    app.run(debug=True)
