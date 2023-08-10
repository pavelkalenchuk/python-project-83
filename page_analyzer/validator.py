from validators import url
from icecream import ic


MAX_CHARS = 255

def validate_len_url(url_adr):
    return False if len(url_adr) > MAX_CHARS else True


def validate_url_url(url_adr):
    return False if not url(url_adr) else True


def validate_url_empry(url_adr):
    return False if not url_adr else True


def validate_url(url_adr):
    validators_list = [
        validate_len_url(url_adr),
        validate_url_url(url_adr),
        validate_url_empry(url_adr)
    ]
    return False if False in validators_list else True

ic(type(url('https://www.yandex.ru')))
ic(url('https://www.yandex.ru'))
ic((type(url(''))))
ic((url('')))
print((url('')))



