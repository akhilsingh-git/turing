FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install pipenv and compilation dependencies
RUN apt-get update
RUN pip install pipenv

# Install python dependencies in /.venv
COPY requirements.txt .
RUN pipenv install -r requirements.txt
RUN pipenv install --system --skip-lock

ENV CLIENT_ID dummy_client_id
ENV CLIENT_SECRET dummy_client_secret

EXPOSE 80

RUN useradd --create-home --shell /bin/bash loco
USER loco
WORKDIR /home/loco/turing

COPY . .
CMD flask run --host 0.0.0.0 --port 80
