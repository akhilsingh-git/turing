from flask import Flask, request, jsonify, make_response
from constants import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)


@app.route("/api/v1/user/<user_uid>/clips/")
def get_recommended_clips(user_uid):
    client_id = request.headers.get('X-CLIENT-ID')
    client_secret = request.headers.get('X-CLIENT-SECRET')

    if client_id == CLIENT_ID and client_secret == CLIENT_SECRET:
        data = {
            "clip_uids": ["abcd", "efgh", "hijk"]
        }
        return make_response(jsonify(data = data), 200)
    else:
        return make_response(jsonify(error="wrong auth credentials"), 401)
