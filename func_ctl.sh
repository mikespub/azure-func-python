#!/bin/bash
#python3 -m venv venv
source venv/bin/activate
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
	list)
		func azure functionapp list-functions mikesfunc1 --show-keys
	;;
	docs)
		cd ..
		wget https://github.com/Azure/azure-functions-python-worker/raw/dev/README.md -O README.in
		echo "Source: [Azure/azure-functions-python-worker](https://github.com/Azure/azure-functions-python-worker)" > README.md
		echo >> README.md
		cat README.in >> README.md
		rm README.in
		wget https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/azure-functions/create-first-function-cli-python.md -O create-first-function-cli-python.in
		echo "Source: [MicrosoftDocs/azure-docs](https://github.com/MicrosoftDocs/azure-docs/tree/master/articles/azure-functions)" > create-first-function-cli-python.md
		echo >> create-first-function-cli-python.md
		cat create-first-function-cli-python.in >> create-first-function-cli-python.md
		rm create-first-function-cli-python.in

	;;
	test)
		# update http test with context from azure functions python library
		#wget https://github.com/Azure/azure-functions-python-library/raw/dev/tests/test_http_wsgi.py -O HttpTrigger/test_http_wsgi.py
		python -m pytest
		deactivate
	;;
	publish)
		func azure functionapp publish mikesfunc1
		deactivate
	;;
	*)
		echo "Usage: $0 {start|edit|publish|new|test|docs|list}"
		exit 1
	;;
esac

exit 0
