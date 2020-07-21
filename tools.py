import os
from datetime import datetime, date
import time
from time import strftime
import user
import copy


def from_text_to_array_schedule(message):
    answer = []
    temp = ''
    temp_d = []
    temp_w = []
    number_of_blank_lines = 0

    for i in message:
        if i == '\n':
            number_of_blank_lines = number_of_blank_lines + 1
            if number_of_blank_lines == 1:  # следущее занятие
                temp_d.append(temp)
                temp = ''
            if number_of_blank_lines == 2:  # следущий день
                temp_w.append(temp_d)
                temp_d = []
            if number_of_blank_lines == 3:  # следущая неделя
                answer.append(temp_w)
                temp_w = []
        else:
            temp = temp + i
            number_of_blank_lines = 0

    n = 0
    while n < 2:
        if not answer:
            answer.append([])
            answer.append([])

        missing = 7 - len(answer[n])
        for j in range(missing):
            answer[n].append([''])
        n += 1


    return answer


def from_file_to_schedule_array(name):
    try:
        file = open('temp/' + str(name) + '.txt', 'r', encoding='utf-8')
    except Exception as e:
        answer = []
        return 'Oops! \n' + str(e)

    message = file.read()

    answer = from_text_to_array_schedule(message)

    file.close()
    os.remove('temp/' + str(name) + '.txt')
    return answer


def get_schedule_text(array):
    answer = ''

    for i in array:
        for j in i:
            for k in j:
                answer += str(k) + '\n'
            answer += '\n'
        answer += '\n'
    return answer


# Создает файл с расписанием пользователя
def make_file_with_schedule(id, array):
    file = open('temp/' + str(id) + '.txt', 'w')

    answer = get_schedule_text(array)

    file.write(answer)
    file.close()


# Из массива в текст
def from_array_to_text(settings):
    answer = ''
    for i in settings.values():
        answer += str(i) + '\n'

    return answer


#   функция перевода из str в bool
def str_to_bool(value):
    return value.lower() in ("yes", "true", "1")


def set_settings(text):
    notification = False,  # уведомление (Да/Нет)
    combination_of_weeks = False,  # совместить расписание в одну неделю (Да/Нет)
    language = 'us'  # язык
    UTC = 0
    Time_instead_of_number = False
    c = 0
    temp = ''
    for i in text:
        if i == '\n':
            c += 1
            if c == 1:  # notification
                notification = str_to_bool(temp)
            elif c == 2:  # combination of weeks
                combination_of_weeks = str_to_bool(temp)
            elif c == 3:  # language
                language = str(temp)
            elif c == 4:  # UTC
                UTC = float(temp)
            elif c == 5:  # Time instead of number
                Time_instead_of_number = str_to_bool(temp)
            temp = ''
        else:
            temp += i
    answer = {
        'notification': notification,  # уведомление (Да/Нет)
        'combination of weeks': combination_of_weeks,  # совместить расписание в одну неделю (Да/Нет)
        'language': language,  # язык
        'UTC': UTC,
        'Time instead of number': Time_instead_of_number
    }

    return answer


def from_text_to_array_position(text):
    last_message = 'null'
    week_even = False
    day = 1
    week = 0
    last_message_id = 0
    last_message_type = 0
    lesson = 0

    c = 0
    temp = ''
    for i in text:
        if i == '\n':
            c += 1
            try:
                if c == 1:  # last message
                    last_message = str(temp)
                elif c == 2:  # week even
                    week_even = str_to_bool(temp)
                elif c == 3:  # day
                    day = int(temp)
                elif c == 4:  # week
                    week = int(temp)
                elif c == 5:  # last message id
                    last_message_id = int(temp)
                elif c == 6:  # last message type
                    last_message_type = int(temp)
                elif c == 7:  # lesson
                    lesson = int(temp)

            except Exception as e:
                print(e)

            temp = ''
        else:
            temp += i

    answer = {  # позиция пользователя
        'last message': last_message,
        'week even': week_even,
        'day': day,
        'week': week,
        'last message id': last_message_id,
        'last message type': last_message_type,
        'lesson': lesson
    }

    return answer


def get_even():  # True - Четная; False - Нечетная
    date_day = date.today()
    w = datetime(date_day.year, date_day.month, date_day.day)
    day_w = w.isoweekday()
    w = w.strftime("%d %b %Y")
    d = time.strptime(w, "%d %b %Y")
    resul = (int(strftime("%U", d)) % 2) == 0
    if day_w == 7:
        return not resul
    return resul


# расписание звонков
couples_schedule = {
    1: '08:30',
    2: '10:10',
    3: '11:50',
    4: '14:00',
    5: '15:40',
    6: '17:20',
    7: '19:00',
    8: '20:40',
    9: '22:20',
    10: '00:00'
}


# находит пользователя в массиве, вырезает его из массива,
# возврящает клон пользователя и массив пользователей без
# этого пользователя
def find_and_cut(array_of_users, user_id):
    array_of_users_copy = copy.deepcopy(array_of_users)
    answer = []
    client = 0
    user_id_array = 0
    for i in array_of_users_copy:
        if i.id == user_id:
            client = copy.deepcopy(array_of_users[user_id_array])
            del array_of_users_copy[user_id_array]
            break
        user_id_array = user_id_array + 1
    answer.append(array_of_users_copy)
    answer.append(client)
    return answer


# возвращает пользователя с изменениями
def people_can_change(user_obj, change, parameter, value):
    id = user_obj.id
    name = user_obj.name
    surname = user_obj.surname
    schedule = user_obj.schedule
    time = user_obj.time
    settings = user_obj.settings
    position = user_obj.position
    del user_obj

    if change == 'id':
        id = value

    elif change == 'name':
        name = value

    elif change == 'surname':
        surname = value

    elif change == 'schedule':
        schedule = value

    elif change == 'time':
        time = value

    elif change == 'settings':
        for i in settings:
            if str(i) == parameter:
                settings[i] = value

    elif change == 'position':
        for i in position:
            if str(i) == parameter:
                position[i] = value

    client = user.user(id=id, name=name, surname=surname, schedule=schedule,
                       time=time, settings=settings, position=position)
    return client
