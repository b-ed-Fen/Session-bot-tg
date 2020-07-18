import copy
import datetime
import threading
import time
from datetime import datetime, date, timedelta
import os

import telebot
from telebot import types

import connection
import languages
import tools
import user


def daily_schedule(client=user.user(), w=0, d=1, arrow=False, choice=False):
    try:
        if client.position['week even']:
            w = 1 if w == 0 else 0

        if client.settings['combination of weeks']:
            w = 0

        answer = ''
        on_account = 0
        #               UTC 0                         пользовательский UTC
        localtime = datetime.now() + timedelta(minutes=client.settings['UTC'] * 60)

        for i in client.schedule[w][d - 1]:
            on_account = on_account + 1
            if client.settings['Time instead of number']:

                # Выбор, тогда не стрелка и не время
                if choice and (on_account == client.position['lesson']):
                    answer = answer + '        ● ' + ' \t '

                # Стрелка тогда не время
                elif (tools.couples_schedule[on_account] <= localtime.strftime('%H:%M') < tools.couples_schedule[on_account + 1]) and arrow:

                    answer = answer + '      → ' + ' \t '

                # Время
                else:
                    answer = answer + tools.couples_schedule[on_account] + ' \t  '

            # Номер занятия
            else:
                if choice and (on_account == client.position['lesson']):
                    answer = answer + ' ●   ' + ' \t '
                else:
                    answer = answer + str(on_account) + ':  ' + ' \t  '

            answer = answer + str(i) + '\n'
    except Exception as e:
        answer = 'Wowps! We had a problem reading your schedule, I only know that: ' + str(e)
        if str(e) == 'list index out of range':
            answer = languages.assembly['no schedule'][client.settings['language']]

    return answer


def information_line(client=user.user(), w=0, d=1, message=''):
    if client.position['week even']:
        w = 1 if w == 0 else 0
    #               UTC 0                         пользовательский UTC
    localtime = datetime.now() + timedelta(minutes=client.settings['UTC'] * 60)

    answer = localtime.strftime('%H:%M') if message == '' else str(message)
    answer += ' | ' + languages.assembly['week day'][client.settings['language']][d]

    if not client.settings['combination of weeks']:
        answer += ' | ' + languages.assembly['week even'][client.settings['language']][w]

    return answer


def information_line_daily(client, w, d):
    if client.position['week even']:
        w = 1 if w == 0 else 0

    answer = languages.assembly['wish of the day'][client.settings['language']][d] + ', ' + client.name
    if not client.settings['combination of weeks']:
        answer += ' | ' + languages.assembly['week even'][client.settings['language']][w]

    return answer


token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)
users = connection.get_array_user()


def notification():
    while True:
        time.sleep(60)
        for client in users:
            #               UTC 0                         пользовательский UTC
            localtime = datetime.now() + timedelta(minutes=client.settings['UTC'] * 60)
            if client.settings['notification'] and client.time == localtime.strftime('%H:%M'):
                bot.send_message(client.id,
                                 information_line_daily(client, int(tools.get_even()), datetime.today().isoweekday()) +
                                 '\n' + daily_schedule(client, int(tools.get_even()), datetime.today().isoweekday()))

            try:
                if client.position['last message type'] == 1:  # обновление сообщения today
                    bot.edit_message_text(chat_id=client.id,
                                          message_id=client.position['last message id'],
                                          text=information_line(client, int(tools.get_even()),
                                                                datetime.today().isoweekday()) +
                                               '\n' + daily_schedule(client, int(tools.get_even()),
                                                                     datetime.today().isoweekday()))
            except Exception as e:
                print(f' *** {client.id} Old version of settings!')


def data_update():
    while True:
        time.sleep(1800)
        connection.Update(users)
        print('database has been updated')


# выбор языка
language_selection = types.InlineKeyboardMarkup()
eng_button = types.InlineKeyboardButton(text="🇺🇸", callback_data='us')
ukr_button = types.InlineKeyboardButton(text="🇺🇦", callback_data='ua')
rus_button = types.InlineKeyboardButton(text="🇷🇺", callback_data='ru')
language_selection.add(eng_button, ukr_button, rus_button)

# кнопки расписания
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/yesterday', '/today', '/tomorrow')
keyboard.row('/week')


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
                     languages.assembly['greeting'][client.settings['language']], reply_markup=keyboard)

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

            client = tools.people_can_change(client, 'schedule', 0, tools.from_file_to_schedule_array(str(chat_id)))
            users.append(client)
        else:
            bot.send_message(message.chat.id,
                             languages.assembly['not in the database']['ru'])

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=['language'])
def language(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        bot.send_message(message.chat.id,
                         languages.assembly['choose a language'][client.settings['language']],
                         reply_markup=language_selection)


@bot.message_handler(commands=['merger'])
def merger(message):
    # соединение недель

    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        connection_weeks = types.InlineKeyboardMarkup()
        connection_weeks_yes = types.InlineKeyboardButton(text=languages.assembly['yes'][client.settings['language']],
                                                          callback_data='connection weeks yes')
        connection_weeks_no = types.InlineKeyboardButton(text=languages.assembly['no'][client.settings['language']],
                                                         callback_data='connection weeks no')
        connection_weeks.add(connection_weeks_no, connection_weeks_yes, )
        bot.send_message(message.chat.id,
                         languages.assembly['joint week'][client.settings['language']], reply_markup=connection_weeks)


@bot.message_handler(commands=['inverting'])
def inverting(message):
    # поменять недели местами

    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        connection_weeks = types.InlineKeyboardMarkup()
        connection_weeks_yes = types.InlineKeyboardButton(text=languages.assembly['yes'][client.settings['language']],
                                                          callback_data='swap schedule yes')
        connection_weeks_no = types.InlineKeyboardButton(text=languages.assembly['no'][client.settings['language']],
                                                         callback_data='swap schedule no')
        connection_weeks.add(connection_weeks_no, connection_weeks_yes, )

        bot.send_message(message.chat.id,
                         languages.assembly['swap schedule'][client.settings['language']],
                         reply_markup=connection_weeks)


@bot.message_handler(commands=['notification'])
def notification_ui(message):
    # включить увидомления
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        connection_weeks = types.InlineKeyboardMarkup()
        connection_weeks_yes = types.InlineKeyboardButton(text=languages.assembly['yes'][client.settings['language']],
                                                          callback_data='notification on yes')
        connection_weeks_no = types.InlineKeyboardButton(text=languages.assembly['no'][client.settings['language']],
                                                         callback_data='notification on no')
        connection_weeks.add(connection_weeks_no, connection_weeks_yes, )

        bot.send_message(message.chat.id,
                         languages.assembly['notification'][client.settings['language']],
                         reply_markup=connection_weeks)


@bot.message_handler(commands=['settings'])
def settings(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        languages.client = client
        bot.send_message(message.chat.id,
                         languages.settings(client))


@bot.message_handler(commands=['UTC'])
def utc(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        users = find[0]  # удаление пользователя для его замены
        bot.send_message(message.chat.id,
                         languages.assembly['choose a utc'][client.settings['language']])
        client = tools.people_can_change(client, 'position', 'last message', 'utc')
        users.append(client)


@bot.message_handler(commands=['yesterday'])
def yesterday(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]
    w = int(tools.get_even())
    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        if date.today().isoweekday() == 1:
            w = int(not tools.get_even())

        bot.send_message(message.chat.id,
                         information_line(client, w,
                                          (date.today() - timedelta(days=1)).isoweekday()) + '\n' +
                         daily_schedule(client, w,
                                        (date.today() - timedelta(days=1)).isoweekday()))


@bot.message_handler(commands=['today'])
def today(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        mes = bot.send_message(message.chat.id,
                               information_line(client, int(tools.get_even()), datetime.today().isoweekday()) + '\n' +
                               daily_schedule(client, int(tools.get_even()), datetime.today().isoweekday(), arrow=True))
        users = find[0]
        client = tools.people_can_change(client, 'position', 'last message id', mes.message_id)
        client = tools.people_can_change(client, 'position', 'last message type', 1)
        users.append(client)


@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]
    w = int(tools.get_even())

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        if date.today().isoweekday() == 7:
            w = int(not tools.get_even())

        bot.send_message(message.chat.id,
                         information_line(client, w,
                                          (date.today() + timedelta(days=1)).isoweekday()) + '\n' +
                         daily_schedule(client, w,
                                        (date.today() + timedelta(days=1)).isoweekday()))


@bot.message_handler(commands=['week'])
def week_ui(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        navigation = types.InlineKeyboardMarkup()
        week_back = types.InlineKeyboardButton(text='<', callback_data='week back')
        week_forward = types.InlineKeyboardButton(text='>', callback_data='week forward')
        navigation.add(week_back, week_forward)

        if not client.settings['combination of weeks']:
            week_another = types.InlineKeyboardButton(
                text=languages.assembly['another'][client.settings['language']],
                callback_data='week another')
            navigation.add(week_another)

        bot.send_message(message.chat.id,
                         information_line(client, client.position['week'], client.position['day']) + '\n' +
                         daily_schedule(client, client.position['week'], client.position['day']),
                         reply_markup=navigation)


def edit_day_week(client=user.user(), message_id=0):
    global users
    navigation = types.InlineKeyboardMarkup()
    messageid = 0
    if client.position['edit']:  # вносим изменения
        week_up = types.InlineKeyboardButton(text='↑', callback_data='edit up')
        week_down = types.InlineKeyboardButton(text='↓', callback_data='edit down')
        week_add_b = types.InlineKeyboardButton(text=languages.assembly['e add']['add b'][client.settings['language']],
                                                callback_data='edit add before')
        week_add_a = types.InlineKeyboardButton(text=languages.assembly['e add']['add a'][client.settings['language']],
                                                callback_data='edit add after')
        week_del = types.InlineKeyboardButton(text=languages.assembly['del'][client.settings['language']],
                                              callback_data='edit delete')
        edit_day = types.InlineKeyboardButton(
            text=languages.assembly['back to day selection'][client.settings['language']],
            callback_data='edit day')

        navigation.add(week_up, week_add_b)
        navigation.add(week_down, week_add_a)
        navigation.add(week_del)
        navigation.add(edit_day)
        if message_id == 0:
            mes = bot.send_message(client.id,
                                   text=information_line(client,
                                                         client.position['week'],
                                                         client.position['day'],
                                                         message=languages.assembly['editing'][
                                                             client.settings['language']]) + '\n'
                                        + daily_schedule(client,
                                                         client.position['week'],
                                                         client.position['day'],
                                                         choice=True),
                                   reply_markup=navigation)
            messageid = mes.message_id
        else:
            bot.edit_message_text(chat_id=client.id,
                                  message_id=message_id,
                                  text=information_line(client,
                                                        client.position['week'],
                                                        client.position['day'],
                                                        message=languages.assembly['editing'][
                                                            client.settings['language']]) + '\n'
                                       + daily_schedule(client,
                                                        client.position['week'],
                                                        client.position['day'],
                                                        choice=True),
                                  reply_markup=navigation)


    else:  # выбор дня для редактирования
        week_back = types.InlineKeyboardButton(text='<', callback_data='edit back')
        week_forward = types.InlineKeyboardButton(text='>', callback_data='edit forward')
        edit_day = types.InlineKeyboardButton(text=languages.assembly['edit this day'][client.settings['language']],
                                              callback_data='edit day')
        navigation.add(week_back, week_forward)

        if not client.settings['combination of weeks']:
            week_another = types.InlineKeyboardButton(
                text=languages.assembly['another'][client.settings['language']],
                callback_data='edit another')
            navigation.add(week_another)

        navigation.add(edit_day)

        if message_id == 0:
            mes = bot.send_message(client.id,
                                   information_line(client, client.position['week'], client.position['day']) + '\n' +
                                   daily_schedule(client, client.position['week'], client.position['day']),
                                   reply_markup=navigation)
            messageid = mes.message_id
        else:
            bot.edit_message_text(chat_id=client.id,
                                  message_id=message_id,
                                  text=information_line(client,
                                                        client.position['week'],
                                                        client.position['day']) + '\n'
                                       + daily_schedule(client,
                                                        client.position['week'],
                                                        client.position['day'],
                                                        choice=True),
                                  reply_markup=navigation)
        if messageid != 0:
            temp = tools.find_and_cut(users, client.id)
            users = temp[0]
            client = tools.people_can_change(client, 'position', 'last message', messageid)
            users.append(client)


@bot.message_handler(commands=['edit'])
def week_ui(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        edit_day_week(client)


@bot.message_handler(commands=['time'])
def time_ui(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        users = find[0]  # удаление пользователя для его замены
        bot.send_message(message.chat.id, languages.assembly['enter time'][client.settings['language']])
        client = tools.people_can_change(client, 'position', 'last message', 'time')
        users.append(client)


@bot.message_handler(commands=['help'])
def help_ui(message):
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        bot.send_message(message.chat.id, languages.assembly['help'][client.settings['language']])


@bot.message_handler(commands=['template'])
def help_ui(message):
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        doc = open('temp/Шаблон расписания.txt', 'rb')
        bot.send_document(message.chat.id, doc)
        doc.close()


@bot.message_handler(commands=['doc'])
def steam_document(message):
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        tools.make_file_with_schedule(client.id, client.schedule)
        doc = open(f'temp/{client.id}.txt', 'rb')
        bot.send_document(message.chat.id, doc)
        doc.close()
        os.remove(f'temp/{client.id}.txt')


@bot.message_handler(commands=['torn'])
def torn_ui(message):
    # включить увидомления
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        torn = types.InlineKeyboardMarkup()
        torn_yes = types.InlineKeyboardButton(text=languages.assembly['yes'][client.settings['language']],
                                              callback_data='torn on yes')
        torn_no = types.InlineKeyboardButton(text=languages.assembly['no'][client.settings['language']],
                                             callback_data='torn on no')
        torn.add(torn_no, torn_yes)

        bot.send_message(message.chat.id,
                         languages.assembly['torn'][client.settings['language']],
                         reply_markup=torn)


@bot.message_handler(content_types=['text'])
def text(message):
    global users
    find = tools.find_and_cut(users, message.chat.id)
    client = find[1]

    if client != 0:

        # установить utc
        if client.position['last message'] == 'utc':
            try:
                client = tools.people_can_change(client, 'settings', 'UTC', float(message.text))
                users = find[0]  # удаление пользователя для его замены
                bot.send_message(message.chat.id,
                                 languages.assembly['done utc'][client.settings['language']] + ' ' +
                                 str(client.settings['UTC']) + '.')
                client = tools.people_can_change(client, 'position', 'last message', 'null')
                users.append(client)

            except Exception as e:
                bot.send_message(message.chat.id, str(e))

        # установить время
        if client.position['last message'] == 'time':
            try:
                time_clock = datetime.strptime(str(message.text), '%H:%M').time()  # если что-то пойдет не так то
                # выкенет Exception

                client = tools.people_can_change(client, 'time', 0, time_clock.strftime('%H:%M'))
                users = find[0]  # удаление пользователя для его замены
                bot.send_message(message.chat.id,
                                 languages.assembly['done time'][client.settings['language']] + ' ' + str(client.time))
                client = tools.people_can_change(client, 'position', 'last message', 'null')
                users.append(client)

            except Exception as e:
                bot.send_message(message.chat.id, str(e))

        # меняем занятие
        if client.position['edit']:
            try:
                temp = client.schedule
                temp[client.position['week']][client.position['day'] - 1][client.position['lesson'] - 1] = message.text
                client = tools.people_can_change(client, 'schedule', 0, temp)
                users = find[0]  # удаление пользователя для его замены
                users.append(client)
                edit_day_week(client, client.position['last message'])
                bot.delete_message(message.chat.id, message.message_id)

            except Exception as e:
                bot.send_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])


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

        # поменять местами расписание
        if call.data == 'swap schedule yes' or call.data == 'swap schedule no':
            past = client.position['week even']
            if call.data == 'swap schedule yes':
                client = tools.people_can_change(client, 'position', 'week even', True)
                users.append(client)
            elif call.data == 'swap schedule no':
                client = tools.people_can_change(client, 'position', 'week even', False)
                users.append(client)

            if call.data != past:
                if call.data == 'swap schedule yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Parity and non-parity have changed: True')
                if call.data == 'swap schedule no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Parity and non-parity have changed: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][client.settings['language']])

        # включить уведомления
        if call.data == 'notification on yes' or call.data == 'notification on no':
            past = client.settings['notification']
            if call.data == 'notification on yes':
                client = tools.people_can_change(client, 'settings', 'notification', True)
                users.append(client)
            elif call.data == 'notification on no':
                client = tools.people_can_change(client, 'settings', 'notification', False)
                users.append(client)

            if call.data != past:
                if call.data == 'notification on yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Notifications are included: True')
                if call.data == 'notification on no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Notifications are included: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][client.settings['language']])
        # расписание на неделю
        if call.data == 'week another' or call.data == 'week back' or call.data == 'week forward':
            if call.data == 'week another':
                if client.position['week'] == 0:
                    client = tools.people_can_change(client, 'position', 'week', 1)
                else:
                    client = tools.people_can_change(client, 'position', 'week', 0)

            if call.data == 'week back':
                if client.position['day'] == 1:
                    client = tools.people_can_change(client, 'position', 'day', 7)
                else:
                    client = tools.people_can_change(client, 'position', 'day', client.position['day'] - 1)

            if call.data == 'week forward':
                if client.position['day'] == 7:
                    client = tools.people_can_change(client, 'position', 'day', 1)
                else:
                    client = tools.people_can_change(client, 'position', 'day', client.position['day'] + 1)

            navigation = types.InlineKeyboardMarkup()  # пересобираем навигацию
            week_back = types.InlineKeyboardButton(text='<', callback_data='week back')
            week_forward = types.InlineKeyboardButton(text='>', callback_data='week forward')
            navigation.add(week_back, week_forward)

            if not client.settings['combination of weeks']:
                week_another = types.InlineKeyboardButton(
                    text=languages.assembly['another'][client.settings['language']],
                    callback_data='week another')
                navigation.add(week_another)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=information_line(client, client.position['week'],
                                                        client.position['day']) + '\n' +
                                       daily_schedule(client, client.position['week'], client.position['day']),
                                  reply_markup=navigation)
            users.append(client)

        # управление edit week
        if call.data[:4] == 'edit':

            if call.data == 'edit another':
                if client.position['week'] == 0:
                    client = tools.people_can_change(client, 'position', 'week', 1)
                else:
                    client = tools.people_can_change(client, 'position', 'week', 0)

            if call.data == 'edit back':
                if client.position['day'] == 1:
                    client = tools.people_can_change(client, 'position', 'day', 7)
                else:
                    client = tools.people_can_change(client, 'position', 'day', client.position['day'] - 1)

            if call.data == 'edit forward':
                if client.position['day'] == 7:
                    client = tools.people_can_change(client, 'position', 'day', 1)
                else:
                    client = tools.people_can_change(client, 'position', 'day', client.position['day'] + 1)

            if call.data == 'edit day':
                client = tools.people_can_change(client, 'position', 'lesson', 0) if client.position['edit'] \
                    else tools.people_can_change(client, 'position', 'lesson', 1)
                client = tools.people_can_change(client, 'position', 'edit', not client.position['edit'])

            if call.data == 'edit up':
                if client.position['lesson'] > 1:
                    client = tools.people_can_change(client, 'position', 'lesson', client.position['lesson'] - 1)
                else:
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='negative value is impossible!')
                    users.append(client)
                    return

            if call.data == 'edit down':
                if client.position['lesson'] < len(
                        client.schedule[client.position['week']][client.position['day'] - 1]):
                    client = tools.people_can_change(client, 'position', 'lesson', client.position['lesson'] + 1)
                else:
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='There is nothing further :3')
                    users.append(client)
                    return

            if call.data == 'edit add before':
                temp = client.schedule
                temp_b = client.schedule[client.position['week']][client.position['day'] - 1]
                temp_b.reverse()
                temp_a = temp_b[: (len(temp_b) - (client.position['lesson'] - 1))]
                temp_b.reverse()
                temp_a.reverse()
                temp_b = temp_b[:client.position['lesson'] - 1]
                temp_b.append(' ')

                temp[client.position['week']][client.position['day'] - 1] = temp_b + temp_a
                client = tools.people_can_change(client, 'schedule', 0, temp)
                client = tools.people_can_change(client, 'position', 'lesson', client.position['lesson'] + 1)

            if call.data == 'edit add after':
                temp = client.schedule
                temp_b = client.schedule[client.position['week']][client.position['day'] - 1]
                temp_b.reverse()
                temp_a = temp_b[: (len(temp_b) - (client.position['lesson']))]
                temp_b.reverse()
                temp_a.reverse()
                temp_b = temp_b[:client.position['lesson']]
                temp_b.append(' ')

                temp[client.position['week']][client.position['day'] - 1] = temp_b + temp_a
                client = tools.people_can_change(client, 'schedule', 0, temp)

            if call.data == 'edit delete':
                temp = client.schedule
                del temp[client.position['week']][client.position['day'] - 1][client.position['lesson'] - 1]
                client = tools.people_can_change(client, 'schedule', 0, temp)

            users.append(client)

            edit_day_week(client, message_id=call.message.message_id)  # сборка расписания

        # Время вместо цифр в расписании
        if call.data == 'torn on no' or call.data == 'torn on yes':
            past = client.settings['Time instead of number']
            if call.data == 'torn on yes':
                client = tools.people_can_change(client, 'settings', 'Time instead of number', True)

            elif call.data == 'torn on no':
                client = tools.people_can_change(client, 'settings', 'Time instead of number', False)

            users.append(client)

            if call.data != past:
                if call.data == 'torn on yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Time instead of number: True')
                if call.data == 'torn on no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Time instead of number: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][client.settings['language']])

    else:
        bot.send_message(call.message.chat.id,
                         languages.assembly['not in the database']['ru'])


th_notigic = threading.Thread(target=notification)
th_db = threading.Thread(target=data_update)

th_notigic.daemon = True
th_notigic.start()

th_db.daemon = True
th_db.start()

bot.polling(none_stop=True)
