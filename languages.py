import user
client = user.user(0, 'non', 'non')
assembly = {
    'hi': {
        'us': 'Hi',
        'ua': 'Привіт',
        'ru': 'Привет'
    },

    'greeting': {
        'us': 'Glad to welcome you! I can come in handy in your dungeon at school or university :3',
        'ua': 'Радий тебе вітати! Я можу тобі знадобиться в твоєму проходженні Данжі в школі або універі: 3',
        'ru': 'Рад тебя приветствовать! Я могу тебе пригодится в твоем прохождении данжа в школе или универе :3'

    },

    'been selected': {
        'us': 'already been selected',
        'ua': 'вже було вибрано',
        'ru': 'уже было выбрано'
    },

    'not in the database': {
        'us': 'You are not in the database, write /start to register.',
        'ua': 'Вас немає в базі, напишіть /start щоб зареєструватись.',
        'ru': 'Вас нет в базе, напишите /start чтобы зарегистрироватся.'
    },

    'joint week': {
        'us': 'We will take the schedule for the odd week as the main thing. Do you want the schedule to be the same '
              'for all types of weeks?',
        'ua': 'Ми візьмемо розклад для непарної тижні як головне. Ви хочете щоб розклад було однаковим на всіх типах '
              'тижнів?',
        'ru': 'Мы возьмем расписание для нечетной недели как главное. Вы хотите чтобы расписание было одинаковым на '
              'всех типах недель? '
    },

    'swap schedule': {
        'us': 'Swap even and non-even schedules?',
        'ua': 'Поміняти місцями парну і не парне розклад?',
        'ru': 'Поменять местами четную и не четное расписание?'
    },

    'choose a language': {
        'us': 'Choose a language',
        'ua': 'Оберіть мову',
        'ru': 'Выберете язык'
    },

    'choose a utc': {
        'us': 'Enter the UTC of your region, for example 2.',
        'ua': 'Введіть UTC вашого регіону, наприклад 2.',
        'ru': 'Введите UTC вашего региона, например 2.'
    },

    'notification': {
        'us': 'Enable daily notifications?',
        'ua': 'Включити щоденні повідомлення?',
        'ru': 'Включить ежедневные уведомления?'
    },

    'week even': {
        'us': {
            0: 'week: Even',
            1: 'week: Not even'
        },

        'ua': {
            0: 'тиждень: Парна',
            1: 'тиждень: Не парна',
        },

        'ru': {
            0: 'неделя: Четная',
            1: 'неделя: Не четная'
        }
    },

    'received': {
        'us': 'received!',
        'ua': 'прийнято!',
        'ru': 'принято!',

    },

    'week day': {
        'us': {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        },

        'ua': {
            1: 'Понеділок',
            2: 'Вівторок',
            3: 'Середа',
            4: 'Четвер',
            5: "П'ятниця",
            6: 'Субота',
            7: 'Неділя'
        },

        'ru': {
            1: 'Понедельник',
            2: 'Вторик',
            3: 'Среда',
            4: 'Четверг',
            5: 'Пятница',
            6: 'Суббота',
            7: 'Воскресенье'

        }

    },
    'yes': {
        'us': 'Yes',
        'ua': 'Так',
        'ru': 'Да'
    },

    'no': {
        'us': 'No',
        'ua': 'Нi',
        'ru': 'Нет'
    },

    'another': {
        'us': 'another week',
        'ua': 'інший тиждень',
        'ru': 'другая неделя'
    }

}


def settings(client):
    user_settings = {
        'us': 'Settings: \n'
            '/merger - The merger of weeks = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - language selection = ' + str(client.settings['language']) + '\n'
            '/UTC - Set your time at UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Swap the weekly schedule = ' + str(client.position['week even']) + '\n'
            '/notification - Turn on notifications = ' + str(client.settings['notification']) + '\n'
            '/time - Set the time for seeing = ' + str(client.time) + '\n',
        'ua': 'Налаштування: \n'
            '/merger - Злиття тижнів = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - Вибір мови = ' + str(client.settings['language']) + '\n'
            '/UTC - Встановити ваш час по UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Поміняти місцями розклад тижнів = ' + str(client.position['week even']) + '\n'
            '/notification - Включення увідомленій = ' + str(client.settings['notification']) + '\n'
            '/time - Встановити час увідомленія = ' + str(client.time) + '\n',
        'ru': 'Настройки: \n'
            '/merger - Слияние недель = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - Выбор языка = ' + str(client.settings['language']) + '\n'
            '/UTC - Установить ваше время по UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Поменять местами расписание недель = ' + str(client.position['week even']) + '\n'
            '/notification - Включение уведомлений = ' + str(client.settings['notification']) + '\n'
            '/time - Установить время увидомления = ' + str(client.time) + '\n'
    }
    return user_settings[client.settings['language']]

