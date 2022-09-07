from api.category.db import all_categories
from api.core.validation import is_str, is_int


def validate_title(val):
    return val != None and is_str(val) and len(val)


def is_category_id_exist(id):
    value = False
    for category in all_categories:
        if category['id'] == id:
            value = True
    return value


def validate_category(val):
    return val != None and is_int(val) and is_category_id_exist(val)