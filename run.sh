#!/bin/bash -ex
homes=$(casperjs ./hemmirror.js)

num=$(echo $homes | wc -l );

echo 'found $num homes';

for h in $homes;
do
    casperjs ./h2b.js --url=$h;
done

