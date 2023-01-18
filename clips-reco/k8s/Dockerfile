FROM python:3.10-slim-bullseye

ARG aws_access_key 
ARG aws_access_secret

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install pipenv and compilation dependencies
RUN apt-get update
RUN apt-get install curl unzip -y
RUN pip install pipenv

# Install python dependencies in /.venv
COPY requirements.txt .
RUN pipenv install -r requirements.txt
RUN pipenv install --system --skip-lock
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

ENV CLIENT_ID internal_clients
ENV CLIENT_SECRET kkasdi31123jjahsdh8h103nkjaabb123jnndjas
ENV AWS_ACCESS_KEY_ID=$aws_access_key
ENV AWS_SECRET_ACCESS_KEY=$aws_access_secret
ENV LOG_FILE_PATH=/home/loco/logs/turing.log

# -------------------------------------------------------

RUN useradd --create-home --shell /bin/bash loco
USER loco

RUN mkdir -p /home/loco/logs/
RUN touch /home/loco/logs/turing.log
RUN mkdir -p /home/loco/turing/recommenders/models/
RUN mkdir -p /home/loco/turing/models_meta/

RUN aws s3 cp s3://loco-ml-models/clips_networkx_models/video_score_matrix/latest.sav /home/loco/turing/recommenders/models/video_score_matrix.sav
RUN aws s3 cp s3://loco-ml-models/clips_networkx_models/watch_history_graph/latest.sav /home/loco/turing/recommenders/models/watch_history_graph.sav

RUN aws s3api head-object --bucket "loco-ml-models" --key "clips_networkx_models/video_score_matrix/latest.sav" > /home/loco/turing/models_meta/video_score_matrix.json
RUN aws s3api head-object --bucket "loco-ml-models" --key "clips_networkx_models/watch_history_graph/latest.sav" > /home/loco/turing/models_meta/watch_history_graph.json

# For local testing
# COPY ./recommenders/models/video_score_matrix.sav /home/loco/turing/recommenders/models/video_score_matrix.sav
# COPY ./recommenders/models/watch_history_graph.sav /home/loco/turing/recommenders/models/watch_history_graph.sav

WORKDIR /home/loco/turing/

# TODO: Need to fix aws s3api command doesnt't run after COPY . .
# This is done so that models_meta does not get replaced by COPY . .
# But this makes the dockerfile fragile to new changes
COPY *.py ./
COPY ./middlewares/*.py ./middlewares/
COPY ./recommenders/*.py ./recommenders/

EXPOSE 3000
CMD flask run --host 0.0.0.0 --port 3000
