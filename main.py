import datetime
import os
import threading
import time
from datetime import datetime, date, timedelta

import telebot
from telebot import types

import connection
import languages
import tools
import user

token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)
users = connection.get_array_user()


def daily_schedule(client=user.user(), w=0, d=1, arrow=False, choice=False, week_even_ignore=False):
    try:
        if client.position['week even'] and not week_even_ignore:
            w = 1 if w == 0 else 0

        if client.settings['combination of weeks']:
            w = 0

        answer = ''
        on_account = 0
        #               UTC 0                         пользовательский UTC
        localtime = datetime.now() + timedelta(minutes=client.settings['UTC'] * 60)

        for i in client.schedule[w][d - 1]:
            on_account = on_account + 1                                                     # длинна массива со временем
            if client.settings['Time instead of number'] and len(client.schedule[w][d - 1]) < len(client.couples_schedule):

                # Выбор, тогда не стрелка и не время
                if choice and (on_account == client.position['lesson']):
                    answer = answer + '        ● ' + ' \t '

                # Стрелка тогда не время
                elif (client.couples_schedule[on_account] <= localtime.strftime('%H:%M') < client.couples_schedule[
                    on_account + 1]) and arrow:

                    answer = answer + '      → ' + ' \t '

                # Время
                else:
                    answer = answer + client.couples_schedule[on_account] + ' \t  '

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


def information_line(client=user.user(), w=0, d=1, message='', week_even_ignore=False):
    if client.position['week even'] and not week_even_ignore:
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


def notification():
    while True:
        time.sleep(60)
        date_day = date.today()
        for client in users:
            #               UTC 0                         пользовательский UTC
            localtime = datetime.now() + timedelta(minutes=client.settings['UTC'] * 60)
            if client.settings['notification'] \
                    and client.time == localtime.strftime('%H:%M') \
                    and client.working_day[date_day.weekday()]:
                bot.send_message(client.id,
                                 information_line_daily(client, int(tools.get_even()), datetime.today().isoweekday()) +
                                 '\n' + daily_schedule(client, int(tools.get_even()), datetime.today().isoweekday()))

            try:
                if client.position['last message type'] == 'today':  # обновление сообщения today
                    bot.edit_message_text(chat_id=client.id,
                                          message_id=client.position['last message id'],
                                          text=information_line(client, int(tools.get_even()),
                                                                datetime.today().isoweekday()) +
                                               '\n' + daily_schedule(client, int(tools.get_even()),
                                                                     datetime.today().isoweekday(), arrow=True))
            except Exception as e:
                print(f' *** {client.id} has a problem - {e}')


def data_update():
    while True:
        connection.Update(users)
        print('database has been updated')
        time.sleep(1800)


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
    number = tools.find(users, message.chat.id)

    if number is None:
        client = user.user(id=message.chat.id, name=message.from_user.first_name, surname=message.from_user.last_name)
        users.append(client)

    bot.send_message(message.chat.id,
                     languages.assembly['hi'][users[number].settings['language']] + ' ' + users[number].name
                     + '.\n' +
                     languages.assembly['greeting'][users[number].settings['language']],
                     reply_markup=keyboard)

    bot.send_message(message.chat.id,
                     languages.assembly['choose a language'][users[number].settings['language']],
                     reply_markup=language_selection)


@bot.message_handler(commands=['test'])
def test(message):
    global users
    number = tools.find(users, message.chat.id)

    if number == 0:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        users[number].surname = 'none'
        bot.send_message(message.chat.id, 'изменил', reply_markup=language_selection)


# Сохраняем присланый файл с расписанием
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        global users
        number = tools.find(users, message.chat.id)

        if not (number is None):
            chat_id = message.chat.id

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'temp/' + str(chat_id) + '.txt'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            users[number].schedule = tools.from_file_to_schedule_array(str(chat_id))
            bot.reply_to(message, languages.assembly['received'][users[number].settings['language']])

        else:
            bot.send_message(message.chat.id,
                             languages.assembly['not in the database']['ru'])

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=['language'])
def language(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        bot.send_message(message.chat.id,
                         languages.assembly['choose a language'][users[number].settings['language']],
                         reply_markup=language_selection)


@bot.message_handler(commands=['merger'])
def merger(message):
    # соединение недель

    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        connection_weeks = types.InlineKeyboardMarkup()
        connection_weeks_yes = types.InlineKeyboardButton(
            text=languages.assembly['yes'][users[number].settings['language']],
            callback_data='connection weeks yes')
        connection_weeks_no = types.InlineKeyboardButton(
            text=languages.assembly['no'][users[number].settings['language']],
            callback_data='connection weeks no')
        connection_weeks.add(connection_weeks_no, connection_weeks_yes, )
        bot.send_message(message.chat.id,
                         languages.assembly['joint week'][users[number].settings['language']],
                         reply_markup=connection_weeks)


@bot.message_handler(commands=['inverting'])
def inverting(message):
    # поменять недели местами

    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        connection_weeks = types.InlineKeyboardMarkup()
        connection_weeks_yes = types.InlineKeyboardButton(
            text=languages.assembly['yes'][users[number].settings['language']],
            callback_data='swap schedule yes')
        connection_weeks_no = types.InlineKeyboardButton(
            text=languages.assembly['no'][users[number].settings['language']],
            callback_data='swap schedule no')
        connection_weeks.add(connection_weeks_no, connection_weeks_yes, )

        bot.send_message(message.chat.id,
                         languages.assembly['swap schedule'][users[number].settings['language']],
                         reply_markup=connection_weeks)


@bot.message_handler(commands=['notification'])
def notification_ui(message):
    # включить увидомления
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        connection_weeks = types.InlineKeyboardMarkup()
        connection_weeks_yes = types.InlineKeyboardButton(
            text=languages.assembly['yes'][users[number].settings['language']],
            callback_data='notification on yes')
        connection_weeks_no = types.InlineKeyboardButton(
            text=languages.assembly['no'][users[number].settings['language']],
            callback_data='notification on no')
        connection_weeks.add(connection_weeks_no, connection_weeks_yes, )

        bot.send_message(message.chat.id,
                         languages.assembly['notification'][users[number].settings['language']],
                         reply_markup=connection_weeks)


@bot.message_handler(commands=['settings'])
def settings(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        languages.client = users[number]
        bot.send_message(message.chat.id, languages.settings(users[number]))


@bot.message_handler(commands=['UTC'])
def utc(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        bot.send_message(message.chat.id,
                         languages.assembly['choose a utc'][users[number].settings['language']])
        users[number].position['last message type'] = 'utc'


@bot.message_handler(commands=['yesterday'])
def yesterday(message):
    global users
    number = tools.find(users, message.chat.id)

    week_parity = int(tools.get_even())
    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        if date.today().isoweekday() == 1:
            week_parity = int(not tools.get_even())

        bot.send_message(message.chat.id,
                         information_line(users[number],
                                          w=week_parity,
                                          d=(date.today() - timedelta(days=1)).isoweekday())
                         + '\n' +
                         daily_schedule(users[number],
                                        week_parity,
                                        (date.today() - timedelta(days=1)).isoweekday()))


@bot.message_handler(commands=['today'])
def today(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        mes = bot.send_message(message.chat.id,
                               information_line(users[number],
                                                int(tools.get_even()),
                                                datetime.today().isoweekday()) + '\n' +
                               daily_schedule(users[number],
                                              int(tools.get_even()),
                                              datetime.today().isoweekday(),
                                              arrow=True))

        users[number].position['last message id'] = mes.message_id
        users[number].position['last message type'] = 'today'


@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        if date.today().isoweekday() == 7:
            week_parity = int(not tools.get_even())

        bot.send_message(message.chat.id,
                         information_line(client=users[number],
                                          w=week_parity,
                                          d=(date.today() + timedelta(days=1)).isoweekday())
                         + '\n' +
                         daily_schedule(client=users[number],
                                        w=week_parity,
                                        d=(date.today() + timedelta(days=1)).isoweekday()))


@bot.message_handler(commands=['week'])
def week_ui(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        navigation = types.InlineKeyboardMarkup()
        week_back = types.InlineKeyboardButton(text='<', callback_data='week back')
        week_forward = types.InlineKeyboardButton(text='>', callback_data='week forward')
        navigation.add(week_back, week_forward)

        if not users[number].settings['combination of weeks']:
            week_another = types.InlineKeyboardButton(
                text=languages.assembly['another'][users[number].settings['language']],
                callback_data='week another')
            navigation.add(week_another)

        bot.send_message(message.chat.id,
                         information_line(users[number],
                                          users[number].position['week'],
                                          users[number].position['day'])
                         + '\n' +
                         daily_schedule(users[number],
                                        users[number].position['week'],
                                        users[number].position['day']),
                         reply_markup=navigation)


def edit_day_week(user_id=0, message_id=0):
    global users
    number = tools.find(users, user_id)

    navigation = types.InlineKeyboardMarkup()
    if users[number].position['last message type'] == 'edit true':  # вносим изменения
        week_up = types.InlineKeyboardButton(text='↑', callback_data='edit up')
        week_down = types.InlineKeyboardButton(text='↓', callback_data='edit down')
        week_add_b = types.InlineKeyboardButton(
            text=languages.assembly['e add']['add b'][users[number].settings['language']],
            callback_data='edit add before')
        week_add_a = types.InlineKeyboardButton(
            text=languages.assembly['e add']['add a'][users[number].settings['language']],
            callback_data='edit add after')
        week_del = types.InlineKeyboardButton(text=languages.assembly['del'][users[number].settings['language']],
                                              callback_data='edit delete')
        edit_day = types.InlineKeyboardButton(
            text=languages.assembly['back to day selection'][users[number].settings['language']],
            callback_data='edit day')

        navigation.add(week_up, week_add_b)
        navigation.add(week_down, week_add_a)
        navigation.add(week_del)
        navigation.add(edit_day)
        if message_id == 0:
            bot.send_message(users[number].id,
                             text=information_line(users[number],
                                                   users[number].position['week'],
                                                   users[number].position['day'],
                                                   message=languages.assembly['editing'][
                                                       users[number].settings['language']],
                                                   week_even_ignore=True) + '\n' +
                                  daily_schedule(users[number],
                                                 users[number].position['week'],
                                                 users[number].position['day'],
                                                 choice=True, week_even_ignore=True),
                             reply_markup=navigation)
        else:
            bot.edit_message_text(chat_id=users[number].id,
                                  message_id=message_id,
                                  text=information_line(users[number],
                                                        users[number].position['week'],
                                                        users[number].position['day'],
                                                        message=languages.assembly['editing'][
                                                            users[number].settings['language']],
                                                        week_even_ignore=True)
                                       + '\n' +
                                       daily_schedule(users[number],
                                                      users[number].position['week'],
                                                      users[number].position['day'],
                                                      choice=True,
                                                      week_even_ignore=True),
                                  reply_markup=navigation)

    else:  # выбор дня для редактирования
        users[number].position['last message type'] = 'edit false'
        week_back = types.InlineKeyboardButton(text='<', callback_data='edit back')
        week_forward = types.InlineKeyboardButton(text='>', callback_data='edit forward')
        edit_day = types.InlineKeyboardButton(
            text=languages.assembly['edit this day'][users[number].settings['language']],
            callback_data='edit day')
        navigation.add(week_back, week_forward)
        message_id_s = 0
        message_text = ''
        if not users[number].settings['combination of weeks']:
            week_another = types.InlineKeyboardButton(
                text=languages.assembly['another'][users[number].settings['language']],
                callback_data='edit another')
            navigation.add(week_another)

        navigation.add(edit_day)

        if message_id == 0:
            mes = bot.send_message(users[number].id,
                                   information_line(users[number],
                                                    users[number].position['week'],
                                                    users[number].position['day'])
                                   + '\n' +
                                   daily_schedule(users[number],
                                                  users[number].position['week'],
                                                  users[number].position['day'],
                                                  week_even_ignore=True),
                                   reply_markup=navigation)
            message_id_s = mes.message_id
            message_text = mes.text
        else:
            answer = information_line(users[number],
                                      users[number].position['week'],
                                      users[number].position['day']) + '\n' \
                     + daily_schedule(users[number],
                                      users[number].position['week'],
                                      users[number].position['day'],
                                      choice=True,
                                      week_even_ignore=True)

            if users[number].position['last message id'] != answer:
                bot.edit_message_text(chat_id=users[number].id,
                                      message_id=message_id,
                                      text=answer,
                                      reply_markup=navigation)
            else:
                bot.answer_callback_query(callback_query_id=users[number].id,
                                          text='Nothing has changed here ＼(ﾟｰﾟ＼)')

        if message_id_s != 0:
            users[number].position['last message id'] = message_id_s
            users[number].position['last message'] = message_text


@bot.message_handler(commands=['edit'])
def week_ui(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        edit_day_week(user_id=message.chat.id)


@bot.message_handler(commands=['time'])
def time_ui(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        bot.send_message(message.chat.id, languages.assembly['enter time'][users[number].settings['language']])
        users[number].position['last message type'] = 'time'


@bot.message_handler(commands=['help'])
def help_ui(message):
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        bot.send_message(message.chat.id, languages.assembly['help'][users[number].settings['language']])


@bot.message_handler(commands=['template'])
def help_ui(message):
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        doc = open('temp/Шаблон расписания.txt', 'rb')
        bot.send_document(message.chat.id, doc)
        doc.close()


@bot.message_handler(commands=['doc'])
def steam_document(message):
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        tools.make_file_with_schedule(message.chat.id, users[number].schedule)
        doc = open(f'temp/{message.chat.id}.txt', 'rb')
        bot.send_document(message.chat.id, doc)
        doc.close()
        os.remove(f'temp/{message.chat.id}.txt')


@bot.message_handler(commands=['torn'])
def torn_ui(message):
    # включить увидомления
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])
    else:
        torn = types.InlineKeyboardMarkup()
        torn_yes = types.InlineKeyboardButton(text=languages.assembly['yes'][users[number].settings['language']],
                                              callback_data='torn on yes')
        torn_no = types.InlineKeyboardButton(text=languages.assembly['no'][users[number].settings['language']],
                                             callback_data='torn on no')
        torn.add(torn_no, torn_yes)

        bot.send_message(message.chat.id,
                         languages.assembly['torn'][users[number].settings['language']],
                         reply_markup=torn)


@bot.message_handler(content_types=['text'])
def text(message):
    global users
    number = tools.find(users, message.chat.id)

    if number is None:
        bot.send_message(message.chat.id,
                         languages.assembly['not in the database']['ru'])

    else:
        # установить utc
        if users[number].position['last message type'] == 'utc':
            try:
                users[number].settings['UTC'] = float(message.text)

                bot.send_message(message.chat.id,
                                 languages.assembly['done utc'][users[number].settings['language']]
                                 + ' ' +
                                 str(users[number].settings['UTC']) + '.')
                users[number].position['last message type'] = 'null'

            except Exception as e:
                bot.send_message(message.chat.id, str(e))

        # установить время
        if users[number].position['last message type'] == 'time':
            try:
                time_clock = datetime.strptime(str(message.text), '%H:%M').time()
                # если что-то пойдет не так то выкенет Exception

                users[number].time = time_clock.strftime('%H:%M')
                bot.send_message(message.chat.id,
                                 languages.assembly['done time'][users[number].settings['language']]
                                 + ' ' +
                                 str(users[number].time))

                users[number].position['last message type'] = 'null'

            except Exception as e:
                bot.send_message(message.chat.id, str(e))

        # меняем занятие
        if users[number].position['last message type'] == 'edit true':
            try:
                temp = users[number].schedule
                temp[users[number].position['week']][users[number].position['day'] - 1][
                    users[number].position['lesson'] - 1] = message.text
                users[number].schedule = temp
                del temp

                edit_day_week(user_id=message.chat.id, message_id=users[number].position['last message id'])
                bot.delete_message(message.chat.id, message.message_id)

            except Exception as e:
                bot.send_message(message.chat.id, str(e))


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # поиск пользователя:
    global users
    number = tools.find(users, call.message.chat.id)

    if number is None:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text='Take it easy!')

    else:
        # смена языка:
        if call.data == 'us' or call.data == 'ua' or call.data == 'ru':
            past = users[number].settings['language']
            if call.data == 'us':
                users[number].settings['language'] = 'us'

            elif call.data == 'ua':
                users[number].settings['language'] = 'ua'

            elif call.data == 'ru':
                users[number].settings['language'] = 'ru'

            if call.data != past:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=languages.assembly['choose a language'][users[number].settings['language']],
                                      reply_markup=language_selection)
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][users[number].settings['language']])
            return

        # слияние недель
        if call.data[:16] == 'connection weeks':
            past = users[number].settings['combination of weeks']

            if call.data == 'connection weeks yes':
                users[number].settings['combination of weeks'] = True

            elif call.data == 'connection weeks no':
                users[number].settings['combination of weeks'] = True

            if call.data != past:
                if call.data == 'connection weeks yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Weeks are the same: True')

                if call.data == 'connection weeks no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Weeks are the same: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][users[number].settings['language']])
            return

        # поменять местами расписание
        if call.data[:13] == 'swap schedule':
            past = users[number].position['week even']
            if call.data == 'swap schedule yes':
                users[number].position['week even'] = True

            elif call.data == 'swap schedule no':
                users[number].position['week even'] = True

            if call.data != past:
                if call.data == 'swap schedule yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Parity and non-parity have changed: True')
                if call.data == 'swap schedule no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Parity and non-parity have changed: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][users[number].settings['language']])
            return

        # включить уведомления
        if call.data[:15] == 'notification on':
            past = users[number].settings['notification']
            if call.data == 'notification on yes':
                users[number].settings['notification'] = True

            elif call.data == 'notification on no':
                users[number].settings['notification'] = False

            if call.data != past:
                if call.data == 'notification on yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Notifications are included: True')
                if call.data == 'notification on no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Notifications are included: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][users[number].settings['language']])
            return

        # расписание на неделю
        if call.data[:4] == 'week':
            if call.data == 'week another':
                if users[number].position['week'] == 0:
                    users[number].position['week'] = 1

                else:
                    users[number].position['week'] = 0

            if call.data == 'week back':
                if users[number].position['day'] == 1:
                    users[number].position['day'] = 7

                else:
                    users[number].position['day'] = users[number].position['day'] - 1

            if call.data == 'week forward':
                if users[number].position['day'] == 7:
                    users[number].position['day'] = 1

                else:
                    users[number].position['day'] = users[number].position['day'] + 1

            navigation = types.InlineKeyboardMarkup()  # пересобираем навигацию
            week_back = types.InlineKeyboardButton(text='<', callback_data='week back')
            week_forward = types.InlineKeyboardButton(text='>', callback_data='week forward')
            navigation.add(week_back, week_forward)

            if not users[number].settings['combination of weeks']:
                week_another = types.InlineKeyboardButton(
                    text=languages.assembly['another'][users[number].settings['language']],
                    callback_data='week another')
                navigation.add(week_another)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=information_line(users[number],
                                                        users[number].position['week'],
                                                        users[number].position['day'])
                                       + '\n' +
                                       daily_schedule(users[number],
                                                      users[number].position['week'],
                                                      users[number].position['day']),
                                  reply_markup=navigation)
            return

        # управление edit week
        if call.data[:4] == 'edit':

            if call.data == 'edit another':
                if users[number].position['week'] == 0:
                    users[number].position['week'] = 1

                else:
                    users[number].position['week'] = 0

                users[number].position['last message type'] = 'edit false'

            if call.data == 'edit back':
                if users[number].position['day'] == 1:
                    users[number].position['day'] = 7

                else:
                    users[number].position['day'] = users[number].position['day'] - 1

                users[number].position['last message type'] = 'edit false'

            if call.data == 'edit forward':
                if users[number].position['day'] == 7:
                    users[number].position['day'] = 1

                else:
                    users[number].position['day'] = users[number].position['day'] + 1

                users[number].position['last message type'] = 'edit false'

            if call.data == 'edit day':
                if users[number].position['last message type'] == 'edit true':
                    users[number].position['lesson'] = 0
                    users[number].position['last message type'] = 'edit false'

                else:
                    users[number].position['lesson'] = 1
                    users[number].position['last message type'] = 'edit true'

            if call.data == 'edit up':
                if users[number].position['lesson'] > 1:
                    users[number].position['lesson'] = users[number].position['lesson'] - 1
                    users[number].position['last message type'] = 'edit true'
                else:
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='negative value is impossible!')
                    return

            if call.data == 'edit down':
                if users[number].position['lesson'] < len(
                        users[number].schedule[users[number].position['week']][users[number].position['day'] - 1]):
                    users[number].position['lesson'] = users[number].position['lesson'] + 1
                    users[number].position['last message type'] = 'edit true'
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='There is nothing further :3')
                    return

            if call.data == 'edit add before':
                users[number].position['last message type'] = 'edit true'
                temp = users[number].schedule
                temp_b = users[number].schedule[users[number].position['week']][users[number].position['day'] - 1]
                temp_b.reverse()
                temp_a = temp_b[: (len(temp_b) - (users[number].position['lesson'] - 1))]
                temp_b.reverse()
                temp_a.reverse()
                temp_b = temp_b[:users[number].position['lesson'] - 1]
                temp_b.append(' ')

                temp[users[number].position['week']][users[number].position['day'] - 1] = temp_b + temp_a
                users[number].schedule = temp
                users[number].position['lesson'] = users[number].position['lesson'] + 1

            if call.data == 'edit add after':
                users[number].position['last message type'] = 'edit true'
                temp = users[number].schedule
                temp_b = users[number].schedule[users[number].position['week']][users[number].position['day'] - 1]
                temp_b.reverse()
                temp_a = temp_b[: (len(temp_b) - (users[number].position['lesson']))]
                temp_b.reverse()
                temp_a.reverse()
                temp_b = temp_b[:users[number].position['lesson']]
                temp_b.append(' ')

                temp[users[number].position['week']][users[number].position['day'] - 1] = temp_b + temp_a
                users[number].schedule = temp

            if call.data == 'edit delete':
                try:
                    users[number].position['last message type'] = 'edit true'
                    temp = users[number].schedule
                    del temp[users[number].position['week']][users[number].position['day'] - 1][users[number].position['lesson'] - 1]
                    lesson = users[number].position['lesson']
                    if len(users[number].schedule[users[number].position['week']][users[number].position['day'] - 1]) <\
                            users[number].position['lesson']:
                        lesson += -1
                    users[number].schedule = temp
                    users[number].position['lesson'] = (lesson if lesson >= 1 else 1)
                except Exception as e:
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text=f'Unexpected error during deletion code: {e}')
                    return

            users[number].position['last message id'] = call.message.message_id

            edit_day_week(user_id=call.message.chat.id, message_id=call.message.message_id)  # сборка расписания
            return

        # Время вместо цифр в расписании
        if call.data == 'torn on no' or call.data == 'torn on yes':
            past = users[number].settings['Time instead of number']
            if call.data == 'torn on yes':
                users[number].settings['Time instead of number'] = True

            elif call.data == 'torn on no':
                users[number].settings['Time instead of number'] = False

            if call.data != past:
                if call.data == 'torn on yes':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Time instead of number: True')
                if call.data == 'torn on no':
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Time instead of number: False')

            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=languages.assembly['been selected'][users[number].settings['language']])
            return


th_notigic = threading.Thread(target=notification)
th_db = threading.Thread(target=data_update)

th_notigic.daemon = True
th_notigic.start()

th_db.daemon = True
th_db.start()

bot.polling(none_stop=True)
