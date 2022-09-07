from flask import request

from api.category.db import all_categories

from api.category.validation import validate_title


def get_category_by_id(category_id):
    category = list(filter(lambda c: c['id'] == category_id, all_categories))
    if len(category):
        return category[0]
    return None



def add_category_to_post(post):
    category = list(filter(lambda c: c['id'] == post['category_id'], all_categories))
    category = category[0]
    post_with_category = post.copy()
    post_with_category.pop('category_id')
    post_with_category['category'] = category
    return post_with_category


def get_all_categories():
    return all_categories


def remove_category(category):
    return all_categories.remove(category)


def validate_and_add_category(title):
    if not private_validate_category(title):
        return None
    return private_add_category(title)


def private_validate_category(title):
    if not request.json:
        return None
    if not 'title' in request.json:
        return None
    if 'title' in request.json:
        if not validate_title(title):
            return None
    return True


def private_add_category(title):
    id = all_categories[-1]['id'] + 1
    category = {
        'id': id,
        'title': title
    }
    all_categories.append(category)
    return category


def validate_and_change_category(category_id, title):
    category = get_category_by_id(category_id)
    if not category:
        return {'status': 0, 'value': None}
    if not request.json:
        return {'status': 1, 'value': "No request"}
    if title is not None and not validate_title(title):
        return {'status': 1, 'value': title}
    if title is not None:
        category['title'] = title
    return {'status': 2, 'value': category}