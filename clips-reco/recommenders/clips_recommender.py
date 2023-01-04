"""
Note: Need to have required models in the /recommenders/models/ directory in the codebase 
to run.
"""
import os
import pickle

# Todo: Rename me for better context
G = None

# Scores the clip to clip score relation matrix
ScoreMatrix = None


def get_clip_max_score(clip_uid):
    return ScoreMatrix[clip_uid]["Maxscore"]


def init_clips_models():
    global G
    global ScoreMatrix

    models_dir = os.path.join(os.getcwd(), "recommenders", "models")

    with open(os.path.join(models_dir, "watch_history_graph.sav"), "rb") as f:
        G = pickle.load(f)

    with open(os.path.join(models_dir, "video_score_matrix.sav"), "rb") as f:
        ScoreMatrix = pickle.load(f)


def get_all_recommended_clips(user_id):
    """
    Recommends the full set of clips for a user present at the time
    the model was trained.

    params:
        user_id | Format: "u_{user_id}"
    """
    result_clip_to_score_mapping = {}

    # Already watched videos by the user
    # Embedded in the model while training
    lifetime_watch_history = list(set(G.neighbors(user_id)))
    lifetime_watch_history.sort(reverse=True, key=get_clip_max_score)

    for source_clip_id in lifetime_watch_history[:20]:
        related_score_matrix = ScoreMatrix[source_clip_id]
        related_clips_ids = list(related_score_matrix.keys())

        for suggested_clip_id in related_clips_ids:
            if suggested_clip_id not in result_clip_to_score_mapping:
                result_clip_to_score_mapping[suggested_clip_id] = related_score_matrix[suggested_clip_id]

            result_clip_to_score_mapping[suggested_clip_id] = max(
                result_clip_to_score_mapping[suggested_clip_id], related_score_matrix[suggested_clip_id]
            )

    for watched_clip in lifetime_watch_history:
        result_clip_to_score_mapping[watched_clip] = -1

    if "Maxscore" in result_clip_to_score_mapping:
        del result_clip_to_score_mapping["Maxscore"]

    results = list(result_clip_to_score_mapping.keys())

    def get_result_mapping_scores(clip_uid):
        return result_clip_to_score_mapping[clip_uid]

    results.sort(reverse=True, key=get_result_mapping_scores)
    results = results[:1000]

    final_clips_scores = {}
    for clip_uid in results:
        final_clips_scores[clip_uid] = result_clip_to_score_mapping[clip_uid]

    return final_clips_scores
