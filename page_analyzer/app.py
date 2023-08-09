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
from settings import SECRET_KEY
from urllib.parse import urlparse
from validators import url




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
    url_ = data['url']
    

""" @app.post("/urls")
def urls_post():
    url_address = request.form.в """

