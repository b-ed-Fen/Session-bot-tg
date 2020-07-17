import user
client = user.user(0, 'non', 'non')
assembly = {
    'hi': {
        'us': 'Hi',
        'ua': 'Привіт',
        'ru': 'Привет'
    },

    'greeting': {
        'us': 'Glad to welcome you! I can come in handy in your dungeon at school or university :3\nWrite /help for '
              'more information',
        'ua': 'Радий тебе вітати! Я можу тобі знадобиться в твоєму проходженні Данжі в школі або універі: 3\nДля '
              'додаткової інформації напиши / help',
        'ru': 'Рад тебя приветствовать! Я могу тебе пригодится в твоем прохождении данжа в школе или универе :3\nДля '
              'дополнительной информации напиши /help '

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
        'ua': 'Поміняти місцями парну і не парну недiлю?',
        'ru': 'Поменять местами четную и нечетную неделю?'
    },

    'choose a language': {
        'us': 'Choose a language',
        'ua': 'Оберіть мову',
        'ru': 'Выберите язык'
    },

    'choose a utc': {
        'us': 'Enter the UTC of your region, for example 2.',
        'ua': 'Введіть UTC вашого регіону, наприклад 2.',
        'ru': 'Введите UTC вашего региона, например 2.'
    },

    'notification': {
        'us': 'Enable daily notifications?',
        'ua': 'Включити щоденні повідомлення?',
        'ru': 'Включить ежедневные уведомлений?'
    },

    'torn': {
        'us': 'Want to see time in your schedule instead of class number?',
        'ua': 'Хочете бачити в своєму розкладі час замість номера занять?',
        'ru': 'Хотите видеть в своем расписании время вместо номера занятия?'
    },

    'week even': {
        'us': {
            0: 'Week: Even',
            1: 'Week: Not even'
        },

        'ua': {
            0: 'Тиждень: Парна',
            1: 'Тиждень: Непарна',
        },

        'ru': {
            0: 'Неделя: Четная',
            1: 'Неделя: Нечетная'
        }
    },

    'received': {
        'us': 'Received!',
        'ua': 'Прийнято!',
        'ru': 'Принято!',

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
    },

    'help': {
        'us': 'How to create your own schedule? \nCreate and open a .txt file, enter the schedule line by line '
              'dividing the lessons with one press of Enter. With two presses of Enter, separate the days of the '
              'week, with three presses complete the schedule of the week. In cases of using an even and odd week, '
              'repeat the same actions for the next week. Paying attention that in the filling we use the format of '
              'week 7, if there is no “empty” class on one day, the day is filled with a space. To get the template '
              'file, enter /template.\n'
              'How to configure a bot for yourself?\т\nEverything is simple here, you just need to write / settings '
              'and select all the functions that you need. Do not be afraid to click on these commands, I will not '
              'delete your schedule until you give me a new one. If it’s not clear from the settings what this or '
              'that function does, try entering its command, I will try to explain what will change.',

        'ua': 'Як створити свій розклад? \nСоздаем і відкриваємо .txt файл, вводите розклад через підрядник '
              'розділяючи заняття одним натисканням Enter. Двома натисканнями Enter поділяєте дні тижня, '
              'трьома натисканнями завершите розклад тижні. У випадки використання парній і непарній тижні повторюєте '
              'такі ж дії на стежить тиждень. Звертаючи увагу що в заповненні використовуємо формат тижні 7, '
              'якщо занять в якийсь день немає «порожній» день заповнюється прогалиною. Для отримання файлу шаблону '
              'введіть /template.\n'
              'Як налаштувати бота під себе\nТут все просто, необхідно лише написати / settings і вибрати всі '
              'функції, які вам потрібні. Не бійтеся натискати на ці команди, я не видалю ваше розклад до тих пір, '
              'поки ви мені не дасте нове. Якщо з налаштувань не ясно що робить та чи інша функція, спробуйте ввести '
              'її команду я постараюся пояснити, що зміниться.',

        'ru': 'Как создать своё расписание?\nСоздаем и открываем .txt файл, вводите расписание построчно разделяя '
              'занятия одним нажатием Enter. Двумя нажатиями Enter разделяете дни недели, тремя нажатиями завершите '
              'расписание недели. В случаи использования четной и нечетной недели повторяете такие же действия на '
              'следящую неделю. Обращая внимание что в заполнении используем формат недели 7, если занятий в какой-то '
              'день нет «пустой» день заполняется пробелом. Для получения файла шаблона введите /template.\n'
              'Как настроить бота под себя?\nТут все просто, необходимо лишь написать /settings и выбрать все '
              'функции, которые вам нужны. Не бойтесь нажимать на эти команды, я не удалю ваше расписание до тех пор, '
              'пока вы мне не дадите новое. Если из настроек не ясно что делает та или иная функция, попробуйте '
              'ввести ее команду я постараюсь объяснить, что изменится. '
    },

    'enter time': {
        'us': 'Enter the time in format "08:30"',
        'ua': 'Введіть час у форматі "08:30"',
        'ru': 'Введите время в формате "08:30"'
    },

    'done time': {
        'us': 'Done! Now I will remind the schedule every day in',
        'ua': 'Готово! Тепер я буду напомінати розпис кожного дня у',
        'ru': 'Готово! Теперь я буду напоминать расписание каждый день в'
    },

    'done utc': {
        'us': 'Done! Now your UTC region is equal to',
        'ua': 'Готово! Тепер ваш регіон ЮТЦ дорівнює',
        'ru': 'Готово! Теперь ваш регион UTC равен'
    },

    'wish of the day': {
        'us': {
            1: 'Have a good monday',
            2: 'Have a good tuesday',
            3: 'Good Wednesday',
            4: 'Good thursday',
            5: 'Have a good friday',
            6: 'Have a good saturday',
            7: 'Have a good Sunday'
        },

        'ua': {
            1: 'Гарного понеділка',
            2: 'Гарного вівторка',
            3: 'Доброю середовища',
            4: 'Доброго четверга',
            5: "Доброю п'ятниці",
            6: 'Вдалою суботи',
            7: 'Гарної неділі'
        },

        'ru': {
            1: 'Хорошего понедельника',
            2: 'Хорошего вторника',
            3: 'Хорошей среды',
            4: 'Доброго четверга',
            5: 'Хорошей пятницы',
            6: 'Удачной субботы',
            7: 'Хорошего воскресенья'

        }

    },

    'no schedule': {
        'us': 'No schedule',
        'ua': 'Розкладу немає',
        'ru': 'Расписания нет'
    },

    'editing': {
        'us': 'EDIT.',
        'ua': 'РЕД.',
        'ru': 'РЕД.'
    },

    'e add': {
        'add b': {
            'us': 'add before',
            'ua': 'додати до',
            'ru': 'добавить до'
        },
        'add a': {
            'us': 'add after',
            'ua': 'додати після',
            'ru': 'добавить после'
        },
    },

    'del': {
        'us': 'delete',
        'ua': 'видалити',
        'ru': 'удалить'
    },

    'edit this day': {
        'us': 'edit this day',
        'ua': 'редагувати цей день',
        'ru': 'редактировать этот день'
    },

    'back to day selection': {
        'us': 'back to day selection',
        'ua': 'до вибору дня',
        'ru': 'к выбору дня'
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
            '/time - Set the time for seeing = ' + str(client.time) + '\n'
            '/torn - Time instead of numbers in the schedule = ' + str(client.settings['Time instead of number']) + '\n',
        'ua': 'Налаштування: \n'
            '/merger - Злиття тижнів = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - Вибір мови = ' + str(client.settings['language']) + '\n'
            '/UTC - Встановити ваш час по UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Поміняти місцями розклад тижнів = ' + str(client.position['week even']) + '\n'
            '/notification - Включення увідомленій = ' + str(client.settings['notification']) + '\n'
            '/time - Встановити час повідомлення = ' + str(client.time) + '\n'
            '/torn - Час замість цифр в розкладі = ' + str(client.settings['Time instead of number']) + '\n',
        'ru': 'Настройки: \n'
            '/merger - Слияние недель = ' + str(client.settings['combination of weeks']) + '\n'
            '/language - Выбор языка = ' + str(client.settings['language']) + '\n'
            '/UTC - Установить ваше время по UTC = ' + str(client.settings['UTC']) + '\n'
            '/inverting - Поменять местами расписание недель = ' + str(client.position['week even']) + '\n'
            '/notification - Включение уведомления = ' + str(client.settings['notification']) + '\n'
            '/time - Установить время уведомлений = ' + str(client.time) + '\n'
            '/torn - Время вместо цифр в расписании = ' + str(client.settings['Time instead of number']) + '\n'
    }
    return user_settings[client.settings['language']]

