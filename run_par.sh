#!/bin/bash 
WORKERS=2
SUPER=2
homes=$(casperjs ./hemmirror.js)
#homes=$(seq 1 100)

num=${#homes[@]}

echo "found $num homes";

worker() {
    home=$1
    echo "$(date) fetch home $home"
    res=$(casperjs ./h2b.js --url=$home);
    url=$(echo $res |  awk -F '|' '{print $3}')
    echo "broker url is $url"
    timeout 10 casperjs ./broker.js --url=$url    
}

test_job() {
   sleep 5
}

bgjobs=()
for h in $homes;
do
    if [ ${#bgjobs[@]} -gt $WORKERS ];
    then
	echo 'wait... '
	wait ${bgjobs[0]}
	bgjobs=(${bgjobs[@]:1})
    else
	worker $h &
	bgjobs+=($!)
    fi
done

