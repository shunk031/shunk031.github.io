.PHONY : update
update :
	./update_wowchemy.sh

.PHONY : server
server :
	hugo server
