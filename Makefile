.PHONY : update
update :
	./update_wowchemy.sh

.PHONY : server
server :
	hugo mod clean
	hugo server --disableFastRender --i18n-warnings

.PHONY : run
run :
	make update
	make server
