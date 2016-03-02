#!/bin/bash -x

count=$1
homes=`casperjs ./hemmirror.js`

casperjs ./scrap_hemurl.js --data="./1.data" & 
pid_part1=$!
casperjs ./scrap_hemurl.js --data="./2.data" & 
pid_part2=$!

wait $pid_part1
wait $pid_part2
