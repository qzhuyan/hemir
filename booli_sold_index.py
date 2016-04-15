#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from urllib import unquote
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(host='192.168.0.33',port=9200)
import os.path, time
import json
import inspect

def has_data_property(tag):
    return tag.has_attr('data-property')

class BooliSoldIndexPage(BeautifulSoup):
    @staticmethod
    def from_file(filepath):
        data = open(filepath).read()
        obj = BooliSoldIndexPage(data, 'html.parser')
        obj.file_mtime = time.ctime(os.path.getmtime(filepath))
        return  obj


    def get_data_property(self):
        ress = self.find_all(has_data_property)
        return  ress


    def get_hem_prop(self):
        res = []
        for p in self.get_data_property():
            attrs = p.a.attrs
            res.append(to_doc(attrs))
        return res

    def send_to_elk(self):
        docs = self.get_hem_prop()
        for doc in docs:
            doc['timestamp'] = datetime.now(),
            res = es.index(index="test1", doc_type='booli_sold', id=doc[u'id'], body=doc)
        return res

def to_doc(attrs):
    meta = json.loads(attrs[u'data-meta'])
    flatten_attrs = dict(attrs)
    flatten_attrs.update(meta)
    for k,v in flatten_attrs.iteritems():
        if type(flatten_attrs[k]) is dict and 'value' in flatten_attrs[k].keys():
            flatten_attrs[k] = flatten_attrs[k]['value']
            
        if type(flatten_attrs[k]) is unicode:
            flatten_attrs[k] = flatten_attrs[k].replace(u"\u00BD",u'5')

        if (k in [u'soldPrice', u'soldSqmPrice', u'soldPriceAbsoluteDiff']):
            try:
                flatten_attrs[k] = int(flatten_attrs[k].replace(u' ',u''))
            except:
                flatten_attrs[k] = -1

    if not flatten_attrs[u'floor']:
        flatten_attrs[u'floor'] = -1

    flatten_attrs[u'soldDate'] = format_date(flatten_attrs[u'soldDate'])
    
    return flatten_attrs


def main(f):
    print "handling file %s" % (f)
    soup = BooliSoldIndexPage.from_file(f)
    soup.send_to_elk()

def format_date(s):
    month_d = {
        u'jan' : '01',
        u'feb' : '02',
        u'mar' : '03',
        u'apr' : '04',
        u'maj' : '05',
        u'jun' : '06',
        u'jul' : '07',
        u'aug' : '08',
        u'sep' : '09',
        u'okt' : '10',        
        u'nov' : '11',
        u'dec' : '12',
    }
    d = s.split(' ');
    if len(d[0]) == 1:
        day = '0'+ d[0]
    else:
        day = d[0]
    month = month_d[d[1]]
    year = d[2]
    res = '%s-%s-%s' % (year,month,day)
    return res

    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process hemnet pages.')
    parser.add_argument('-f', dest='file',
                        help='file to read')
    args = parser.parse_args()
    main(args.file)

