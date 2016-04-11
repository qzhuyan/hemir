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
             res.append(p.a.attrs)
        return res

    def send_to_elk(self):
        docs = self.get_hem_prop()
        for doc in docs:
            doc['timestamp'] = datetime.now(),
            res = es.index(index="hemmirv3", doc_type='booli_sold', id=doc[u'id'], body=doc)
        return res


def main(f):
    print "handling file %s" % (f)
    soup = BooliSoldIndexPage.from_file(f)
    soup.send_to_elk()
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process hemnet pages.')
    parser.add_argument('-f', dest='file',
                   help='file to read')
    args = parser.parse_args()
    main(args.file)

