#!/bin/bash -x

count=$1
homes=(`casperjs ./hemmirror.js`)
num=${#homes[@]}
echo "found $num homes";
let half=$num/2


echo 'now split array'
firsthalf=( "${homes[@]:1:$half}" )
sechalf=( "${homes[@]:$half:$num}" )

echo "process 1 would handle ${#firsthalf[@]}"
echo "process 2 would handle ${#sechalf[@]}"

part1="${firsthalf[@]}"
part2="${sechalf[@]}"

casperjs ./scrap_hemurl.js --hems="$part1" & 
pid_part1=$!
casperjs ./scrap_hemurl.js --hems="$part2" & 
pid_part2=$!

wait $pid_part1
wait $pid_part2
