import pytest

from page_analyzer.validator import validate_url
from page_analyzer.validator import validate_url_url
from page_analyzer.validator import validate_len_url
from page_analyzer.validator import validate_url_empry


validate_len_url_data = [
    ('https://www.yandex.ru', True),
    ('x' * 256, False),
]

validate_url_url_data = [
    ()
]


@pytest.mark.parametrize('url_adr, result', validate_len_url_data)
def test_validate_len_url(url_adr, result):
    assert validate_len_url(url_adr) == result


@pytest.mark.parametrize('url_adr, result', validate_url_url_data)
def test_validate_url_url(url_adr, result):
    assert validate_url_url(url_adr) == result
