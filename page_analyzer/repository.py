import psycopg2

import datetime as dt
from settings import DATABASE_URL
from icecream import ic



def add_url_db(url: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (name, created_at) VALUES (%s, %s)",
        (url, dt.datetime.now().replace(microsecond=0).isoformat())
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_url_info_db(**columns):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    if 'name' in columns:
        column = 'name'
        value = columns["name"]
    if 'id' in columns:
        column = 'id'
        value = columns['id']
    cursor.execute(f"SELECT id, name, created_at FROM urls WHERE {column} = (%s)", (value,))
    selection = cursor.fetchone()
    if not selection:
        return False
    cursor.close()
    conn.close()
    result = {
        "id": selection[0],
        "name": selection[1],
        "created_at": selection[2]
    }
    return result


def convert(tuple_):
    KEYS = ("id", "name", "created_at")
    result = dict(zip(KEYS, tuple_))
    return result


def get_urls_by_date():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    SQL = "SELECT * FROM urls ORDER BY created_at DESC"
    cursor.execute(SQL)
    selection = cursor.fetchall()
    cursor.close()
    conn.close()
    result = list(map(convert, selection))
    return result

a =  (16, 'https://www.ya.ru', "10-10-10")
b = convert(a)
ic(b)

urls =  [(19, 'https://ya.ru', "10-10-10"),
           (18, 'https://proglib.io', "10-10-10"),
           (17, 'https://ru.hexlet.io', "10-10-10"),
           (16, 'https://www.ya.ru', "10-10-10"),
           (15,
            'https://www.pythonicway.com',
            "10-10-10")]

c = list(
    map(
        convert, urls
    )
)
ic(c)


time_ = dt.datetime(2023, 8, 22, 23, 24, 5)
ic(type(time_))