import env
import time
from flask import Flask, current_app as app, request, jsonify, make_response, abort


from logger import app_logger
from recommenders.clips_recommender import init_clips_models, get_all_recommended_clips
from error_handlers import unauthorized_request_handler, bad_request_handler
from middlewares.auth_middlewares import internal_auth_required


def create_app():
    model_load_start_time = time.time()
    init_clips_models()
    app_logger.debug(
        msg={"model_load_time": time.time() - model_load_start_time}
    )

    app = Flask(__name__)

    app.config["CLIENT_ID"] = env.CLIENT_ID
    app.config["CLIENT_SECRET"] = env.CLIENT_SECRET

    app.register_error_handler(401, unauthorized_request_handler)
    app.register_error_handler(400, bad_request_handler)

    @app.route("/api/v1/clips/", methods=["GET"])
    @internal_auth_required
    def get_recommended_clips():
        query_params = request.args
        user_id = query_params.get("user_id")

        if user_id is None or len(user_id.strip()) == 0:
            abort(400, "user_id query param is required!")

        formatted_user_uid = "u_{}".format(user_id)

        # # Todo: Log my time
        # print("Execution time new: " + str(time.time() - start_time))
        recommended_clips = []

        try:
            recommended_clips = get_all_recommended_clips(formatted_user_uid)
        except Exception as e:
            # # Todo: Log me
            print(e)

        data = {
            "clip_uids": recommended_clips
        }

        return make_response(jsonify(data=data), 200)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=False)
