from api.category.db import all_categories
from api.post.db import all_posts

def find_category_by_id(category_id):
    category = list(filter(lambda c: c['id'] == category_id, all_categories))
    return category



def add_category_to_post(post):
    category = list(filter(lambda c: c['id'] == post['category_id'], all_categories))
    category = category[0]
    post_with_category = post.copy()
    post_with_category.pop('category_id')
    post_with_category['category'] = category
    return post_with_category


def is_category_id_exist(id):
    value = False
    for category in all_categories:
        if category['id'] == id:
            value = True
    return value


def validate_for_category(val):
    return isinstance(val, int) and is_category_id_exist(val)


def get_all_categories():
    return all_categories


def get_posts_with_category(posts):
    return list(map(add_category_to_post, posts))


def add_category(category):
    return all_categories.append(category)


def remove_category(category):
    return all_categories.remove(category)