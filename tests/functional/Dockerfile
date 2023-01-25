FROM python:3.10.8-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add build-base

COPY requirements.txt .

RUN pip install --upgrade setuptools pip
COPY . .
RUN pip install -r requirements.txt --no-cache-dir

ENV PYTHONPATH=${PYTHONPATH}:/functional
CMD ["python", "./utils/wait_for_es.py"]
CMD ["pytest", "./src/"]
