# Docker + gunicorn + hug
# inspired by https://github.com/timothycrosley/hug/blob/develop/docker/gunicorn/Dockerfile

FROM python:3.6-alpine
MAINTAINER "agaus@dpa-newslab.com"

EXPOSE 8000

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["gunicorn"]
CMD ["--reload", "--bind=0.0.0.0:8000",  "server_compare:__hug_wsgi__" ]