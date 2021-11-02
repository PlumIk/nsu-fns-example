import threading

from for_nalog.my_error import My_error
from for_nalog.nalog_python import NalogRuPython


class Worker:

    def __init__(self):
        self.nalog = NalogRuPython()
        self.nalog.set_session_id()
        self.data = dict()
        self.start_timer()

    def add_data(self, inid, qr):
        if self.data.get(inid) is None:
            one = {inid: {
                'qr': qr,
                'iter': 0,
                'time': 0
            }}
            self.data.update(one)

        return

    def do_all_fns(self):
        self.fordel = list()
        self.forupdate = list()
        for key in self.data:
            if self.data.get(key).get('time') <= 0:
                one = self.do_fns(key)
                if one is not None:

                    self.to_back_ok(one, key)

        self.re_in()
        self.del_from()

        return

    def re_in(self):
        for key in self.forupdate:
            self.data.get(key).update({'iter': self.data.get(key).get('iter') + 1})
            if self.data.get(key).get('iter') >= 4:
                self.fordel.append(key)
            else:
                self.data.get(key).update({'time': 10})
            '''
            if self.data.get(key).get('iter') >= 4:
                self.fordel.append(key)
            elif self.data.get(key).get('iter') == 1:
                self.data.get(key).update({'time': 10})
            elif self.data.get(key).get('iter') == 2:
                self.data.get(key).update({'time': 60})
            elif self.data.get(key).get('iter') == 3:
                self.data.get(key).update({'time': 24 * 60})
            '''
        return

    def del_from(self):
        for key in self.fordel:
            self.data.pop(key)

    def to_back_ok(self, info, key):
        ret = dict({'id': key, 'status': 200, 'data': info})
        print('отправил бэку:', ret)
        return

    def to_back_not_ok(self, key, err_type, err_code=0):
        if err_code != 0:
            ret = dict({'id': key, 'status': err_code, 'data': ''})
            print('отправил бэку:', ret)
            return
        print('А чего ты, собственно, ожидал? ', err_type)
        return

    def do_fns(self, key):
        try:
            ret = self.nalog.get_ticket(self.data.get(key).get('qr'))
        except My_error as e:
            if self.data.get(key).get('iter') < 3:
                self.forupdate.append(key)
            else:
                self.to_back_not_ok(key, e.my_type)
                self.fordel.append(key)
            return None
        if ret.get('status') == 1:
            try:
                ret = self.nalog.get_ticket(self.data.get(key).get('qr'))
            except My_error as e:
                if self.data.get(key).get('iter') < 3:
                    self.forupdate.append(key)
                else:
                    self.to_back_not_ok(key, e.my_type)
                    self.fordel.append(key)
                return None
        elif ret.get('status') != 2:
            if self.data.get(key).get('iter') < 3:
                self.forupdate.append(key)
            else:
                self.to_back_not_ok(key, 0, ret.get('status'))
                self.fordel.append(key)
            return None
        self.fordel.append(key)
        return ret

    def step_ten(self):
        for key in self.data:
            self.data.get(key).update({'time': self.data.get(key).get('time') - 10})
        self.do_all_fns()
        # threading.Timer(600, self.step_ten).start()
        threading.Timer(10, self.step_ten).start()

    def step_inst(self):
        threading.Timer(5, self.do_all_fns).start()

    def start_timer(self):
        # threading.Timer(600, self.step_ten).start()
        threading.Timer(10, self.step_ten).start()
