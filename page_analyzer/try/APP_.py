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
import os

from page_analyzer.database import PostsRepository
from validator import validate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello_world'


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/posts')
def posts_get():
    repo = PostsRepository()
    messages = get_flashed_messages(with_categories=True)
    posts = repo.content()
    return render_template(
        'posts/index.html',
        posts=posts,
        messages=messages,
        )


@app.route('/posts/new')
def new_post():
    post = {}
    errors = {}
    return render_template(
        'posts/new.html',
        post=post,
        errors=errors,
    )


@app.post('/posts')
def posts_post():
    repo = PostsRepository()
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'posts/new.html',
            post=data,
            errors=errors,
            ), 422
    id = repo.save(data)
    flash('Post has been created', 'success')
    resp = make_response(redirect(url_for('posts_get')))
    resp.headers['X-ID'] = id
    return resp


@app.route('/posts/<id>/update', methods=['GET', 'POST'])
def post_update(id):
    repo = PostsRepository()
    post = repo.find(id)
    errors = []

    if request.method == 'GET':
        return render_template(
                'posts/edit.html',
                post=post,
                errors=errors,
                data=post,
                )

    if request.method == 'POST':
        data = request.form.to_dict()

        errors = validate(data)
        if errors:
            return render_template(
                'posts/edit.html',
                post=post,
                data=data,
                errors=errors,
                ), 422

        post['title'] = data['title']
        post['body'] = data['body']
        repo.save(post)
        flash('Post has been updated', 'success')
        return redirect(url_for('posts_get'))


# BEGIN (write your solution here)
@app.route('/posts/<id>/delete', methods=['POST'])
def post_delete(id):
    repo = PostsRepository()
    repo.destroy(id)
    flash('Post has been deleted')
    return redirect(url_for('posts_get'))
# END
