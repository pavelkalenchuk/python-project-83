from page_analyzer.repository import get_url_info_db, add_url_db, get_urls_by_date
from icecream import ic

urls = get_urls_by_date()


ic(urls)
