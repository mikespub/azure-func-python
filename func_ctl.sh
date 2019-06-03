#!/bin/bash
#python3.6 -m venv .env
source .env/bin/activate
#func init mikesfunc1
cd mikesfunc1

# Possible parameters
case "$1" in
	new)
		func new
		deactivate
	;;
	start)
		func host start
		deactivate
	;;
	edit)
	;;
	test)
		pytest
		deactivate
	;;
	publish)
		func azure functionapp publish mikesfunc1
		deactivate
	;;
	*)
		echo "Usage: $0 {start|edit|publish|new|test}"
		exit 1
	;;
esac

exit 0
