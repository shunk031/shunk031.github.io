export HUGO_SERVER_PORT=1313

export MUFFET_TIMEOUT=20
export MUFFET_MAX_CONNECTIONS=10

.PHONY : update
update :
	./update_wowchemy.sh

.PHONY : server
server :
	hugo mod clean
	hugo server --port $(HUGO_SERVER_PORT)

.PHONY : test
test :
	muffet http://localhost:$(HUGO_SERVER_PORT) \
		-t $(MUFFET_TIMEOUT) \
		-c $(MUFFET_MAX_CONNECTIONS) \
		-e linkedin.com \
		-e twitter.com \
		-e facebook.com  \
		-e gstatic.com \
		-e researchgate.net \
		-e arxiv.org \
		-e valuenex.com  \
		-e paper-survey \
		-e "publication/#\d"

.PHONY : run
run :
	make update
	make server
