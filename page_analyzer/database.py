import psycopg2

from datetime import datetime


class UrlsDataBase():
    def connect(self, db_url):
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        return cursor
    
    def add_url_to_db(self, url, db_url):
        cursor = UrlsDataBase.connect(db_url)
        cursor.exucute(
            "INSRT INTO urls (name, created_at) VALUES (%s, %s)",
            (url, datetime.now().isoformat())
        )



    def add_url(self, url)