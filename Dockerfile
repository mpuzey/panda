FROM python:3.9-alpine
MAINTAINER Matthew Puzey "mpuzey1@outlook.com"

RUN mkdir -p   /tmdb
COPY src /panda/src
COPY main.py /panda/main.py
COPY constants.py /panda/constants.py
COPY config.py /panda/config.py
COPY requirements.txt /panda/requirements.txt

WORKDIR /panda
RUN apk add --update \
    py-pip

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "main.py"]