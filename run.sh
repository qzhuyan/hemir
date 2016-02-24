#!/bin/bash -ex
homes=$(casperjs ./hemmirror.js)

num=$(echo $homes | wc -l );

echo "found $num homes";

for h in $homes;
do
    res=$(casperjs ./h2b.js --url=$h);
    url=$(echo $res |  awk -F '|' '{print $3}')
    echo "broker url is $url"
    casperjs ./broker.js --url=$url
done

