from icecream import ic
from validators import url
from urllib.parse import urlparse


url_valid = 'http://validators.readthedocs.io/url/super_url'
url2_notvalid = 'blabla.ru'
url3_empty = ''

urls = [
    'http://validators.readthedocs.io/url/super_url',
    'blabla.ru',
     ''    
]
result = list(map(bool, (map(url, urls))))
ic(result)

adress = "https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python/835527#835527"
ic(urlparse(adress))
site_url = urlparse(adress)
normolized_url = f'{site_url.scheme}://{site_url.netloc}'
ic(normolized_url)
