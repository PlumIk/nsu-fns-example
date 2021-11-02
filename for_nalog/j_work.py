import json
import random

from for_nalog.my_data import MyDataMass, MyData


class Jwork:

    def __init__(self):

        self.data = MyDataMass()  # Кастом массив данных
        self.end_use = 1  # На каком количестве использований остановиться
        self.last_use = None  # номер последнего использованного набора данных

    # Сохранить текущий массив
    def save_dict(self):
        with open("for_nalog/fns_info.json", "w") as write_file:
            json.dump(self.data.code_me(), write_file, indent=4)

    # Вернуть массив под номером r
    def part_dict(self, r):
        return self.data.get_i(r)

    # Добавить в json новые данные
    def save_new_data(self, inn, password, client_secret):
        self.load_dict()
        self.data.append(MyData(inn, password, client_secret, 0))
        self.save_dict()

    # Некоторые тестовые значения(потом изменить)
    def test_data(self):
        self.save_new_data(111, 'qwerty', 'vegan')
        self.save_new_data(222, 'asdfgh', 'ne vegan')

    # Загрузить массив из json
    def load_dict(self):
        with open("for_nalog/fns_info.json", "r") as read_file:
            self.data.uncode_me(json.load(read_file))

    # Получить массив с данными для установления соединения. Если такого нет, то вернуть None
    def get_inf(self, with_use=False) -> MyData:
        if self.last_use is None:  # такой случай возможен только при установлении соединения или поиске новго набора,
            # поэтому использование не добавляется
            self.last_use = self.get_can_use()
            if self.last_use is None:
                return None  # Нет подходящих наборов
            return self.data.get_i(self.last_use)
        elif not self.try_to_use():  # если набор исчерпал своё количество использований, последний
            # использованный None и мы пытаемся найти новый
            self.last_use = self.get_can_use()
            return self.get_inf(with_use)
        if with_use:
            self.data.get_i(self.last_use).use()
        self.save_dict()
        return self.data.get_i(self.last_use)

    # Проверка, можно ли ещё использовать последний выбранный набор
    def try_to_use(self) -> bool:
        r = self.last_use
        if (self.data.get_i(r).get_use() >= self.end_use):
            return False
        return True

    # Получение номера набора, который можно использовать. Если такого нет, то вернуть None
    def get_can_use(self) -> int:
        self.load_dict()
        myhave = list()
        r = (random.randrange(0, self.data.size(), 1))
        donow = True
        while (self.data.get_i(r).get_use() >= self.end_use and donow):
            myhave.append(r)
            myhave = list(set(myhave))
            if (len(myhave) == self.data.size()):
                donow = False
            r = (random.randrange(0, self.data.size(), 1))

        if (donow):
            return r
        return None

    # Обнулить количество использований
    def zeroed_use(self):
        self.load_dict()
        self.data.zero_use()
        self.save_dict()

    # Обнулить количество использований всех данных
    def do_empty(self):
        self.data = MyDataMass()
        self.save_dict()
