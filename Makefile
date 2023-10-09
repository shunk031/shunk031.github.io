.PHONY : update
update :
	./update_wowchemy.sh

.PHONY : build
build :
	hugo

.PHONY : mod-clean
clean :
	hugo mod clean

.PHONY : server
server :
	hugo server

.PHONY : run
run : update mod-clean server

.PHONY : test
test : build
	./scripts/check_broken_links.sh
	