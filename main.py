import datetime
from datetime import datetime, date, timedelta
import time
from time import gmtime, strftime
import telepot
from telebot import types
import telegram.ext
from telegram.ext import Updater
import os

import languages
import user
import tools

u = user.user
u.name = 0
u.schedule = [[['11', '22', '33'], ['21', '32', '43'], ['31', '42', '53'], ['41', '52', '63'], ['51', '62', '73'],
               ['61', '72', '83'], ['71', '82', '93']],
              [['11', '22', '33'], ['21', '32', '43'], ['31', '42', '53'], ['41', '52', '63'], ['51', '62', '73'],
               ['61', '72', '83'], ['71', '82', '93']]]


def daily_schedule(client, w, d):
    answer = ''
    on_account = 0
    #                                    UTC 0                         пользовательский UTC
    localtime = datetime.now() + timedelta(minutes=-180) + timedelta(minutes=client.settings['UTC'] * 60)

    for i in client.schedule[w][d - 1]:
        on_account = on_account + 1
        if localtime.strftime('%H %M') == tools.couples_schedule[on_account]:
            answer = answer + '→' + ' \t '
        else:
            answer = answer + tools.couples_schedule[on_account] + ' \t  '
        answer = answer + str(i) + '\n'
    return answer


def information_line(client, w, d):
    localtime = datetime.now() + timedelta(minutes=-180) + timedelta(minutes=client.settings['UTC'] * 60)
    answer = localtime.strftime('%H:%M') + ' | ' + languages.assembly['week day'][client.settings['language']][d] \
             + ' | ' + languages.assembly['week even'][client.settings['language']][w]
    return answer


print(information_line(u, 1, 1))
