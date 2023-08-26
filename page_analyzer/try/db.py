from page_analyzer.repository import get_url_info_db, add_url_db, get_urls_by_date, get_url_checks_by_date
from icecream import ic

urls = get_urls_by_date()
#ic(urls)


new_urls = []
for url in urls:
    url_id = url['id']
    if get_url_checks_by_date(url_id):
        url_last_check = get_url_checks_by_date(url_id)[0]
        ic(url_last_check)
        dt_last_check = url_last_check['created_at']
    else:
        dt_last_check = ''
    url['last_check'] = dt_last_check
    new_urls.append(url)


ic(new_urls)

