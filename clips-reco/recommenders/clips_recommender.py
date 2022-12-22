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


def init_clips_models():
    global G
    global ScoreMatrix

    models_dir = os.path.join(os.getcwd(), "recommenders", "models")

    with open(os.path.join(models_dir, "network_all.sav"), "rb") as f:
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
    result_clip_to_score_maping = {}

    # Already watched videos by the user
    # Embedded in the model while training
    lifetime_watch_history = list(set(G.neighbors(user_id)))

    # Todo: Might need to shift to top 100 only
    for source_clip_id in lifetime_watch_history:
        related_score_matrix = ScoreMatrix[source_clip_id]
        related_clips_ids = list(related_score_matrix.keys())

        for suggested_clip_id in related_clips_ids:
            if suggested_clip_id not in result_clip_to_score_maping:
                result_clip_to_score_maping[suggested_clip_id] = related_score_matrix[suggested_clip_id]

            result_clip_to_score_maping[suggested_clip_id] = max(
                result_clip_to_score_maping[suggested_clip_id], related_score_matrix[suggested_clip_id]
            )

    for watched_clip in lifetime_watch_history:
        result_clip_to_score_maping[watched_clip] = -1

    if "Maxscore" in result_clip_to_score_maping:
        del result_clip_to_score_maping["Maxscore"]

    return result_clip_to_score_maping
