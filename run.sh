#!/bin/bash
python ./sinanews/server.py 1>>/var/log/news/normal.log 2>&1 &
