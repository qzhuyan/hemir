#!/usr/bin/python
import unittest
import inspect
from booli_sold_index import BooliSoldIndexPage
from booli_sold_index import to_doc
class TestBooliSoldIndexPage(unittest.TestCase):
    def test_get_list(self):
        soup = BooliSoldIndexPage.from_file('test2.html')
        res =  soup.get_data_property()
        self.assertEqual(len(res), 35) 

    # def test_get_hem_prop(self):
    #     soup = BooliSoldIndexPage.from_file('test2.html')
    #     res =  soup.get_hem_prop()
    #     self.assertEqual(len(res), 35)

    def test_send_to_elk(self):
        soup = BooliSoldIndexPage.from_file('test2.html')
        soup.send_to_elk()
        #res =  soup.get_hem_prop()
         
    def test_json_flatten(self):
        data = {u'target': u'_blank', u'data-open-modal': u'/annons/2062587', u'id': u'id_2062587', u'href': u'https://www.booli.se/annons/2062587', u'data-type': u'sold', u'class': [u'hit__anchor', u'js__hit__anchor'], u'data-meta': u'{"primaryArea":{"name":"Huvudsta"},"floor":{"value":7,"unit":" tr"},"id":2062587,"booliId":2062587,"latitude":59.3496497,"livingArea":{"value":"81.6","unit":" m\xb2"},"longitude":17.9940791,"objectType":"L\\u00e4genhet","primaryImage":{"url":"","isStreetview":false,"fromAgency":false,"isMissing":true},"rooms":{"value":3,"unit":" rum"},"soldDate":{"value":"6 apr 2016","unit":""},"soldPrice":{"value":"3 610 000","unit":" kr"},"soldSqmPrice":{"value":"44 240","unit":" kr\\/m\xb2"},"soldPriceAbsoluteDiff":{"value":"415 000","unit":" kr"},"soldPricePercentageDiff":{"value":"+13,0","unit":"%"},"soldPriceTrend":{"value":"positive","unit":false},"isVerified":false,"isNewConstruction":false,"isMatchedWithListing":true,"streetAddress":"Krysshammarv\\u00e4gen 18","url":"\\/annons\\/2062587","compositions":{"rooms-livingArea-floor":"3  rum, 81.6  m\xb2, 7  tr"}}'}
        
        flatten = to_doc(data)
        self.assertEqual(flatten, 35)         


        
