#!/bin/bash -x

count=$1
homes=`casperjs ./hemmirror.js`

casperjs ./scrap_hemurl.js --data="./1.data" 

