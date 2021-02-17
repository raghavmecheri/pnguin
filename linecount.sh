#!/bin/bash
LINE=""
while read x ; do LINE=$x ; done;
IFS=' ' read -r -a array <<< "$LINE"

if [ "${array[3]}" -gt "1000" ]; then
	exit 1;
fi