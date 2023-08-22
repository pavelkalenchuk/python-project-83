import psycopg2

from datetime import datetime


def add_url_db(url: str, db_url):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (name, created_at) VALUES (%s, %s)",
        (url, datetime.now().replace(microsecond=0).isoformat())
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_url_info_db(db_url, **columns):
    conn = psycopg2.connect(db_url)
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