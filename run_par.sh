#!/bin/bash 
WORKERS=${1:-2}

worker() {
    home=$1
    echo "$(date) fetch home $home"
    res=$(casperjs ./h2b.js --url=$home);
    url=$(echo $res |  awk -F '|' '{print $3}')
    if [ "null" == $url ];
    then
	echo "broker url is $url, skipp.."
    else
	echo "broker url is $url"
	timeout 60 casperjs ./broker.js --url=$url
    fi
}

test_job() {
   sleep 5 &
}

wait_for_worker()
{
    bgs=$(jobs -p |grep -v Done | wc -l)
    if [ $bgs -ge $WORKERS ];
    then
       #echo "$bgs workers in bg, wait ..."
       sleep 1;
       wait_for_worker
    else
	echo "$bgs workers in bg, conti.."
    fi
}

homes=(`casperjs ./hemmirror.js`)
num=${#homes[@]}
echo "found $num homes";

for h in "${homes[@]}";
do
    echo "handling $h"
    wait_for_worker
    worker $h &
done

