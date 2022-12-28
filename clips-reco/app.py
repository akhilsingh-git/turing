import env
import time
import logging
from pythonjsonlogger import jsonlogger
from logging.handlers import WatchedFileHandler
from flask import Flask, current_app as app, request, jsonify, make_response, abort

from recommenders.clips_recommender import init_clips_models, get_all_recommended_clips
from error_handlers import unauthorized_request_handler, bad_request_handler
from middlewares.auth_middlewares import internal_auth_required

from env import LOG_FILE_PATH

formatter = jsonlogger.JsonFormatter()

log_handler = WatchedFileHandler(LOG_FILE_PATH)
log_handler.setFormatter(formatter)

app_logger = logging.getLogger()
app_logger.addHandler(log_handler)
app_logger.setLevel(logging.DEBUG)

model_load_start_time = time.time()
init_clips_models()
app_logger.info(msg={
    "func": "model_load_time",
    "time": time.time() - model_load_start_time
})

app = Flask(__name__)

app.config["CLIENT_ID"] = env.CLIENT_ID
app.config["CLIENT_SECRET"] = env.CLIENT_SECRET

app.register_error_handler(401, unauthorized_request_handler)
app.register_error_handler(400, bad_request_handler)


@app.route("/api/v1/clips/", methods=["GET"])
@internal_auth_required
def get_recommended_clips():
    app_logger.info("reached get_recommended_clips")
    query_params = request.args
    user_id = query_params.get("user_id")

    if user_id is None or len(user_id.strip()) == 0:
        abort(400, "user_id query param is required!")

    formatted_user_uid = "u_{}".format(user_id)

    recommended_clips = []
    try:
        start_time = time.time()
        recommended_clips = get_all_recommended_clips(formatted_user_uid)
        app_logger.info(msg={
            "func": "model_exec_time",
            "time": time.time() - start_time,
            "clips_length": len(recommended_clips),
            "user_id": user_id
        })
    except Exception as e:
        app_logger.error(msg=str(e))

    data = {
        "clip_uids": recommended_clips
    }

    return make_response(jsonify(data=data), 200)

@app.route("/health/", methods=["GET"])
def get_health():
    data = {
        "message": "health"
    }

    return make_response(jsonify(data=data), 200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
