# FROM alpine:3.14
#FROM python:3.8-slim
FROM ubuntu:20.04

RUN apt update -y
RUN apt-get update -y
RUN apt-get install -y python3.8
RUN apt install -y python3-pip

WORKDIR /home

COPY requirements.txt requirements.txt

COPY GUI GUI

RUN pip3 install virtualenv

RUN virtualenv ./venv

RUN /bin/bash -c "source ./venv/bin/activate"

RUN pip3 install -r requirements.txt