from page_analyzer.parser import parse_url
from page_analyzer.repository import add_url_check, get_url_checks_by_date
from icecream import ic


site = "https://ru.hexlet.io"

parsed_site = parse_url(site)

ic(parsed_site)

add_url_check(1, parsed_site)
add_url_check(1, parsed_site)
add_url_check(1, parsed_site)
add_url_check(1, parsed_site)
add_url_check(1, parsed_site)


url_checks = get_url_checks_by_date(1)
ic(url_checks)
