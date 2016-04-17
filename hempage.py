#!/usr/bin/python
from bs4 import BeautifulSoup
import re
from urllib import unquote
from datetime import datetime
from datetime import timedelta
from elasticsearch import Elasticsearch
es = Elasticsearch(host='127.0.0.1',port=9200)
import os.path, time
import json

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[str(name[:-1])] = x
                

    flatten(y)
    return out

def days_passed(day1,day2):
    day2 = time.strptime(day2.split('T')[0], "%Y-%m-%d")
    return round((day1 - time.mktime(day2))/86400)

class HemnetPage(BeautifulSoup):
    """ translate hemnet html page data to json """
    file_mtime = None

    def get_hem_prop(self):
        try:
            ret = self.find_all(class_='property__attributes')
            keys = map(lambda x: x.string, ret[0].find_all('dt'))
            values =  map(lambda x: x.string, ret[0].find_all('dd'))
            return dict(zip(keys,values))
        except:
            return None

    def get_broker_prop(self):
        try:
            brokerprop = dict()
            #todo: maybe we can narrow to class broker fist 
            ret = self.find(class_='broker')
            brokerprop['name'] = ret.p.b.string
            brokerprop['link'] = ret.find(class_='broker-link').get_text().strip()
            brokerprop['phone'] = ret.find(class_='phone-number').get_text().strip()
            ret = ret.find(class_='broker__email')
            brokerprop['email'] = unquote(ret['href'])

            ret = self.find_all(class_='broker-link')

            return brokerprop
        except:
            return None


    def get_property_stats(self):
        try:
            visits = self.find(class_ = 'property-stats__visits').string.replace(u'\xa0', '')
            spans =  self.find(class_ = 'property-stats__container').find_all('span')
            for s in spans:
                if s.has_attr(u'datetime'):
                    start_date = s[u'datetime']
            return dict(visits=int(visits), start_date=start_date)
        except:
            return None
        

    def get_property_address(self):
        try:
            location = self.find(class_='property-location text--subtle').get_text().split('\n')
            com = location[2].strip()
            addr = location[1].strip()
            return addr+com
        except:
            return None
        
    def get_datalayer(self):
        # return self.find(rel='canonical')['href'].split('-')[-1]
#          dataLayer = [{"taxonomy":{"Sajt":"hemnet-se","Sektion":"objektsida"}},{"page":{"type":"standard"}},{"property":{"id":8680875,"broker_firm":"One Fastighetsm\u00e4kleri AB","foreign":false,"location":"Solna","locations":{"country":"Sverige","region":"Stockholms l\u00e4n","municipality":"Solna kommun","postal_city":"Solna","district":"R\u00e5sunda","street":"Vinterv\u00e4gen","city":"Stockholm"},"images_count":23,"new_production":false,"home_swapping":false,"offers_selling_price":true,"status":"for_sale","item_type":"Bostadsr\u00e4ttsl\u00e4genhet","main_location":"Solna","street_address":"Vinterv\u00e4gen 26, v\u00e5n 4","rooms":2.0,"living_area":45.0,"price_per_m2":64333,"price":2895000,"has_price_change":false,"borattavgift":2432,"upcoming_open_houses":true}}];
        try:
            datalayer = self.body.script.string.split('\n')[1].split('=')[1].strip().rstrip(';')
            return json.loads(datalayer)
        except:
            return None
        
    # hope it is uid
    def get_id(self):
        try:
            res = self.get_datalayer()
            return res[2][u'property'][u'id']
        except:
            return None
    
    def to_doc(self):
        z = { 'id': self.get_id(),
                 'timestamp': datetime.now(),
                 'stats':   self.get_property_stats(),
                 'broker':  self.get_broker_prop(),
            }
        try:
            z.update(self.get_datalayer()[2][u'property'])
        except:
            print "error: cannot update with property"
        return flatten_json(z)

    def send_to_elk(self, index = 'hemmirv1', doc_type='hemnet'):
        doc = self.to_doc()
        doc['file_mtime'] = time.ctime(self.file_mtime)
        if  'stats_start_date' in doc:
            doc['daysOnHemnet'] = days_passed(self.file_mtime, doc['stats_start_date'])
        res = es.index(index=index, doc_type=doc_type, id=doc['id'], body=doc)
        return res

    
    @staticmethod
    def from_file(filepath):
        data = open(filepath).read()
        obj = HemnetPage(data, 'html.parser')
        obj.file_mtime = os.path.getmtime(filepath)
        return  obj

        
