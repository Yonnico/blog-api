from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth


from api.post.services import get_short_post, make_full_post
from api.post.services import add_post, find_post_by_id
from api.post.services import get_all_posts, remove_post

from api.category.services import get_posts_with_category, get_all_categories
from api.category.services import add_category_to_post, add_category
from api.category.services import find_category_by_id, validate_for_category
from api.category.services import remove_category

from api.core.services import validate_len, validate_request
from api.core.services import validate_for_str


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
    with_category = request.args.get('with-category')
    if with_category or with_category == '':
        posts = get_posts_with_category(posts)
    return jsonify({'all_posts': get_short_post(posts)})


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = find_post_by_id(post_id)
    validate_len(post)
    post = post[0]
    with_category = request.args.get('with-category')
    if with_category or with_category == '':
        post = add_category_to_post(post)
    return jsonify(make_full_post(post))


@app.route('/blog/api/v1.0/posts', methods=['POST'])
@auth.login_required
def create_post():
    if not request.json:
        abort(400)
    validate_request('author')
    validate_request('title')
    validate_request('content')
    validate_request('category_id')
    if 'author' in request.json:
        if not validate_for_str(request.json['author']):
            abort(400)
    if 'title' in request.json:
        if not validate_for_str(request.json['title']):
            abort(400)
    if 'short_description' in request.json:
        if not validate_for_str(request.json['short_description']):
            abort(400)
    if 'content' in request.json:
        if not validate_for_str(request.json['content']):
            abort(400)
    if 'category_id' in request.json:
        if not validate_for_category(request.json['category_id']):
            abort(400)
    posts = get_all_posts()
    id = posts[-1]['id'] + 1
    post = {
        'id': id,
        'category_id':request.json['category_id'],
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
    post = post[0]
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
    if 'category_id' in request.json:
        if not validate_for_category(request.json['category_id']):
            abort(400)
    post['author'] = request.json.get('author', post['author'])
    post['title'] = request.json.get('title', post['title'])
    post['short_description'] = request.json.get('short_description', post['short_description'])
    post['content'] = request.json.get('content', post['content'])
    post['category_id'] = request.json.get('category_id', post['category_id'])
    return jsonify(post)


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    post = find_post_by_id(post_id)
    validate_len(post)
    post = post[0]
    remove_post(post)
    return jsonify({'result': True})


@app.route('/blog/api/v1.0/categories', methods=['GET'])
def get_categories():
    categories = get_all_categories()
    return jsonify({'all_categories': categories})


@app.route('/blog/api/v1.0/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = find_category_by_id(category_id)
    validate_len(category)
    category = category[0]
    return jsonify(category)


@app.route('/blog/api/v1.0/categories', methods=['POST'])
@auth.login_required
def create_category():
    if not request.json:
        abort(400)
    validate_request('name')
    if 'name' in request.json:
        if not validate_for_str(request.json['name']):
            abort(400)
    categories = get_all_categories()
    id = categories[-1]['id'] + 1
    category = {
        'id': id,
        'name':request.json['name']
    }
    add_category(category)
    return jsonify(category)



@app.route('/blog/api/v1.0/categories/<int:category_id>', methods=['PUT'])
@auth.login_required
def edit_category(category_id):
    category = find_category_by_id(category_id)
    validate_len(category)
    category = category[0]
    if not request.json:
        abort(400)
    if 'name' in request.json:
        if not validate_for_str(request.json['name']):
            abort(400)
    category['name'] = request.json.get('name', category['name'])
    return jsonify(category)


@app.route('/blog/api/v1.0/categories/<int:category_id>', methods=['DELETE'])
@auth.login_required
def delete_category(category_id):
    category = find_category_by_id(category_id)
    validate_len(category)
    category = category[0]
    remove_category(category)
    return jsonify({'result': True})