from flask import jsonify, make_response


def unauthorized_request_handler(e):
    error_message = e.description
    return make_response(jsonify({
        "message": error_message,
    }), 401)


def bad_request_handler(e):
    error_message = e.description
    return make_response(jsonify({
        "message": error_message,
    }), 400)
