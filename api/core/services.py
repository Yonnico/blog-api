from flask import request, abort

def validate_len(val):
    if len(val) == 0:
        abort(404)
    return


def validate_request(val):
    if val not in request.json:
        abort(400)
    return