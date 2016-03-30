#!/bin/sh
myfilepath="/root/newsAPP/sinanews/"
myfile="${myfilepath}sinaspider.py"
if [ ! -x "{$myfile}" ]; then
	python $myfile
else
	exit 0
fi
