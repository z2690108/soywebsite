#! /bin/bash
for i in `ps -ef | grep -v "$0" | grep uwsgi | grep -v "grep" | awk '{print $2}'`;
do
    kill -9 $i
done
sleep 1

uwsgi --ini uwsgi.ini
