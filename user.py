class user:
    id = 0  # идентификатор
    name = ''  # имя
    surname = ''  # фамилия
    schedule = []  # расписание
    time = '00:00'  # время получения ув.
    settings = {}  # настройки
    position = {}  # позиции

    def __init__(self, id=0, name='', surname='', schedule=[[[' '], [' '], [' '], [' '], [' '], [' '], [' ']],
                                                            [[' '], [' '], [' '], [' '], [' '], [' '], [' ']], [[' ']]],
                 time='00:00',
                 settings={
                     'notification': False,  # уведомление (Да/Нет)
                     'combination of weeks': False,  # совместить расписание в одну неделю (Да/Нет)
                     'language': 'us',  # язык
                     'UTC': 3.0,
                     'Time instead of number': False
                 },
                 position={  # позиция пользователя
                     'last message': 'null',
                     'week even': False,  # поменять местами неделю
                     'day': 1,
                     'week': 0,
                     'last message id': 0,
                     'last message type': 'null',
                     'lesson': 0
                 }
                 ):
        self.id = id
        self.name = name
        self.surname = surname
        self.schedule = schedule
        self.time = time
        self.settings = settings
        self.position = position
