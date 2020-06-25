class user:
    id = 0  # идентификатор
    name = ''  # имя
    surname = ''  # фамилия
    schedule = []  # расписание
    time = '00:00'
    settings = {
        'notification': 0,  # уведомление (Да/Нет)
        'combination of weeks': 0,  # совместить расписание в одну неделю (Да/Нет)
        'language': 'us',  # язык
        'UTC': 3
    }

    position = {  # позиция пользователя
        'last message': 0,  # **может не понадобится**
        'week even': False,
        'day': 1
    }

    def __init__(self, id, name, surname):
        self.id = id
        self.name = name
        self.surname = surname
