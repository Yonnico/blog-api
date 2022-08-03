from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth


from api.post.services import make_short_post, make_full_post, find_post_by_id
from api.post.services import validate_for_str, add_post
from api.post.services import get_all_posts, remove_post

from api.core.services import validate_len, validate_request


app = Flask(__name__)


auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'password'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/blog/api/v1.0/posts', methods=['GET'])
def get_posts():
    posts = get_all_posts()
    posts = list(map(make_short_post, posts))
    return jsonify({'all_posts': posts})


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = find_post_by_id(post_id)
    validate_len(post)
    post = make_full_post(post[0])
    return jsonify(post)


@app.route('/blog/api/v1.0/posts', methods=['POST'])
@auth.login_required
def create_post():
    if not request.json:
        abort(400)
    validate_request('author')
    validate_request('title')
    validate_request('content')
    if 'author' in request.json:
        if not validate_for_str('author'):
            abort(400)
    if 'title' in request.json:
        if not validate_for_str('title'):
            abort(400)
    if 'short_description' in request.json:
        if not validate_for_str('short_description'):
            abort(400)
    if 'content' in request.json:
        if not validate_for_str('content'):
            abort(400)
    posts = get_all_posts()
    id = posts[-1]['id'] + 1
    post = {
        'id': id,
        'author':request.json['author'],
        'title':request.json['title'],
        'short_description':request.json.get('short_description', ''),
        'content':request.json['content']
    }
    add_post(post)
    return jsonify(post)


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['PUT'])
@auth.login_required
def change_post(post_id):
    post = find_post_by_id(post_id)
    validate_len(post)
    if not request.json:
        abort(400)
    if 'author' in request.json:
        if not validate_for_str(request.json['author']):
            abort(400)
    if 'title' in request.json:
        if not validate_for_str(request.json['title']):
            abort(400)
    if 'short_description' in request.json:
        if not isinstance(request.json['short_description'], str):
            abort(400)
    if 'content' in request.json:
        if not validate_for_str(request.json['content']):
            abort(400)
    post = post[0]
    post['author'] = request.json.get('author', post['author'])
    post['title'] = request.json.get('title', post['title'])
    post['short_description'] = request.json.get('short_description', post['short_description'])
    post['content'] = request.json.get('content', post['content'])
    return jsonify(post)


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    post = find_post_by_id(post_id)
    post = post[0]
    validate_len(post)
    remove_post(post)
    return jsonify({'result': True})