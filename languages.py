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
        'us': 'If you want the schedule to be the same at all weeks (even and non-even), then click on "🟢", '
              'if you want to disable this function, click on "⭕".\nWe will take your schedule for the odd week as '
              'the main thing.',
        'ua': 'Якщо ви хочете щоб розклад було однаковим на всіх тижнях (парних і не) то натисніть на "🟢", '
              'якщо хочете відключити цю функцію натисніть на "⭕".\nМи візьмемо ваш розклад для непарної тижні як '
              'головне.',
        'ru': 'Если вы хотите чтобы расписание было одинаковым на всех неделях (четным и не) то нажмите на "🟢", '
              'если хотите отключить эту функцию нажмите на "⭕".\nМы возьмем ваше расписание для нечетной недели как '
              'главное. '
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

    'week even': {
        'us': {
            0: 'week: Even',
            1: 'week: Not even'
        },

        'ua': {
            0: 'тиждень: Парна',
            1: 'тиждень: Непарна',
        },

        'ru': {
            0: 'неделя: Четная',
            1: 'неделя: Нечетная'
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

    }

}


def settings(client):
    user_settings = {
        'us': 'Settings: \n'
            '/merger - The merger of weeks = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - language selection = ' + str(client.settings['language']) + '\n'
            '/UTC - Set your time at UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Swap the weekly schedule = ' + str(client.position['week even']) + '\n'
            '/notification - Turn on the visions = ' + str(client.position['week even']) + '\n'
            '/time - Set the time for seeing = ' + str(client.time) + '\n',
        'ua': 'Налаштування: \n'
            '/merger - Злиття тижнів = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - Вибір мови = ' + str(client.settings['language']) + '\n'
            '/UTC - Встановити ваш час по UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Поміняти місцями розклад тижнів = ' + str(client.position['week even']) + '\n'
            '/notification - Включення увідомленій = ' + str(client.position['week even']) + '\n'
            '/time - Встановити час увідомленія = ' + str(client.time) + '\n',
        'ru': 'Settings: \n'
            '/merger - Слияние недель = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - Выбор языка = ' + str(client.settings['language']) + '\n'
            '/UTC - Установить ваше время по UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Поменять местами расписание недель = ' + str(client.position['week even']) + '\n'
            '/notification - Turn on the visions = ' + str(client.position['week even']) + '\n'
            '/time - Установить время увидомления = ' + str(client.time) + '\n'
    }
    return user_settings[client.settings['language']]

