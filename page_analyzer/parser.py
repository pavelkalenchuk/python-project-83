import requests

from bs4 import BeautifulSoup


def parse_url(url):
    response = requests.get(url)
    status_code = response.status_code
    content_ = response.content
    html = BeautifulSoup(content_, "html.parser")
    if html.title:
        title = html.title.string
    else:
        title = ""
    if html.h1:
        h1 = html.h1.string
    else:
        h1 = ""
    meta_tags = html.find_all("meta")
    meta_attrs_content = [
        meta.attrs["content"]
        for meta in meta_tags
        if "name" in meta.attrs and meta.attrs["name"] == "description"
    ]
    if meta_attrs_content:
        description = meta_attrs_content[0]
    else:
        description = ""
    return {
        "status_code": status_code,
        "h1": h1,
        "title": title,
        "description": description,
    }
