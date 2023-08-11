import psycopg2

from datetime import datetime


def add_url_db(url: str, db_url):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (name, created_at) VALUES (%s, %s)",
        (url, datetime.now().isoformat())
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_url_info_db(url: str, db_url):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, url, created_at FROM urls"
    )
    cursor.fetchone()
    cursor.close()
    conn.close()