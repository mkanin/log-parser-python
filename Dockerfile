FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
COPY . /code

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt && alembic upgrade head

ENTRYPOINT ["/code/entrypoint.sh"]