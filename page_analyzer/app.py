from flask import Flask
from flask import render_template
from settings import SECRET_KEY


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template(
        'index.html'
    )
