from flask import ( # noqa F401
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from settings import SECRET_KEY
from urllib.parse import urlparse
from validators import url as validate_url
from page_analyzer.repository import (
    add_url_db,
    get_url_info_db,
    get_urls_by_date,
    add_url_checks,
    get_url_checks_by_date
)


from icecream import ic # noqa F401

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/urls")
def urls_post():
    url = request.form.get("url")
    validated_url = validate_url(url)

    if not validated_url or (len(url) > 255 and validate_url):
        if len(url) > 255:
            flash("URL превышает 255 символов", "danger")
        elif not validated_url.value:
            flash("URL обязателен", "danger")
        else:
            flash("Некорректный URL", "danger")
        return render_template(
            "index.html",
            url=url,
        )

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
        url_checks = url_checks
    )


@app.route("/urls")
def urls_get():
    urls = get_urls_by_date()
    if urls:
        updated_urls = []
        for url in urls:
            url_id = url['id']
            if get_url_checks_by_date(url_id):
                url_last_check = get_url_checks_by_date(url_id)[0]
                ic(url_last_check)
                dt_last_check = url_last_check['created_at']
            else:
                dt_last_check = ''
            url['last_check'] = dt_last_check
            updated_urls.append(url)
    return render_template(
        "urls/index.html",
        urls = updated_urls,
    )


@app.post("/urls/<url_id>/checks")
def url_checks(url_id):
    url_id = id
    add_url_checks(url_id)
    flash("Страница успешно проверена", "success")
    return redirect(
        url_for("url_page", id = url_id)
    )