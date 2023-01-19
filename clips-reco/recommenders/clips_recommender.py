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
allVideoIdList = None


def get_clip_max_score(clip_uid):
    return ScoreMatrix[clip_uid]["information"]["Maxscore"]

def initialiseCatgoryCount():
    """
    initialises count for cateories for new users,
    please add new category here.

    params:
    """
    return ({
        '1000': 0,
        '1001': 0,
        '1003': 0,
        '1004': 0,
        '1005': 0,
        '1006': 0,
        '1007': 0,
        '1008': 0,
        '1009': 0,
        '1010': 0,
        '1011': 0,
        '1012': 0,
        '1013': 0,
        '1014': 0,
        '1015': 0,
        '1016': 0,
        '1017': 0,
        '1018': 0,
        '1019': 0,
        '1020': 0,
        '1021': 0,
        '1022': 0,
        '1023': 0,
        '1024': 0,
        '117645': 0,
        '131470': 0,
        '13266': 0,
        '1386': 0,
        '20097': 0,
        '264017': 0,
        '565773': 0,
        '568925': 0,
        '571890': 0,
        '70323': 0
        
    }
    )
 

def init_clips_models():
    model_load_start_time = time.time()

    global G
    global ScoreMatrix

    models_dir = os.path.join(os.getcwd(), "recommenders", "models")

    with open(os.path.join(models_dir, "watch_history_graph.sav"), "rb") as f:
        G = pickle.load(f)

    with open(os.path.join(models_dir, "video_score_matrix.sav"), "rb") as f:
        ScoreMatrix = pickle.load(f)

    allVideoIdList = list(ScoreMatrix.keys())
    allVideoIdList.sort(reverse=True, key=get_clip_max_score)

    logging.info(msg={
        "func": "init_clips_models",
        "message": "model_load_time",
        "time_taken_ms": ((time.time() - model_load_start_time) * 1000),
    })

def get_mix_category_recommended_clips_for_new_users():
    """
    Recommends the set of clips for a new user for which model does not have any data

    params:
    """

    # Already watched videos by the user
    # Embedded in the model while training
    categories= initialiseCatgoryCount() #all category id stores total video in recommendation in each category
    results = [] #at top have freefire video
    recommeded_video = []
    countOfCompletedCategories = 0
    videoInEachCategory = 50
    for video_id in list(allVideoIdList):
        try:
            categoryOfVideo = ScoreMatrix[video_id]["information"]["Category"]
            categories[categoryOfVideo]
        except:
            continue
        if(countOfCompletedCategories >= len(categories.keys())):
            break
        if(categories[categoryOfVideo]>videoInEachCategory):
            continue
        if(categories[categoryOfVideo]==videoInEachCategory):
            countOfCompletedCategories = countOfCompletedCategories+1
        categories[categoryOfVideo] = categories[categoryOfVideo]+1
        if(categoryOfVideo == "20097" and categories[categoryOfVideo] <10):
            results.append(video_id)
            continue
        recommeded_video.append(video_id)
        
    results.extend(recommeded_video)
    
    return results

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
        
    if(formatted_user_uid == "u_-1" ):
        return(get_mix_category_recommended_clips_for_new_users())

    # Already watched videos by the user
    # Embedded in the model while training
    lifetime_watch_history = list(set(G.neighbors(formatted_user_uid)))
    lifetime_watch_history.sort(reverse=True, key=get_clip_max_score)

    for source_clip_id in lifetime_watch_history[:20]:
        related_score_matrix = ScoreMatrix[source_clip_id]['relation']
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

def get_all_recommended_clips_for_recent_view(formatted_user_uid,recent_watch_history):
    """
    todo: test it before launch  with ivory 
    Recommends the full set of clips for a user present at the time
    the model was trained based on recent watch history

    params:
        formatted_user_uid -> Format: "u_{user_id}"
        recent_watch_history -> list of video_id on january 2023 length of list is 3
    """
    result_clip_to_score_mapping = {}

    

    for source_clip_id in recent_watch_history:
        related_score_matrix = ScoreMatrix[source_clip_id]['relation']
        related_clips_ids = list(related_score_matrix.keys())

        for suggested_clip_id in related_clips_ids:
            if suggested_clip_id not in result_clip_to_score_mapping:
                result_clip_to_score_mapping[suggested_clip_id] = related_score_matrix[suggested_clip_id]

            result_clip_to_score_mapping[suggested_clip_id] = max(
                result_clip_to_score_mapping[suggested_clip_id], related_score_matrix[suggested_clip_id]
            )

    for watched_clip in recent_watch_history:
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
