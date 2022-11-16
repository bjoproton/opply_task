FROM python:3.9.15-bullseye
ADD . /backend
WORKDIR /backend
RUN pip install -r requirements.txt