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
		pytest
		deactivate
	;;
	publish)
		func azure functionapp publish mikesfunc1
		deactivate
	;;
	*)
		echo "Usage: $0 {start|edit|publish|new|test|docs}"
		exit 1
	;;
esac

exit 0
