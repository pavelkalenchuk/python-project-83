import datetime as dt
from icecream import ic
from repository import get_url_checks_by_date, add_url_checks

a = dt.datetime.now()

print(a)
print(type(a))

b = str(a)
print(b)
print(type(b))

z = a.strftime("%Y-%m-%d")
print(z)

list_ = [
    (1, a),
    (2, a)
]

result = list(
    map(
        lambda t: (t[0], t[1].strftime("%Y-%m-%d")),
        list_
    )
)

ic(result)

add_url_checks(1)
add_url_checks(1)
add_url_checks(1)
query = get_url_checks_by_date(1)
ic(query)



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

add_url_checks(1)
add_url_checks(1)
add_url_checks(1)
query = get_url_checks_by_date(1)
ic(query)