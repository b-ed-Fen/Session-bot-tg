import os
from datetime import datetime, date
import time
from time import strftime
import user
import copy


def set_schedule_arr(message):
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

    return answer


def set_schedule(name):
    try:
        file = open('temp/' + str(name) + '.txt', 'r', encoding='utf-8')
    except Exception as e:
        answer = []
        return 'Oops! \n' + str(e)

    message = file.read()

    answer = set_schedule_arr(message)

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


def get_schedule(id, array):
    file = open('temp/' + str(id) + '.txt', 'w')

    answer = get_schedule_text(array)

    file.write(answer)
    file.close()


def get_settings(settings):
    answer = ''
    for i in settings.values():
        answer += str(i) + '\n'

    return answer


def get_position(position):
    answer = ''
    for i in position.values():
        answer += str(i) + '\n'

    return answer


def set_settings(text):
    notification = False
    combination_of_weeks = False
    language = 'us'
    UTC = 0
    time_instead_of_number = False
    c = 0
    temp = ''
    for i in text:
        if i == '\n':
            c += 1
            if c == 1:
                notification = bool(temp)
            if c == 2:
                combination_of_weeks = bool(temp)
            if c == 3:
                language = str(temp)
            if c == 4:
                UTC = float(temp)
            if c == 5:
                time_instead_of_number = bool(temp)
            temp = ''
        else:
            temp += i

    answer = {
        'notification': notification,  # уведомление (Да/Нет)
        'combination of weeks': combination_of_weeks,  # совместить расписание в одну неделю (Да/Нет)
        'language': language,  # язык
        'UTC': UTC,
        'Time instead of number': time_instead_of_number
    }

    return answer


def set_position(text):
    last_message = 'null'
    week_even = False
    day = 1
    week = 0
    c = 0
    temp = ''
    for i in text:
        if i == '\n':
            c += 1
            if c == 1:
                last_message = str(temp)
            if c == 2:
                week_even = bool(temp)
            if c == 3:
                day = int(temp)
            if c == 4:
                week = int(temp)
            temp = ''
        else:
            temp += i

    answer = {  # позиция пользователя
        'last message': last_message,
        'week even': week_even,
        'day': day,
        'week': week
    }

    return answer



def get_even():  # True - Четная; False - Не четная
    date_day = date.today()
    w = datetime(date_day.year, date_day.month, date_day.day)
    w = w.strftime("%d %b %Y")
    d = time.strptime(w, "%d %b %Y")

    if (int(strftime("%U", d)) % 2) == 0:
        return False
    return True


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

'''
Пример работы создания файла с расписанием и чтение с автоудалением соответсвенно:
get_schedule(0, [[['11', '22', '33'], ['21', '32', '43'], ['31', '42', '53'], ['41', '52', '63'], ['51', '62', '73'],
                  ['61', '72', '83'], ['71', '82', '93']],
                 [['11', '22', '33'], ['21', '32', '43'], ['31', '42', '53'], ['41', '52', '63'], ['51', '62', '73'],
                  ['61', '72', '83'], ['71', '82', '93']]])
print(set_schedule(0))
'''


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


# возвращает массив пользователей с измененным пользователем
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
        if parameter == 'notification':
            settings['notification'] = value
        elif parameter == 'combination of weeks':
            settings['combination of weeks'] = value
        elif parameter == 'language':
            settings['language'] = value
        elif parameter == 'UTC':
            settings['UTC'] = value
        elif parameter == 'Time instead of number':
            settings['Time instead of number'] = value
    elif change == 'position':
        if parameter == 'last message':
            position['last message'] = value
        elif parameter == 'week even':
            position['week even'] = value
        elif parameter == 'day':
            position['day'] = value
        elif parameter == 'week':
            position['week'] = value

    client = user.user(id=id, name=name, surname=surname, schedule=schedule,
                       time=time, settings=settings, position=position)
    return client
