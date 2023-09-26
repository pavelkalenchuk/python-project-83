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
    add_url,
    get_urls,
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
        return (
            render_template(
                "index.html",
                url=url,
            ),
            422,
        )

    parsed_url = urlparse(url)
    url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if not get_urls(name=url):
        url_id = add_url(url)
        flash("Страница успешно добавлена", "success")
    else:
        flash("Страница уже существует", "warning")
        url_id = get_urls(name=url)['id']

    return redirect(url_for("url_page", id=url_id))


@app.route("/urls/<id>")
def url_page(id):
    id = int(id)
    messages = get_flashed_messages(with_categories=True)
    url_info = get_urls(id=id)
    url_checks = get_url_checks_by_date(id)
    for url_check in url_checks:
        url_check['created_at'] = url_check['created_at'].strftime("%Y-%m-%d")
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
            updated_url = {}
            url_id = url["id"]
            if get_url_checks_by_date(url_id):
                last_check = get_url_checks_by_date(url_id)[0]
                dt_last_check = last_check["created_at"]
                dt_last_check = dt_last_check.strftime("%Y-%m-%d")
                code_last_check = last_check["status_code"]
            else:
                dt_last_check = ""
                code_last_check = ""
            updated_url["last_check"] = dt_last_check
            updated_url["status_code"] = code_last_check
            updated_url['id'] = url['id']
            updated_url['name'] = url['name']
            updated_urls.append(updated_url)
    return render_template(
        "urls/index.html",
        urls=updated_urls,
    )


@app.post("/urls/<url_id>/checks")
def url_checks(url_id):
    url_id = url_id
    url_name = get_urls(id=url_id)["name"]
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
