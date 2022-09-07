from api.post.db import all_posts

from api.category.services import add_category_to_post

from api.category.validation import validate_category

from api.post.validation import validate_author, validate_content, validate_title
from api.post.validation import validate_description


def make_short_post(post):
    short_post = post.copy()
    short_post.pop('content')
    return short_post


def make_full_post(post):
    full_post = post.copy()
    full_post.pop('description')
    return full_post


def get_posts_with_category(posts):
    return list(map(add_category_to_post, posts))


def get_post_by_id(post_id, isFull = False):
    post = list(filter(lambda p: p['id'] == post_id, all_posts))
    if len(post):
        if isFull:
            return make_full_post(post[0])
        return make_short_post(post[0])
    return None


def get_all_posts(isFull = False):
    value = all_posts
    if isFull:
        return list(map(make_full_post, value))
    return list(map(make_short_post, value))


def remove_post(post_id):
    post = get_post_by_id(post_id)
    if post != None:
        return all_posts.remove(post)
    return False


def validate_and_add_post(author, title, description, content):
    if not private_validate_post(author, title, description, content, True):
        return None
    return private_add_post(author, title, description, content)


def private_validate_post(author, title, description, content, required):
    if required or author != None:
        if not validate_author(author):
            return False
    if required or title != None:
        if not validate_title(title):
            return False
    if required or description != None:
        if not validate_description(description):
            return False
    if required or content != None:
        if not validate_content(content):
            return False
    return True


def private_add_post(author, title, description, content):
    id = all_posts[-1]['id'] + 1
    post = {
        'id': id,
        'author': author,
        'title': title,
        'description': description,
        'content': content
    }
    all_posts.append(post)
    return post


def validate_and_change_post(post_id, category_id, author, title, description, content):
    post = get_post_by_id(post_id)
    if not post:
        return {'status': 0, 'value': None}
    if not private_validate_post(author, title, description, content, False):
        return{'status': 1, 'value': None}
    if category_id != None:
        if not validate_category(category_id):
            return{'status': 1, 'value': 'category_id'}
    if category_id != None:
        post['category_id'] = category_id
    if author != None:
        post['author'] = author
    if title != None:
        post['title'] = title
    if description != None:
        post['description'] = description
    if content != None:
        post['content'] = content
    return {'status': 2, 'value': post}