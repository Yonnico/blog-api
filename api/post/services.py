from api.post.db import all_posts


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


def find_post_by_id(post_id):
    post = list(filter(lambda p: p['id'] == post_id, all_posts))
    return post


def get_all_posts():
    return all_posts


def add_post(post):
    return all_posts.append(post)


def remove_post(post):
    return all_posts.remove(post)