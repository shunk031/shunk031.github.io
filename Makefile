.PHONY : update
update :
	./update_wowchemy.sh

.PHONY : server
server :
	hugo mod clean
	hugo server

.PHONY : run
run : update server
