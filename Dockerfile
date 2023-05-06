# syntax=docker/dockerfile:1
FROM python:3.10.11-alpine3.16
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "flask", "--app", "src/main.py", "run", "--host=0.0.0.0"]