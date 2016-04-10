#!/usr/bin/python
import os
import sys
import argparse
from hempage import HemnetPage
# forward hemnet page to elk

parser = argparse.ArgumentParser(description='Process hemnet pages.')
parser.add_argument('-s', dest='source_dir',
                   help='root dir of hemnet pages')

args = parser.parse_args()

print "source dir is %s" % (args.source_dir)

f = os.popen("""find %s -name '*index.html' """%(args.source_dir))

htmls = f.read().split('\n')

for h in htmls:
    print "processing " + h
    HemnetPage.from_file(h).send_to_elk()
    
