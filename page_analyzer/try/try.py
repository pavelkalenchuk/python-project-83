from validators import url
from urllib.parse import urlparse
from icecream import ic

url_adr = 'http://www.aq-plastic.ru/catalog/baki-dlya-vody/atv/atv_24.html'

parsed_url = urlparse(url_adr)
ic(parsed_url)
url_adr = f'{parsed_url.scheme}://{}'



