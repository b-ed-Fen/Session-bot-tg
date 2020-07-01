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
import copy

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
        # bot.send_message(user_id, 'notification')
        time.sleep(60)


# выбор языка
language_selection = types.InlineKeyboardMarkup()
eng_button = types.InlineKeyboardButton(text="🇺🇸", callback_data='us')
ukr_button = types.InlineKeyboardButton(text="🇺🇦", callback_data='ua')
rus_button = types.InlineKeyboardButton(text="🇷🇺", callback_data='ru')
language_selection.add(eng_button, ukr_button, rus_button)

# соединение недель
connection_weeks = types.InlineKeyboardMarkup()
connection_weeks_yes = types.InlineKeyboardButton(text="🟢", callback_data='connection weeks yes')
connection_weeks_no = types.InlineKeyboardButton(text="⭕", callback_data='connection weeks no')
connection_weeks.add(connection_weeks_no, connection_weeks_yes, )


@bot.message_handler(commands=['start'])
def start(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        client = user.user(id=message.chat.id, name=message.from_user.first_name, surname=message.from_user.last_name)
        users.append(client)

    bot.send_message(message.chat.id,
                     languages.assembly['hi'][client.settings['language']] + ' ' + client.name + '.\n' + \
                     languages.assembly['greeting'][client.settings['language']])

    bot.send_message(message.chat.id,
                     languages.assembly['choose a language'][client.settings['language']],
                     reply_markup=language_selection)


# Сохраняем присланый файл с расписанием
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        global users
        find = tools.find_and_cut(users, message.chat.id)
        client = find[1]

        if client != 0:
            users = find[0]
            chat_id = message.chat.id

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'temp/' + str(chat_id) + '.txt'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, languages.assembly['received'][client.settings['language']])

            client = tools.people_can_change(client, 'schedule', 0, tools.set_schedule(str(chat_id)))
            users.append(client)
        else:
            bot.send_message(message.chat.id,
                             languages.assembly['not in the database']['ua'])

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=['language'])
def language(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ua'])
    else:
        bot.send_message(message.chat.id,
                         languages.assembly['choose a language'][client.settings['language']],
                         reply_markup=language_selection)


@bot.message_handler(commands=['merger'])
def merger(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ua'])
    else:
        bot.send_message(message.chat.id,
                         languages.assembly['joint week'][client.settings['language']], reply_markup=connection_weeks)


@bot.message_handler(commands=['settings'])
def settings(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ua'])
    else:
        languages.client = client
        bot.send_message(message.chat.id,
                         languages.settings(client))


@bot.message_handler(commands=['UTC'])
def settings(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ua'])
    else:
        users = find[0]  # удаление пользователя для его замены
        languages.client = client
        bot.send_message(message.chat.id,
                         languages.assembly['choose a utc'][client.settings['language']])
        client = tools.people_can_change(client, 'position', 'last message', 'utc')
        users.append(client)


@bot.message_handler(content_types=['text'])
def text(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]
    if client != 0:

        if client.position['last message'] == 'utc':

            try:
                client = tools.people_can_change(client, 'settings', 'UTC', float(message.text))
                users = find[0]  # удаление пользователя для его замены
                users.append(client)
                bot.send_message(message.chat.id,
                                 'Готово! Тепер ваш регіон UTC =' + ' ' + str(client.settings['UTC']))
                client = tools.people_can_change(client, 'position', 'last message', 'null')
                users.append(client)

            except Exception as e:
                bot.send_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ua'])


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # поиск пользователя:

    global users
    find = tools.find_and_cut(users, call.message.chat.id)
    client = find[1]

    if client != 0:
        users = find[0]
        # смена языка:
        if call.data == 'us' or call.data == 'ua' or call.data == 'ru':
            past = client.settings['language']
            client = copy.deepcopy(client)
            if call.data == 'us':
                client = tools.people_can_change(client, 'settings', 'language', 'us')
                users.append(client)

            elif call.data == 'ua':
                client = tools.people_can_change(client, 'settings', 'language', 'ua')
                users.append(client)

            elif call.data == 'ru':
                client = tools.people_can_change(client, 'settings', 'language', 'ru')
                users.append(client)

            if call.data != past:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=languages.assembly['choose a language'][client.settings['language']],
                                      reply_markup=language_selection)
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][client.settings['language']])

        # слияние недель
        if call.data == 'connection weeks yes' or call.data == 'connection weeks no':
            past = client.settings['combination of weeks']
            if call.data == 'connection weeks yes':
                client = tools.people_can_change(client, 'settings', 'combination of weeks', True)
                users.append(client)
            elif call.data == 'connection weeks no':
                client = tools.people_can_change(client, 'settings', 'combination of weeks', False)
                users.append(client)

            if call.data != past:
                if call.data == 'connection weeks yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Weeks are the same: True')
                if call.data == 'connection weeks no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Weeks are the same: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][client.settings['language']])
    else:
        bot.send_message(call.message.chat.id,
                         languages.assembly['not in the database']['ua'])


th = threading.Thread(target=notification)
th.daemon = True
th.start()
bot.polling(none_stop=True)
