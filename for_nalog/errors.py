# Проблема в _get_ticket_id

class MDataError(ValueError):

    def __init__(self, my_type):
        super()
        self.my_type = my_type

# Проблемы системы
# 0 - не удалось начать сессию
# 1 - кончились данные
class MSystemError(ValueError):

    def __init__(self, my_type):
        super()
        self.my_type = my_type



