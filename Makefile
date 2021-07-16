REGISTRY   		:= registry.gitlab.com/hoovada/hoovada-auth-service
REPO_NAME   	:= $$(/usr/bin/basename -s .git `git config --get remote.origin.url`)
GIT_COMMIT 		:= $$(git rev-parse --short HEAD)
GIT_BRANCH 		:= $$(git branch | grep \* | cut -d ' ' -f2)
DATE 			:= $$(date +'%d%b%Y')

AUTH   			:= ${REGISTRY}:auth-service-${GIT_COMMIT}-${GIT_BRANCH}-${DATE}

auth-service:
	@docker build -t ${AUTH} -f ./docker/app/Dockerfile .
	@docker push ${AUTH}

deploy-staging:
	@kubectl set image deployment/app app=${AUTH} -n auth-service --context=do-sgp1-test --record

all-staging: auth-service deploy-staging

deploy-live:
	@kubectl set image deployment/app app=${AUTH} -n auth-service --context=do-sgp1-production --record

all-live: auth-service deploy-live

login:
	@docker login registry.gitlab.com