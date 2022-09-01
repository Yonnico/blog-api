from flask import request

from api.post.db import all_posts

from api.category.validation import validate_category

from api.post.validation import validate_author, validate_content, validate_title
from api.post.validation import validate_s_d, validate_s_d_for_change


def make_short_post(post):
    short_post = post.copy()
    short_post.pop('content')
    return short_post


def make_full_post(post):
    full_post = post.copy()
    full_post.pop('short_description')
    return full_post


def get_short_post(posts):
    return list(map(make_short_post, posts))


def get_post_by_id(post_id):
    post = list(filter(lambda p: p['id'] == post_id, all_posts))
    if len(post):
        return post[0]
    return None


def get_all_posts():
    return all_posts


def remove_post(post):
    return all_posts.remove(post)


def validate_and_add_post(category_id, author, title, short_description, content):
    id = all_posts[-1]['id'] + 1
    post = post = {
        'id': id,
        'category_id': 0,
        'author': 0,
        'title': 0,
        'short_description': 0,
        'content': 0
    }
    if not request.json:
        return {'status': 1, 'value': "No request"}
    if not validate_category(category_id):
        return {'status': 1, 'value': category_id}
    if not validate_author(author):
        return {'status': 1, 'value': author}
    if not validate_title(title):
        return {'status': 1, 'value': title}
    if not validate_s_d(short_description):
        return {'status': 1, 'value': short_description}
    if not validate_content(content):
        return {'status': 1, 'value': content}
    post['category_id'] = category_id
    post['author'] = author
    post['title'] = title
    post['short_description'] = short_description
    post['content'] = content
    all_posts.append(post)
    return {'status': 2, 'value': post}

def validate_and_change_post(post_id, category_id, author, title, short_description, content):
    post = get_post_by_id(post_id)
    if not post:
        return {'status': 0, 'value': None}
    if not request.json:
        return {'status': 1, 'value': "No request"}
    if category_id is not None and not validate_category(category_id):
        return {'status': 1, 'value': category_id}
    if author is not None and not validate_author(author):
        return {'status': 1, 'value': author}
    if title is not None and not validate_title(title):
        return {'status': 1, 'value': title}
    if short_description is not None and not validate_s_d_for_change(short_description):
        return {'status': 1, 'value': short_description}
    if content is not None and not validate_content(content):
        return {'status': 1, 'value': content}
    if category_id is not None:
        post['category_id'] = category_id
    if author is not None:
        post['author'] = author
    if title is not None:
        post['title'] = title
    if short_description is not None:
        post['short_description'] = short_description
    if content is not None:
        post['content'] = content
    return {'status': 2, 'value': post}