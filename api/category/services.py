from api.category.db import all_categories
from api.post.db import all_posts

from api.category.validation import  validate_title


def get_category_by_id(category_id):
    category = list(filter(lambda c: c['id'] == category_id, all_categories))
    if len(category):
        return category[0]
    return None



def add_category_to_post(post):
    if 'category_id' in post:
        category = list(filter(lambda c: c['id'] == post['category_id'], all_categories))
        category = category[0]
        post_with_category = post.copy()
        post_with_category.pop('category_id')
        post_with_category['category'] = category
        return post_with_category
    return post


def get_all_categories():
    return all_categories


def remove_category(category_id):
    category = get_category_by_id(category_id)
    if category != None:
        posts = list(filter(lambda p: p['category_id'] == category['id'], all_posts))
        if posts != None:
            for post in posts:
                post.pop('category_id')
            return all_categories.remove(category)
    return False


def validate_and_add_category(title):
    if not private_validate_category(title, True):
        return None
    return private_add_category(title)


def private_validate_category(title, required):
    if required or 'title' != None:
        if not validate_title(title):
            return False
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
    if not private_validate_category(title, False):
        return {'status': 1, 'value': None}
    if title is not None:
        category['title'] = title
    return {'status': 2, 'value': category}