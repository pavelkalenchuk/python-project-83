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


from icecream import ic

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    ic('index loaded')
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages = messages
    )

@app.post("/")
def url_post():
    # data = request.form.to_dict()
    # url = data['url_adr']
    url = request.form.get('url')
    validated_url = validate_url(url)

    if not validated_url or len(url) > 255:
        if len(url) > 255:
            flash('URL превышает 255 символов', 'danger')
            flash('Некорректный URL', 'danger')
        if not validated_url.value:
            flash('Некорректный URL', 'danger')
            flash('URL обязателен', 'danger')
        else:
            flash('Некорректный URL', 'danger')
        return render_template(
            'urls/try.html',
            url = url,
        )

    parsed_url = urlparse(url)
    url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    # проверка на наличие URL в БД:
    if not get_url_info_db(name=url):
        add_url_db(url)
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'warning')

    url_info = get_url_info_db(name=url)
    id_url = url_info['id']
    return redirect(
        url_for('url_page', id=id_url)
    )


@app.route('/urls/<id>')
def url_page(id):
    messages = get_flashed_messages(with_categories=True)
    url_info = get_url_info_db(id=id)
    return render_template(
        'urls/show.html',
        messages = messages,
        url_info=url_info
    )


@app.route('/urls')
def get_urls():
    render_template(
        'urls/index.html'
    )
