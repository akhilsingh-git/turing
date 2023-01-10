import os

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "app.log")

VIDEO_SCORE_MATRIX_MODEL_DATE = os.environ["video_score_matrix_model_date"]
VIDEO_SCORE_MATRIX_MODEL_TYPE = os.environ["video_score_matrix_model_type"]
VIDEO_SCORE_MATRIX_MODEL_ARCH = os.environ["video_score_matrix_model_arch"]
VIDEO_SCORE_MATRIX_MODEL_ARCHIVE_NAME = os.environ["video_score_matrix_model_archive_name"]
VIDEO_SCORE_MATRIX_MODEL_CONTENT = os.environ["video_score_matrix_model_content"]

WATCH_HISTORY_GRAPH_MODEL_DATE = os.environ["watch_history_graph_model_date"]
WATCH_HISTORY_GRAPH_MODEL_TYPE = os.environ["watch_history_graph_model_type"]
WATCH_HISTORY_GRAPH_MODEL_ARCH = os.environ["watch_history_graph_model_arch"]
WATCH_HISTORY_GRAPH_MODEL_ARCHIVE_NAME = os.environ["watch_history_graph_model_archive_name"]
WATCH_HISTORY_GRAPH_MODEL_CONTENT = os.environ["watch_history_graph_model_content"]

MODELS_METADATA_RESPONSE = {
    "video_score_matrix": {
        "name": "video_score_matrix",
        "date": VIDEO_SCORE_MATRIX_MODEL_DATE,
        "type": VIDEO_SCORE_MATRIX_MODEL_TYPE,
        "arch": VIDEO_SCORE_MATRIX_MODEL_ARCH,
        "archive_name": VIDEO_SCORE_MATRIX_MODEL_ARCHIVE_NAME,
        "content": VIDEO_SCORE_MATRIX_MODEL_CONTENT,
    },
    "watch_history_graph": {
        "name": "watch_history_graph",
        "date": WATCH_HISTORY_GRAPH_MODEL_DATE,
        "type": WATCH_HISTORY_GRAPH_MODEL_TYPE,
        "arch": WATCH_HISTORY_GRAPH_MODEL_ARCH,
        "archive_name": WATCH_HISTORY_GRAPH_MODEL_ARCHIVE_NAME,
        "content": WATCH_HISTORY_GRAPH_MODEL_CONTENT,
    },
}
