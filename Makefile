SHELL := /bin/bash


deploy: docker-build-live docker-push hpa-restart


docker-build-live: 
	echo Build $$(date +%Y%m%d%H%M%S) >static/build.txt
	docker build -t nex:live .


dockerhub-login:
	$$(aws ecr get-login --region eu-central-1)


DOCKERHUB := 491576843636.dkr.ecr.eu-central-1.amazonaws.com


docker-push: 
	docker tag nex:live $(DOCKERHUB)/nex:live && \
	docker push $(DOCKERHUB)/nex:live


hpa-restart:
	hpa stop-task $$(hpa list-tasks | grep -B6 -A1 nex-live | sed -n 1p)

docker-run:
	docker run --publish 8000:8000 --name=nex_compare_server --rm nex:live


SESSION=nex-proxy

remote:
	expect -c 'spawn ssh werkzeugkasten ; send "tmux attach-session -t $(SESSION) || tmux new-session -A -c ~ -t $(SESSION)\r"; interact '
	
