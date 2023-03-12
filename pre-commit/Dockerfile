FROM python:3.8.5-slim-buster

RUN apt-get update
RUN apt-get install -y git

RUN pip install pre-commit==2.13.0

RUN mkdir /pre-commit && cd /pre-commit
RUN git init . && pre-commit install

WORKDIR /pre-commit
