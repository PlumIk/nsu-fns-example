import copy
import threading
import datetime

import requests

from for_nalog.errors import MDataError
from for_nalog.errors import MSystemError
from for_nalog.nalog_python import NalogRuPython


class Worker:

    def __init__(self):
        self.timer_on = False
        self.i_work = True
        self.nalog = NalogRuPython()
        self.ok_data = list()
        self.init_timer()
        try:
            self.nalog.set_session_id()
        except MSystemError as e:
            if e.my_type == 0:
                pass
            else:
                self.i_work = False
        self.data = dict()
        self.data_add = list()
        self.for_del = list()
        self.for_update = list()

    def init_timer(self):
        now = datetime.datetime.now()
        clear_requests = copy.deepcopy(now)
        clear_requests = clear_requests.replace(hour=4, minute=0, second=0)

        if not 0 <= now.hour <= 3:
            clear_requests += datetime.timedelta(days=1)

        remaining = clear_requests - now
        threading.Timer(remaining.total_seconds(), self.clear_requests_count_timer).start()

    def clear_requests_count_timer(self):
        self.nalog.restart_use()

        threading.Timer(86400, self.clear_requests_count_timer).start()  # 24 hours

    def try_to_work(self):
        self.i_work = True
        try:
            self.nalog.set_session_id()
        except MSystemError as e:
            if e.my_type == 0:
                pass
            else:
                self.i_work = False

    def add_data(self, inid, qr):
        if not self.timer_on:
            self.timer_on = True
            self.start_timer()
        if self.data.get(inid) is None:
            one = {inid: {
                'qr': qr,
                'iter': 0,
                'time': 0
            }}
            self.data_add.append(one)
            self.step_inst()
        return

    def do_all_fns(self):
        if self.i_work:
            self.for_del = self.data_add[:]
            self.data_add = list()
            for one in self.for_del:
                self.data.update(one)

            self.for_del = list()
            self.for_update = list()

            work_data = self.data.copy()
            try:
                for key in work_data:
                    if self.data.get(key).get('time') <= 0:
                        one = self.do_fns(key)
                        if one is not None:
                            self.ok_data.append([key, 200, one])

                self.re_in()
                self.del_from()
                self.to_back()
            except MSystemError as e:
                if e.my_type == 0:
                    pass
                else:
                    self.i_work = False

        return

    def re_in(self):
        for key in self.for_update:

            self.data.get(key).update({'iter': self.data.get(key).get('iter') + 1})
            '''
            if self.data.get(key).get('iter') >= 4:
                self.for_del.append(key)
            else:
                self.data.get(key).update({'time': 10})
           '''
            if self.data.get(key).get('iter') >= 4:
                self.for_del.append(key)
            elif self.data.get(key).get('iter') == 1:
                self.data.get(key).update({'time': 10})
            elif self.data.get(key).get('iter') == 2:
                self.data.get(key).update({'time': 60})
            elif self.data.get(key).get('iter') == 3:
                self.data.get(key).update({'time': 24 * 60})

        return

    def del_from(self):
        for key in self.for_del:
            self.data.pop(key)

    def to_back(self):
        c_ok_data = self.ok_data.copy()
        self.ok_data = list()
        url = f'http://3.15.140.143:8080/hmc/api/v1/fns/qr-code-response'
        for one in c_ok_data:
            ret = dict({'id': one[0], 'status': one[1], 'data': one[2]})
            try:
                resp = requests.post(url, json=ret)
                if resp.status_code != 200:
                    self.ok_data.append(one)
            except Exception as e:
                self.ok_data.append(one)
        return

    def do_fns(self, key):
        try:
            ret = self.nalog.get_ticket(self.data.get(key).get('qr'))
        except MDataError as e:
            if self.data.get(key).get('iter') < 3:
                self.for_update.append(key)
            else:
                self.ok_data.append([key, e.my_type, None])
                self.for_del.append(key)
            return None
        if ret.get('status') == 1:
            try:
                ret = self.nalog.get_ticket(self.data.get(key).get('qr'))
            except MDataError as e:
                if self.data.get(key).get('iter') < 3:
                    self.for_update.append(key)
                else:
                    self.ok_data.append([key, e.my_type, None])
                    self.for_del.append(key)
                return None
        elif ret.get('status') != 2:
            if self.data.get(key).get('iter') < 3:
                self.for_update.append(key)
            else:
                self.ok_data.append([key, ret.get('status'), None])
                self.for_del.append(key)
            return None
        self.for_del.append(key)
        return ret

    def do_fns_one(self):
        one = self.data_add.pop()
        key = 1
        for two in one:
            key = two
        try:
            try:
                ret = self.nalog.get_ticket(one.get(key).get('qr'))
            except MDataError as e:
                self.data.update(one)
                return None
            if ret.get('status') == 1:
                try:
                    ret = self.nalog.get_ticket(one.get(key).get('qr'))
                except MDataError as e:
                    self.data.update(one)
                    return None
            elif ret.get('status') != 2:
                self.data.update(one)
                return None
            self.ok_data.append([key, 200, ret])
        except MSystemError as e:
            if e.my_type == 0:
                pass
            else:
                self.i_work = False
        return

    def step_ten(self):
        for key in self.data:
            self.data.get(key).update({'time': self.data.get(key).get('time') - 10})
        self.do_all_fns()
        threading.Timer(600, self.step_ten).start()
        # threading.Timer(10, self.step_ten).start()

    def step_inst(self):
        threading.Timer(5, self.do_fns_one).start()

    def start_timer(self):
        threading.Timer(600, self.step_ten).start()
        # threading.Timer(10, self.step_ten).start()
