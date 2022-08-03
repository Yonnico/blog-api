from api.post.db import all_posts

def make_short_post(post):
    return{
        "id": post['id'],
        "author": post['author'],
        "title": post['title'],
        "short_description": post['short_description']
    }


def make_full_post(post):
    return{
        "id": post['id'],
        "author": post['author'],
        "title": post['title'],
        "content": post['content']
    }


def find_post_by_id(post_id):
    post = list(filter(lambda p: p['id'] == post_id, all_posts))
    return post


def get_all_posts():
    return all_posts


def add_post(val):
    return all_posts.append(val)


def validate_for_str(val):
    return isinstance(val, str) and len(val)


def remove_post(post):
    return all_posts.remove(post)