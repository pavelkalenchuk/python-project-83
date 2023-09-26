import datetime as dt

from psycopg2.extras import DictCursor
from page_analyzer.database import PsqlDatabase


psql_db = PsqlDatabase()


def add_url(url: str):
    with psql_db.get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO urls (name, created_at) VALUES (%s, %s)",
            (url, dt.datetime.now().replace(microsecond=0).isoformat()),
        )
        cursor.execute(
            "SELECT id FROM urls where name=(%s)",
            (url,)
        )
        url_id = cursor.fetchone()[0]
    return url_id


def get_urls(**columns):
    with psql_db.get_cursor() as cursor:
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
    result = {
        "id": selection[0],
        "name": selection[1],
        "created_at": selection[2].strftime("%Y-%m-%d"),
    }
    return result


def get_urls_by_date():
    with psql_db.get_cursor(cursor_mode=DictCursor) as cursor:
        SQL = "SELECT * FROM urls ORDER BY created_at DESC"
        cursor.execute(SQL)
        selection = cursor.fetchall()
    return selection


def add_url_check(url_id, parsed_url):
    with psql_db.get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                url_id, # noqa E126
                parsed_url["status_code"],
                parsed_url["h1"],
                parsed_url["title"],
                parsed_url["description"],
                dt.datetime.now().replace(microsecond=0).isoformat(),
            ),
        )


def get_url_checks_by_date(id_url):
    with psql_db.get_cursor(cursor_mode=DictCursor) as cursor:
        cursor.execute(
            f"""SELECT
            id, url_id, status_code, h1, title, description,
            created_at FROM url_checks
            WHERE url_id={id_url} ORDER BY created_at DESC"""
        )
        selection = cursor.fetchall()
    return selection
