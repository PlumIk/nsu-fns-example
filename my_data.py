class MyData:
    __INN = ""
    __PASSWORD = ""
    __CLIENT_SECRET = ""
    __INUSE = 0

    # Создание набора данных
    def __init__(self, INN, PASSWORD, SECRET, INUSE):
        self.__INN = INN
        self.__PASSWORD = PASSWORD
        self.__CLIENT_SECRET = SECRET
        self.__INUSE = INUSE

    # Сохранит, что было использование
    def use(self):
        self.__INUSE += 1;
        return self

    # Получить ИНН, пароль, специальное поле
    def get_inn(self) -> str:
        return self.__INN

    def get_pass(self) -> str:
        return self.__PASSWORD

    def get_sec(self) -> str:
        return self.__CLIENT_SECRET

    # Получить, сколько раз было использовано
    def get_use(self) -> int:
        return self.__INUSE

    # Обнулить использования
    def zero_use(self):
        self.__INUSE = 0

    # Для перегона в json
    def code_me(self):
        return (self.__INN, self.__PASSWORD, self.__CLIENT_SECRET, self.__INUSE)


class MyDataMass:
    __Data = list()

    # Добавить набор в массив
    def append(self, value):
        self.__Data.append(value)

    # Узнать размер массива
    def size(self) -> int:
        return len(self.__Data)

    # Получить i набор данных
    def get_i(self, i):
        return self.__Data[i]

    # Закодировать массив с наборами в json
    def code_me(self):
        ret = list()
        for one in self.__Data:
            ret.append(one.code_me())
        return ret

    # Раскодировать json
    def uncode_me(self, data):
        self.__Data = list()
        for one in data:
            self.__Data.append(MyData(one[0], one[1], one[2], one[3]))

    # Обнулить количество использований всех наборов
    def zero_use(self):
        for one in self.__Data:
            one.zero_use()
