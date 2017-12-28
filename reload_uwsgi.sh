#! /bin/bash
for i in `ps -ef | grep -v "$0" | grep uwsgi | grep -v "grep" | awk '{print $2}'`;
do
    sudo kill -9 $i
done
sleep 1

sudo uwsgi --ini uwsgi.ini
