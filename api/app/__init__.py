from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth


from api.post.services import get_posts_with_category, remove_post
from api.post.services import get_post_by_id, validate_and_add_post
from api.post.services import get_all_posts, validate_and_change_post

from api.category.services import validate_and_change_category, get_all_categories
from api.category.services import add_category_to_post, validate_and_add_category
from api.category.services import get_category_by_id, remove_category


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
    return jsonify({'all_posts': posts})


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = get_post_by_id(post_id, True)
    if not post:
        abort(404)
    with_category = request.args.get('with-category')
    if with_category or with_category == '':
        post = add_category_to_post(post)
    return jsonify(post)


@app.route('/blog/api/v1.0/posts', methods=['POST'])
@auth.login_required
def add_post():
    if not request.json:
        abort(400)
    post = validate_and_add_post(
        request.json.get('author', None),
        request.json.get('title', None),
        request.json.get('description', None),
        request.json.get('content', None)
    )
    if not post:
        abort(404)
    return jsonify(post)


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['PUT'])
@auth.login_required
def change_post(post_id):
    if not request.json:
        abort(400)
    response = validate_and_change_post(
        post_id,
        request.json.get('category_id', None),
        request.json.get('author', None),
        request.json.get('title', None),
        request.json.get('short_description', None),
        request.json.get('content', None)
    )
    if response['status'] == 0:
        abort(404)
    if response['status'] == 1:
        abort(400)
    return jsonify(response['value'])


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    result = remove_post(post_id)
    if result == False:
        abort(404)
    return jsonify({'result': True})


@app.route('/blog/api/v1.0/categories', methods=['GET'])
def get_categories():
    categories = get_all_categories()
    return jsonify({'all_categories': categories})


@app.route('/blog/api/v1.0/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = get_category_by_id(category_id)
    if not category:
        abort(404)
    return jsonify(category)


@app.route('/blog/api/v1.0/categories', methods=['POST'])
@auth.login_required
def add_category():
    if not request.json:
        abort(400)
    category = validate_and_add_category(
        request.json.get('title', None)
    )
    if not category:
        abort(404)
    return jsonify(category)



@app.route('/blog/api/v1.0/categories/<int:category_id>', methods=['PUT'])
@auth.login_required
def change_category(category_id):
    if not request.json:
        abort(400)
    response = validate_and_change_category(
        category_id,
        request.json.get('title', None)
    )
    if response['status'] == 0:
        abort(404)
    if response['status'] == 1:
        abort(400)
    return jsonify(response['value'])


@app.route('/blog/api/v1.0/categories/<int:category_id>', methods=['DELETE'])
@auth.login_required
def delete_category(category_id):
    result = remove_category(category_id)
    if result == False:
        abort(404)
    return jsonify({'result': True})