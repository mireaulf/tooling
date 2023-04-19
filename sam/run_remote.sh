#!/bin/bash

cwd=$(pwd)
workspace=$1
config=$2

cd $1
sam build -p
sam deploy --config-file ./$config --no-confirm-changeset
cd $cwd