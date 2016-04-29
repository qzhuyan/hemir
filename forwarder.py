#!/usr/bin/python
import os
import sys
import argparse
from hempage import HemnetPage
from booli_sold_index import BooliSoldIndexPage
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# forward hemnet page to elk

parser = argparse.ArgumentParser(description='Process hemnet pages.')
parser.add_argument('-s', dest='source_dir',
                    help='root dir of pages')
parser.add_argument('-n', dest='net',
                    default='hemnet',
                    help='hemnet or booli')
parser.add_argument('-a', dest='address',
                    default='127.0.0.1',
                    help='address of elk')

parser.add_argument('-i', dest='index',
                    default='hemmir_test',
                    help='index')

args = parser.parse_args()

print "source dir is %s" % (args.source_dir)

if args.net == 'hemnet':
    f = os.popen("""find %s -name '*index.html' """%(args.source_dir))
elif args.net == 'booli':
    f = os.popen("""find %s -name '*page=*' """%(args.source_dir))

htmls = f.read().split('\n')

es = Elasticsearch(host=args.address,port=9200)

actions = []

for h in htmls:
    if h !='':
        print "processing " + h
        if args.net == 'hemnet':
            soup = HemnetPage.from_file(h)
        elif args.net == 'booli':
            soup = BooliSoldIndexPage.from_file(h)
        res = es.index(index=args.index,
                       doc_type=args.net,
                       id=soup.get_id(),
                       body=soup.to_doc())

    
