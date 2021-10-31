class My_error(ValueError):

    def __int__(self, what):
        super()
        self.my_type = what

    def __init__(self, text, ex):
        super()
        self.my_type = 0
        self.text = text
        self.ex = ex



"""
Возможные типыЖ
0 - ошибка с возвращаемым кодом
1 - ошибка при установки свзяи с фнс
2 - кончились неиспользованные записи
"""