from api.category.db import all_categories

from api.post.services import get_all_posts

from api.category.validation import validate_title

#FOR CONTROLLER

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

#FOR VIEW

def get_category_by_id(category_id):
    category = list(filter(lambda c: c['id'] == category_id, all_categories))
    if len(category):
        return category[0]
    return None


def get_all_categories():
    return all_categories


def remove_category(category_id):
    category = get_category_by_id(category_id)
    posts = get_all_posts()
    if category != None:
        link = list(filter(lambda p: p['category_id'] == category['id'], posts))
        if link != None:
            for post in link:
                post.pop('category_id')
            return all_categories.remove(category)
    return False


def validate_and_add_category(title):
    if not private_validate_category(title, True):
        return None
    return private_add_category(title)


def validate_and_change_category(category_id, title):
    category = get_category_by_id(category_id)
    if not category:
        return {'status': 0, 'value': None}
    if not private_validate_category(title, False):
        return {'status': 1, 'value': None}
    if title is not None:
        category['title'] = title
    return {'status': 2, 'value': category}