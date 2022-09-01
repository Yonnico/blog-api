from api.core.validation import is_str


def validate_author(val):
    return is_str(val) and len(val)


def validate_title(val):
    return is_str(val) and len(val)


def validate_s_d(val):
    return is_str(val) and len(val)


def validate_s_d_for_change(val):
    return is_str(val)


def validate_content(val):
    return is_str(val) and len(val)