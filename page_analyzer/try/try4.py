from page_analyzer.repository import add_url_to_db
from settings import DATABASE_URL
from icecream import ic
import psycopg2





data_url = DATABASE_URL
url = 'http://wwww.ya.ru'
ic(type(data_url))
ic(data_url)

try:
    conn = psycopg2.connect(data_url)
except:
    ic('no connect')

add_url_to_db(url, data_url)

