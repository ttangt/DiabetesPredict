# FROM alpine:3.14

FROM ubuntu:20.04

RUN apt update -y
RUN apt-get update -y
RUN apt -y nano
RUN apt install -y python3-pip

WORKDIR /home

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install google-cloud-core==2.3.0

COPY GUI GUI

# COPY GUI GUI
