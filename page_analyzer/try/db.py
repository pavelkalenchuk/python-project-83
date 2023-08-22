from page_analyzer.repository import get_url_info_db, add_url_db
from settings import DATABASE_URL
from icecream import ic
import psycopg2


""" data_url = DATABASE_URL
url = 'http://wwww.yandex.ru'
ic(type(data_url))
ic(data_url)

try:
    conn = psycopg2.connect(data_url)
except:
    ic('no connect')

add_url_db(url, data_url) """

""" url1 = "website"
selection = get_url_info_db(url1, DATABASE_URL)
ic(selection)

if not get_url_info_db(url1, DATABASE_URL):
    ic ('no URL in DB')
else:
    ic('YES') """

# ic(type(selection['created_at']))

""" url2 = "website"
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
SQL = "SELECT id, name, created_at FROM urls WHERE name = %s"
cursor.execute(SQL, (url2,))
selection = cursor.fetchone()
ic(selection)
cursor.close()
conn.close()

ic(type(selection))

if not selection:
    ic('no website')
else:
    ic("website here")

var1 = has_db_url(url1, DATABASE_URL)
var2 = has_db_url(url2, DATABASE_URL)

ic(var1, var2) """


def f(p1, p2='', p3=''):
    if p2:
        return p1, p2
    if p3:
        return p1, p3
    
a = f('hello', p2="world")
b = f('hello', p3=1)
c = f('hello', p3='hello')
ic(a, b, c)

selection = get_url_info_db(DATABASE_URL, name='website')

ic(selection)

selection = get_url_info_db(DATABASE_URL, id=11)
ic(selection)

id=13
selection = get_url_info_db(DATABASE_URL, id=13)
ic(selection)
