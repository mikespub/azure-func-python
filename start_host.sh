#!/bin/bash
#python3.6 -m venv .env
source .env/bin/activate
#func init mikesfunc1
cd mikesfunc1
#func new
func host start
#...
#func azure functionapp publish mikesfunc1
deactivate
