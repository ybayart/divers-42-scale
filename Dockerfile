FROM python:3.8.5-alpine

MAINTAINER YanYan, yanyan@hexanyn.fr

WORKDIR /data

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY scale.py utils.py ./

CMD python3 scale.py
