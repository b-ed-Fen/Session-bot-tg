import datetime
from datetime import datetime, date, timedelta
import time
from time import gmtime, strftime
import telepot
import telebot
from telebot import types
import telegram.ext
from telegram.ext import Updater
import os
import threading

import languages
import user
import tools


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


token = '1206596318:AAH_n8Uz71KIGJHqpv_dFN5fz3aJ15Dkspk'
update = Updater(token, use_context=True)
bot = telebot.TeleBot(token)
job = update.job_queue

users = []


def notification():
    while True:
        bot.send_message(436867541, 'notification')
        time.sleep(60)


# выбор языка
language_selection = types.InlineKeyboardMarkup()
eng_button = types.InlineKeyboardButton(text="🇺🇸", callback_data='us')
ukr_button = types.InlineKeyboardButton(text="🇺🇦", callback_data='ua')
rus_button = types.InlineKeyboardButton(text="🇷🇺", callback_data='ru')
language_selection.add(eng_button, ukr_button, rus_button)


@bot.message_handler(commands=['start'])
def start(message):
    global users

    client = user.user(message.chat.id, message.from_user.first_name, message.from_user.last_name)
    users.append(client)

    bot.send_message(message.chat.id,
                     languages.assembly['hi'][client.settings['language']] + ' ' + client.name + '.\n' + \
                     languages.assembly['greeting'][client.settings['language']], reply_markup=language_selection)


# Сохраняем присланый файл с расписанием
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        user_id_array = 0
        for i in users:
            if i.id == message.chat.id:
                client = users[user_id_array]
                break
            user_id_array = user_id_array + 1

        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'temp/' + str(chat_id) + '.txt'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, languages.assembly['received'][client.settings['language']])

        client.schedule = tools.set_schedule(str(chat_id))
        users[user_id_array] = client
        print(client.schedule)

    except Exception as e:
        bot.reply_to(message, e)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # поиск пользователя:
    user_id_array = 0
    global users
    for i in users:
        if i.id == call.message.chat.id:
            client = users[user_id_array]
            break
        user_id_array = user_id_array + 1

    # смена языка:
    if call.data == 'us' or call.data == 'ua' or call.data == 'ru':
        past = users[user_id_array].settings['language']
        if call.data == 'us':
            users[user_id_array].settings['language'] = 'us'
        elif call.data == 'ua':
            users[user_id_array].settings['language'] = 'ua'
        elif call.data == 'ru':
            users[user_id_array].settings['language'] = 'ru'

        if call.data != past:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=languages.assembly['hi'][
                                           client.settings['language']] + ' ' + client.name + '.\n' + \
                                       languages.assembly['greeting'][client.settings['language']],
                                  reply_markup=language_selection)
        else:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text=languages.assembly['been selected'][client.settings['language']])


th = threading.Thread(target=notification)
th.daemon = True
th.start()
bot.polling(none_stop=True)
