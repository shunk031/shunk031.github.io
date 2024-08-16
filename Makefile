.PHONY : update
update :
	./update_wowchemy.sh

.PHONY : server
server :
	hugo mod clean
	hugo server

.PHONY : run
run : update server

.PHONY : post
post:
ifeq ($(name),)
	$(error name for the post is not set: make post name=YOUR-POST-NAME)
endif
	hugo new --kind post post/$(name)

.PHONY : news
news:
ifeq ($(name),)
	$(error name for the news is not set: make news name=YOUR-NEWS-NAME)
endif
	hugo new --kind post news/$(name)

.PHONY : publication
publication:
ifeq ($(name),)
	$(error name for the publication is not set: make publication name=AUTHOR-YEAR-TITLE)
endif
	hugo new --kind publication publication/$(name)

.PHONY : event
event:
ifeq ($(name),)
	$(error name for the event is not set: make event name=EVENT-TALK-NAME)
endif
	hugo new --kind event event/$(name)

.PHONY : ogp-image
ogp-image:
ifeq ($(name),)
	$(error name for the OGP image is not set: make ogp-image name=PUBLICATION-NAME)
endif
	./scripts/generate_ogp_image_for_publication.sh $(name)
