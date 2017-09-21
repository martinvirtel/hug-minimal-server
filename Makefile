SHELL := /bin/bash

dev-server:
	hug -f server.py


WORKERS = 5

dev-server-gunicorn:
	gunicorn  --workers $(WORKERS) server:__hug_wsgi__

