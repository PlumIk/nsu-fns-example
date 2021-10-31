class My_error(ValueError):

    def __init__(self, my_type, text='', ex=0):
        super()
        self.my_type = my_type
        self.text = text
        self.ex = ex


"""
Возможные типыЖ
0 - ошибка с возвращаемым кодом
1 - ошибка при установки свзяи с фнс
2 - кончились неиспользованные записи
3 - проблема с ticket_id
"""
