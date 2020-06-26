import os
from datetime import datetime, date
import time
from time import strftime


def set_schedule(name):
    try:
        file = open('temp/' + str(name) + '.txt', 'r')
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
    1: '8 30',
    2: '10 10',
    3: '11 50',
    4: '14 00',
    5: '15 40',
}

'''
Пример работы создания файла с расписанием и чтение с автоудалением соответсвенно:
get_schedule(0, [[['11', '22', '33'], ['21', '32', '43'], ['31', '42', '53'], ['41', '52', '63'], ['51', '62', '73'],
                  ['61', '72', '83'], ['71', '82', '93']],
                 [['11', '22', '33'], ['21', '32', '43'], ['31', '42', '53'], ['41', '52', '63'], ['51', '62', '73'],
                  ['61', '72', '83'], ['71', '82', '93']]])
print(set_schedule(0))
'''
