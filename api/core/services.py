from flask import request, abort

def validate_len(val):
    if len(val) == 0:
        return abort(404)
    return


def validate_request(val):
    if val not in request.json:
        return abort(400)
    return


def validate_for_str(val):
    return isinstance(val, str) and len(val)
