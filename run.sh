#!/bin/bash -x

count=$1
homes=(`casperjs ./hemmirror.js`)
num=${#homes[@]}

echo "found $num homes";

i=1
for h in "${homes[@]}";
do
    if [ $i -gt $count ]; then
       exit 0;
    else
	res=$(casperjs ./h2b.js --url=$h);
	url=$(echo $res |  awk -F '|' '{print $3}')
	echo "broker url is $url"
	casperjs ./broker.js --url=$url
	let i+=1
    fi
done

