import psycopg2

import datetime as dt
from settings import DATABASE_URL
from icecream import ic # noqa F401


def add_url_db(url: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (name, created_at) VALUES (%s, %s)",
        (url, dt.datetime.now().replace(microsecond=0).isoformat()),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_url_info_db(**columns):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    if "name" in columns:
        column = "name"
        value = columns["name"]
    if "id" in columns:
        column = "id"
        value = columns["id"]
    cursor.execute(
        f"SELECT id, name, created_at FROM urls WHERE {column} = (%s)",
        (value,)
    )
    selection = cursor.fetchone()
    if not selection:
        return False
    cursor.close()
    conn.close()
    result = {
        "id": selection[0],
        "name": selection[1],
        "created_at": selection[2].strftime("%Y-%m-%d"),
    }
    return result


def convert_url(tuple_: tuple):
    KEYS = ("id", "name", "created_at")
    return dict(zip(KEYS, tuple_))


def get_urls_by_date():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    SQL = "SELECT * FROM urls ORDER BY created_at DESC"
    cursor.execute(SQL)
    selection = cursor.fetchall()
    cursor.close()
    conn.close()
    result = list(map(convert_url, selection))
    return result


def add_url_checks(url_id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)",
        (url_id, dt.datetime.now().replace(microsecond=0).isoformat()),
    )
    conn.commit()
    cursor.close()
    conn.close()


def convert_url_checks(tuple_: tuple):
    KEYS = ("id", "created_at")
    return dict(zip(KEYS, tuple_))


def get_url_checks_by_date(id_url):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT id, created_at FROM url_checks WHERE url_id={id_url} ORDER BY created_at DESC"
    )
    selection = cursor.fetchall()
    cursor.close()
    conn.close()
    selection = list(
        map(
            lambda t: (t[0], t[1].strftime("%Y-%m-%d")),
            selection
        )
    )
    result = list(
        map(
            convert_url_checks, selection
        )
    )
    return result
