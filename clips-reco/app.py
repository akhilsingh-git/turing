from flask import Flask, request, jsonify, make_response
from constants import CLIENT_ID, CLIENT_SECRET
from recommender import recommend_video

app = Flask(__name__)


@app.route("/api/v1/user/<user_uid>/clips/")
def get_recommended_clips(user_uid):
    client_id = request.headers.get('X-CLIENT-ID')
    client_secret = request.headers.get('X-CLIENT-SECRET')

    if client_id == CLIENT_ID and client_secret == CLIENT_SECRET:
        formatted_user_uid = "u_{}".format(user_uid)
        recommended_clips = []
        
        try:
            recommended_clips = recommend_video(formatted_user_uid)
        except Exception as e:
            print(e)

        data = {
            "clip_uids": recommended_clips
        }
        return make_response(jsonify(data = data), 200)
    else:
        return make_response(jsonify(error="wrong auth credentials"), 401)
