import os
import psycopg2
import tools
import user
import progressbar

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

try:
    cursor.execute('''CREATE TABLE UDB  
        (ID INT PRIMARY KEY NOT NULL,
        Name TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Schedule TEXT NOT NULL,
        Time TEXT NOT NULL,
        Settings TEXT NOT NULL,
        Position TEXT NOT NULL,
        Couples_schedule TEXT NOT NULL,
        Working_day TEXT NOT NULL);''')
    print("Таблица создана")
except Exception as identifier:
    print(str(identifier))


def Update(user_array):
    bar = progressbar.ProgressBar(maxval=len(user_array), widgets=[     # для наглядности отправки пльзователей в бд
        'Base Update :      ',  # Статический текст
        progressbar.Bar(left='[', marker='=', right=']'),  # Прогресс
        progressbar.SimpleProgress(),  # Надпись "1 из 2"
    ]).start()
    t = 0

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    de = 'DELETE FROM UDB;'     # Временное решение, удаление всех данных из базы данных с последущим созданием их.
    cur.execute(de)
    for i in user_array:
        t += 1
        try:

            setinfo = f"INSERT INTO UDB " \
                      f"(ID,Name,Surname,Schedule,Time,Settings,Position,Couples_schedule,Working_day) " \
                      f"VALUES ({str(i.id)}, '{str(i.name)}', '{str(i.surname)}', " \
                      f"'{tools.get_schedule_text(i.schedule)}', " \
                      f"'{i.time}', '{tools.from_array_to_text(i.settings.values())}', " \
                      f"'{tools.from_array_to_text(i.position.values())}', " \
                      f"'{tools.from_array_to_text(i.couples_schedule.values())}', " \
                      f"'{tools.from_array_to_text(i.working_day)}')"

            cur.execute(setinfo)
        except Exception as e:
            print('\n' + str(e))

    conn.commit()
    cursor.close()
    conn.close()

    bar.finish()


def get_array_user():
    array = []
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT ID,Name,Surname,Schedule,Time,Settings,Position,Couples_schedule,Working_day from UDB")
    rows = cursor.fetchall()

    bar = progressbar.ProgressBar(maxval=len(rows), widgets=[
        'Getting user base: ',  # Статический текст
        progressbar.Bar(left='[', marker='=', right=']'),  # Прогресс
        progressbar.SimpleProgress(),  # Надпись "1 из 2"
    ]).start()
    t = 0
    for row in rows:
        t += 1
        id = row[0]
        name = row[1]
        surname = row[2]
        schedule = tools.from_text_to_array_schedule(row[3])
        time = row[4]
        settings = tools.set_settings(row[5])
        position = tools.from_text_to_array_position(row[6])
        couples_schedule = tools.from_text_to_array_couples_schedule(row[7])
        working_day = tools.from_text_to_array(row[8])

        client = user.user(id, name, surname, schedule, time, settings, position, couples_schedule, working_day)

        array.append(client)
        bar.update(t)

    conn.close()
    bar.finish()
    return array


conn.commit()
cursor.close()
conn.close()
