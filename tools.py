import os
from datetime import datetime, date
import time
from time import strftime
import user
import copy


def set_schedule(name):
    try:
        file = open('temp/' + str(name) + '.txt', 'r', encoding='utf-8')
    except Exception as e:
        answer = []
        return 'Oops! \n' + str(e)

    message = file.read()
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

    file.close()
    os.remove('temp/' + str(name) + '.txt')
    return answer


def get_schedule(id, array):
    file = open('temp/' + str(id) + '.txt', 'w')
    temp = ''

    for i in array:
        for j in i:
            for k in j:
                temp = temp + str(k) + '\n'
            temp = temp + '\n'
        temp = temp + '\n'
    file.write(temp)
    file.close()


def get_even():  # True - Четная; False - Не четная
    date_day = date.today()
    w = datetime(date_day.year, date_day.month, date_day.day)
    w = w.strftime("%d %b %Y")
    d = time.strptime(w, "%d %b %Y")

    if (int(strftime("%U", d)) % 2) == 0:
        return False
    return True


couples_schedule = {
    1: '8:30',
    2: '10:10',
    3: '11:50',
    4: '14:00',
    5: '15:40',
    6: '15:40',
    7: '15:40',
    8: '15:40',
    9: '15:40',
    10: '15:40',
    11: '15:40',
    12: '15:40',
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
    elif change == 'position':
        if parameter == 'last message':
            position['last message'] = value
        elif parameter == 'week even':
            position['week even'] = value
        elif parameter == 'day':
            position['day'] = value

    client = user.user(id=id, name=name, surname=surname, schedule=schedule,
                       time=time, settings=settings, position=position)
    return client
