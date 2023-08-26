import datetime as dt
from icecream import ic
from page_analyzer.repository import [
    get
]


check = get_url_checks_by_date(2)

ic(check[0])