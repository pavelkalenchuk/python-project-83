import requests

from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from urllib.parse import urlparse
from validators import url as validate_url
from page_analyzer.parser import parse_url
from page_analyzer.repository import (
    psql_db,
    add_url_db,
    get_url_info_db,
    get_urls_by_date,
    add_url_check,
    get_url_checks_by_date,
)
from settings import SECRET_KEY


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
psql_db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/urls")
def urls_post():
    url = request.form.get("url")
    validated_url = validate_url(url)

    if not validated_url or (len(url) > 255 and validate_url):
        if len(url) > 255:
            flash("URL превышает 255 символов", "dark")
        elif not validated_url.value:
            flash("URL обязателен", "dark")
        else:
            flash("Некорректный URL", "dark")
        return render_template(
            "index.html",
            url=url,
        ), 422

    parsed_url = urlparse(url)
    url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if not get_url_info_db(name=url):
        add_url_db(url)
        flash("Страница успешно добавлена", "success")
    else:
        flash("Страница уже существует", "warning")

    url_info = get_url_info_db(name=url)
    url_id = url_info["id"]
    return redirect(url_for("url_page", id=url_id))


@app.route("/urls/<id>")
def url_page(id):
    messages = get_flashed_messages(with_categories=True)
    url_info = get_url_info_db(id=id)
    url_checks = get_url_checks_by_date(id)
    return render_template(
        "urls/show.html",
        messages=messages,
        url_info=url_info,
        url_checks=url_checks
    )


@app.route("/urls")
def urls_get():
    urls = get_urls_by_date()
    updated_urls = []
    if urls:
        for url in urls:
            url_id = url["id"]
            if get_url_checks_by_date(url_id):
                url_last_check = get_url_checks_by_date(url_id)[0]
                dt_last_check = url_last_check["created_at"]
                status_code_last_check = url_last_check["status_code"]
            else:
                dt_last_check = ""
                status_code_last_check = ""
            url["last_check"] = dt_last_check
            url["status_code"] = status_code_last_check
            updated_urls.append(url)
    return render_template(
        "urls/index.html",
        urls=updated_urls,
    )


@app.post("/urls/<url_id>/checks")
def url_checks(url_id):
    url_id = url_id
    url_name = get_url_info_db(id=url_id)["name"]
    try:
        r = requests.get(url_name)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        flash("Произошла ошибка при проверке", "dark")
        return redirect(url_for("url_page", id=url_id))
    parsed_url = parse_url(url_name)
    add_url_check(url_id, parsed_url)
    flash("Страница успешно проверена", "success")
    return redirect(url_for("url_page", id=url_id))
