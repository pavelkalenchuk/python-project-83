from psycopg2 import DatabaseError
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import cursor as DefaultCursor
from contextlib import contextmanager
from settings import DATABASE_URL


class PsqlDatabase:
    def __init__(self):
        self.app = None
        self.pool = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        self.pool = SimpleConnectionPool(1, 20, dsn=DATABASE_URL)
        return self.pool

    @contextmanager
    def get_cursor(self, cursor_mode=DefaultCursor):
        if self.pool is None:
            self.connect()
        con = self.pool.getconn()
        try:
            yield con.cursor(cursor_factory=cursor_mode)
            con.commit()
        except (Exception, DatabaseError) as error: # noqa F841
            con.rollback()
        finally:
            self.pool.putconn(con)
