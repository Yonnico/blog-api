from api.core.validation import is_str


def validate_author(val):
    return val != None and is_str(val) and len(val)


def validate_title(val):
    return val != None and is_str(val) and len(val)


def validate_description(val):
    return val != None and is_str(val) and len(val)


def validate_content(val):
    return val != None and is_str(val) and len(val)