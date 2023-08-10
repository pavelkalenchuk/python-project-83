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
from repository import add_url_to_db


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template(
        'index.html'
    )

@app.post("/urls")
def urls_post():
    data = request.form.to_dict()
    url = data['url_adr']
    validated_url = validate_url(url)
    if not validated_url or len(url) > 255:
        if len(url) > 255:
            flash('URL превышает 255 символов', 'error')
            flash('Некорректный URL', 'error')
        if not validated_url.value:
            flash('Некорректный URL')
            flash('URL обязателен', 'error')
        else:
            flash('Некорректный URL', 'error')
        return render_template(
            '/',
            url = url
        )
    # добавляем в БД
    add_url_to_db(url, DATABASE_URL)
    flash('Страница успешно добавлена', 'success')
    
    
    
