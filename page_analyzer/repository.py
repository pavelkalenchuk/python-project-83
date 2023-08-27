import psycopg2
import datetime as dt

from settings import DATABASE_URL


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


def convert_urls(tuple_: tuple):
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
    result = list(map(convert_urls, selection))
    return result


def add_url_check(url_id, parsed_url):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)", # noqa E501
        (
            url_id,
            parsed_url["status_code"],
            parsed_url["h1"],
            parsed_url["title"],
            parsed_url["description"],
            dt.datetime.now().replace(microsecond=0).isoformat(),
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()


def convert_url_checks(tuple_: tuple):
    KEYS = (
        "id",
        "url_id",
        "status_code",
        "h1",
        "title",
        "description",
        "created_at"
    )
    return dict(zip(KEYS, tuple_))


def get_url_checks_by_date(id_url: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT id, url_id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id={id_url} ORDER BY created_at DESC" # noqa E501
    )
    selection = cursor.fetchall()
    cursor.close()
    conn.close()
    selection = list(
        map(
            lambda t: (t[0], t[1], t[2], t[3], t[4], t[5], t[6].strftime("%Y-%m-%d")), # noqa E501
            selection,
        )
    )
    result = list(map(convert_url_checks, selection))
    return result
