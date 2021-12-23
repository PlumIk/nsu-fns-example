import threading
"""
class One(Exception):
    def al(self):
        print('one')
class Two(Exception):
    def al(self):
        print('two')
class MC:
    def b(self, value:int):
        if(value==1):
            raise One()
        print('no')
        raise Two()
a= [1,2,3]
b=a.pop()
while b:
    print(b)
    if len(a)>0:
        b=a.pop()
    else:
        b=False
dic = dict()
dic.update({1: {2: 2, 3: 3}})
dic.update({2: {2: 2, 3: 3}})
dic.update({3: {2: 2, 3: 3}})
dic.update({4: {2: 2, 3: 3}})
a=MC()
try:
    try:
        a.b(2)
        print(' heho')
    except One as a:
        print('he ')
        a.al()
except Two as a:
    print('hi ')
    a.al()"""

from flask import make_response
from flask import request

from flask import Flask, jsonify

# curl -i http://localhost:5000/HMC

app = Flask(__name__)

# curl -i -H "Content-Type: application/json" -X GET -d '{"qr":"t=20210506T153900&s=263.50&fn=9960440300049147&i=36086&fp=3305237468&n=1", "id":1}' http://localhost:8080/HMC/qr
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


@app.route('/hmc/api/v1/fns/qr-code-response', methods=['POST'])
def get_task():
    print('here :', request.json)
    return jsonify({'data': 'None'}), 200


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080)