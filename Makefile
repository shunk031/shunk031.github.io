HUGO_VERSION := 0.136.5
HUGO_CMD := docker run --rm -v $(PWD):/project -v $(HOME)/Library/Caches/hugo_cache:/cache -p 1313:1313 ghcr.io/gohugoio/hugo:v$(HUGO_VERSION)

.PHONY : help
help :
	$(HUGO_CMD) help

.PHONY : update
update :
	$(HUGO_CMD) mod get -u

.PHONY : build
build :
	$(HUGO_CMD) build

.PHONY : server
server :
	$(HUGO_CMD) server --bind=0.0.0.0

.PHONY : run
run : update server

.PHONY: check-broken-links
check-broken-links: build
	lychee public --config .lychee/config.toml

.PHONY : post
post:
ifeq ($(name),)
	$(error name for the post is not set: make post name=YOUR-POST-NAME)
endif
	$(HUGO_CMD) new --kind post post/$(name)

.PHONY : news
news:
ifeq ($(name),)
	$(error name for the news is not set: make news name=YOUR-NEWS-NAME)
endif
	$(HUGO_CMD) new --kind post news/$(name)

.PHONY : publication
publication:
ifeq ($(name),)
	$(error name for the publication is not set: make publication name=AUTHOR-YEAR-TITLE)
endif
	$(HUGO_CMD) new --kind publication publication/$(name)

.PHONY : event
event:
ifeq ($(name),)
	$(error name for the event is not set: make event name=EVENT-TALK-NAME)
endif
	$(HUGO_CMD) new --kind event event/$(name)

.PHONY : ogp-image
ogp-image:
ifeq ($(name),)
	$(error name for the OGP image is not set: make ogp-image name=PUBLICATION-NAME)
endif
	./scripts/generate_ogp_image_for_publication.sh $(name)
