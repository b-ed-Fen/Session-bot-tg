import os
import psycopg2
import tools
import user

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
        Position TEXT NOT NULL);''')
    print("Таблица создана")
except Exception as identifier:
    print(str(identifier))


def Update(user_array):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    for i in user_array:
        try:
            setinfo = "INSERT INTO UDB (ID,Name,Surname,Schedule,Time,Settings,Position) VALUES (" + \
                      str(i.id) + ", '" + str(i.name) + "', '" + str(i.surname) + "', '" + \
                      tools.get_schedule_text(i.schedule) + "', '" + i.time + "', '" + tools.get_settings(i.settings) + \
                      "','" + tools.get_position(i.position) + "')"

            cursor.execute(setinfo)
        except Exception as e:
            print(e)
            try:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cursor = conn.cursor()
                cursor.execute("UPDATE UDB set Name = '" + str(i.name) + "' where ID = " + str(i.id))
                cursor.execute("UPDATE UDB set Surname = '" + str(i.surname) + "' where ID = " + str(i.id))
                cursor.execute(
                    "UPDATE UDB set Schedule = '" + tools.get_schedule_text(i.schedule) + "' where ID = " + str(i.id))
                cursor.execute("UPDATE UDB set Time = '" + i.time + "' where ID = " + str(i.id))
                cursor.execute("UPDATE UDB set Settings = '" + tools.get_settings(i.settings) + "' where ID = " + str(i.id))
                cursor.execute("UPDATE UDB set Position = '" + tools.get_position(i.position) + "' where ID = " + str(i.id))

            except Exception as e:
                print(e)

    conn.commit()
    cursor.close()
    conn.close()


def get_array_user():
    array = []

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT ID,Name,Surname,Schedule,Time,Settings,Position from UDB")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        name = row[1]
        surname = row[2]
        schedule = tools.set_schedule_arr(row[3])
        time = row[4]
        settings = tools.set_settings(row[5])
        position = tools.set_position(row[6])

        client = user.user(id, name, surname, schedule, time, settings, position)

        array.append(client)

    conn.close()

    return array


conn.commit()
cursor.close()
conn.close()
