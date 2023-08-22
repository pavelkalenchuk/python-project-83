from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from settings import SECRET_KEY, DATABASE_URL
from urllib.parse import urlparse
from validators import url as validate_url
from page_analyzer.repository import add_url_db, get_url_info_db


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template(
        'index.html'
    )

@app.route("/goto_url", methods=["POST"])
def urls_post():
    # data = request.form.to_dict()
    # url = data['url_adr']
    url = request.form.get('url')
    validated_url = validate_url(url)

    if not validated_url or len(url) > 255:
        if len(url) > 255:
            flash('URL превышает 255 символов', 'error')
            flash('Некорректный URL', 'error')
        if not validated_url.value:
            flash('Некорректный URL', 'error')
            flash('URL обязателен', 'error')
        else:
            flash('Некорректный URL', 'error')
        return render_template(
            '/',
            url = url
        ), 422
    parsed_url = urlparse(url)
    url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    # проверка на наличие URL в БД:
    if not get_url_info_db(url, DATABASE_URL):
        add_url_db(url, DATABASE_URL)
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'success')

    url_info = get_url_info_db(url, DATABASE_URL)
    id_url = url_info['id']
    return redirect(
        url_for(
        'url_page',
        id = id_url,
        )
    )


@app.route('/urls/<id>')
def url_page(id):
    messages = get_flashed_messages(with_categories=True)
    url_info = get_url_info_db(DATABASE_URL, id=id)
    return render_template(
        'urls/show.html'
    )

