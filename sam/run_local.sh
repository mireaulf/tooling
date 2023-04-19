#!/bin/bash

cwd=$(pwd)
workspace=$1
function=$2

cd $1
sam build $function
sam local invoke $function --event event.json -n conf/env.json | json_pp
cd $cwd