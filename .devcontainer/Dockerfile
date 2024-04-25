ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

RUN apt-get update && apt-get install -y libmariadb3 libmariadb-dev gcc && \
pip install --upgrade pip

#Create virtual env and activate it
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#Install dependencies and remove the requirements file
COPY /app/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
