"""
Note: Need to have required models in the /recommenders/models/ directory in the codebase 
to run.
"""
import os
import time
import pickle
import logging

# Todo: Rename me for better context
G = None

# Scores the clip to clip score relation matrix
ScoreMatrix = None


def get_clip_max_score(clip_uid):
    return ScoreMatrix[clip_uid]["information"]["Maxscore"]


def init_clips_models():
    model_load_start_time = time.time()

    global G
    global ScoreMatrix

    models_dir = os.path.join(os.getcwd(), "recommenders", "models")

    with open(os.path.join(models_dir, "watch_history_graph.sav"), "rb") as f:
        G = pickle.load(f)

    with open(os.path.join(models_dir, "video_score_matrix.sav"), "rb") as f:
        ScoreMatrix = pickle.load(f)

    logging.info(msg={
        "func": "init_clips_models",
        "message": "model_load_time",
        "time_taken_ms": ((time.time() - model_load_start_time) * 1000),
    })


def get_all_recommended_clips(formatted_user_uid):
    """
    Recommends the full set of clips for a user present at the time
    the model was trained.

    params:
        formatted_user_uid -> Format: "u_{user_id}"
    """
    result_clip_to_score_mapping = {}

    # -1 is used for non logged in users
    # Solves cold start problem
    if not G.has_node(formatted_user_uid):
        formatted_user_uid = "u_-1"

    # Already watched videos by the user
    # Embedded in the model while training
    lifetime_watch_history = list(set(G.neighbors(formatted_user_uid)))
    lifetime_watch_history.sort(reverse=True, key=get_clip_max_score)

    for source_clip_id in lifetime_watch_history[:20]:
        related_score_matrix = ScoreMatrix[source_clip_id]["relation"]
        related_clips_ids = list(related_score_matrix.keys())

        for suggested_clip_id in related_clips_ids:
            if suggested_clip_id not in result_clip_to_score_mapping:
                result_clip_to_score_mapping[suggested_clip_id] = related_score_matrix[suggested_clip_id]

            result_clip_to_score_mapping[suggested_clip_id] = max(
                result_clip_to_score_mapping[suggested_clip_id], related_score_matrix[suggested_clip_id]
            )

    for watched_clip in lifetime_watch_history:
        result_clip_to_score_mapping[watched_clip] = -1

    results = list(result_clip_to_score_mapping.keys())

    def get_result_mapping_scores(clip_uid):
        return result_clip_to_score_mapping[clip_uid]

    results.sort(reverse=True, key=get_result_mapping_scores)
    results = results[:1000]

    final_clips_scores = {}
    for clip_uid in results:
        final_clips_scores[clip_uid] = result_clip_to_score_mapping[clip_uid]

    return final_clips_scores
