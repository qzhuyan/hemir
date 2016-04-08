#!/usr/bin/python
from bs4 import BeautifulSoup
import re
from urllib import unquote
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()
import os.path, time
import json

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
            brokerprop['broker'] = ret.p.b.string
            brokerprop['broker_link'] = ret.find(class_='broker-link').get_text().strip()
            brokerprop['broker_phone'] = ret.find(class_='phone-number').get_text().strip()
            ret = ret.find(class_='broker__email')
            brokerprop['broker_email'] = unquote(ret['href'])

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
            return datalayer
        except:
            return None

        
    # hope it is uid
    def get_id(self):
        try:
            res = json.loads(self.get_datalayer())
            return res[2][u'property'][u'id']
        except:
            return None
    
    def to_doc(self):
        return { 'id': self.get_id(),
                 'timestamp': datetime.now(),
                 'address': self.get_property_address(),
                 'stats':   self.get_property_stats(),
                 'hemprop': self.get_hem_prop(),
                 'broker':  self.get_broker_prop(),
                 'datalayer': self.get_datalayer()
        }

    def send_to_elk(self):
        doc = self.to_doc()
        doc['file_mtime'] = self.file_mtime
        res = es.index(index="hemmir", doc_type='hemnet', id=doc['id'], body=doc)
        return res
    
    @staticmethod
    def from_file(filepath):
        data = open(filepath).read()
        obj = HemnetPage(data, 'html.parser')
        obj.file_mtime = time.ctime(os.path.getmtime(filepath))
        return  obj

        
