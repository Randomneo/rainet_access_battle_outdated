FROM python:3.9

COPY requirements.txt /opt/project/requirements.txt
WORKDIR /opt/project

RUN pip install -r requirements.txt --no-cache-dir
COPY . /opt/project
