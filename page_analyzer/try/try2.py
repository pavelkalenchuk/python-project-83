from icecream import ic
from validators import url
from urllib.parse import urlparse


url_ = 'http://validators.readthedocs.io/url/super_url'

a = url(url_)
ic(a)
ic(type(a))

if a:
    ic('valid')
else:
    ic('not valid')

adress = "https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python/835527#835527"
ic(urlparse(adress))
site_url = urlparse(adress)
normolized_url = f'{site_url.scheme}://{site_url.netloc}'
ic(normolized_url)




