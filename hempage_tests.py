#!/usr/bin/python
import unittest
from hempage import HemnetPage

class TestHemPage(unittest.TestCase):
    def test_get_hem_prop(self):
        expected =  {u'Antal rum': u'2 rum', u'Pris/m\xb2': u'64\xa0333 kr/m\xb2', u'Bostadstyp': u'\n      Bostadsr\xe4ttsl\xe4genhet\n    ', u'Avgift/m\xe5nad': u'2\xa0432 kr/m\xe5n', u'Bygg\xe5r': u'1931', u'Boarea': u'45 m\xb2'}
        
        htmldata = open('test.html').read()
        soup = HemnetPage(htmldata, 'html.parser')
        self.assertEqual(expected, soup.get_hem_prop())

    def test_get_broker_prop(self):
        expected = u'Jennifer Malmstr\xf6m'
        htmldata = open('test.html').read()
        soup = HemnetPage(htmldata, 'html.parser')
        brokerprop = soup.get_broker_prop()
        self.assertEqual(expected, brokerprop['broker'])
        self.assertEqual('mailto:jennifer@onemakleri.se', brokerprop['broker_email'])
        self.assertEqual( u'One Fastighetsm\xe4kleri AB', brokerprop['broker_link'])
        self.assertEqual( u'08-522 191 33', brokerprop['broker_phone'])

    def test_get_property_stats(self):
        htmldata = open('test.html').read()
        soup = HemnetPage(htmldata, 'html.parser')
        prop = soup.get_property_stats()
        self.assertEqual( 3082, prop['visits'])
        self.assertEqual(  u'2016-03-30T00:00:00+0000', prop['start_date'])

    def test_get_addr(self):
        htmldata = open('test.html').read()
        soup = HemnetPage(htmldata, 'html.parser')
        addr = soup.get_property_address()
        self.assertEqual(u'Gamla R\xe5sunda,Solna', addr)

    def test_to_doc(self):
        expected = {'id': 8680875,'hemprop': {u'Antal rum': u'2 rum', u'Pris/m\xb2': u'64\xa0333 kr/m\xb2', u'Bostadstyp': u'\n      Bostadsr\xe4ttsl\xe4genhet\n    ', u'Avgift/m\xe5nad': u'2\xa0432 kr/m\xe5n', u'Bygg\xe5r': u'1931', u'Boarea': u'45 m\xb2'}, 'stats': {'start_date': u'2016-03-30T00:00:00+0000', 'visits': 3082}, 'broker': {'broker_phone': u'08-522 191 33', 'broker': u'Jennifer Malmstr\xf6m', 'broker_email': u'mailto:jennifer@onemakleri.se', 'broker_link': u'One Fastighetsm\xe4kleri AB'}, 'address': u'Gamla R\xe5sunda,Solna', 'datalayer':u'[{"taxonomy":{"Sajt":"hemnet-se","Sektion":"objektsida"}},{"page":{"type":"standard"}},{"property":{"id":8680875,"broker_firm":"One Fastighetsm\\u00e4kleri AB","foreign":false,"location":"Solna","locations":{"country":"Sverige","region":"Stockholms l\\u00e4n","municipality":"Solna kommun","postal_city":"Solna","district":"R\\u00e5sunda","street":"Vinterv\\u00e4gen","city":"Stockholm"},"images_count":23,"new_production":false,"home_swapping":false,"offers_selling_price":true,"status":"for_sale","item_type":"Bostadsr\\u00e4ttsl\\u00e4genhet","main_location":"Solna","street_address":"Vinterv\\u00e4gen 26, v\\u00e5n 4","rooms":2.0,"living_area":45.0,"price_per_m2":64333,"price":2895000,"has_price_change":false,"borattavgift":2432,"upcoming_open_houses":true}}]'}
        htmldata = open('test.html').read()
        soup = HemnetPage(htmldata, 'html.parser')
        doc = soup.to_doc()
        # timestamp changes
        del doc['timestamp']
        self.assertEqual(expected, doc)

    def test_send_to_elk(self):
        expected = 1
        htmldata = open('test.html').read()
        soup = HemnetPage(htmldata, 'html.parser')
        res = soup.send_to_elk()
        self.assertEqual(expected, res[u'_shards'][u'successful'])        


    def test_from_file(self):
        soup = HemnetPage.from_file('test.html')
        addr = soup.get_property_address()
        self.assertEqual(u'Gamla R\xe5sunda,Solna', addr)
        self.assertTrue(soup.file_mtime != None)

    def test_get_id(self):
        soup = HemnetPage.from_file('test.html')
        self.assertEqual( 8680875, soup.get_id())

    def test_get_datalayer(self):
        expected = u'[{"taxonomy":{"Sajt":"hemnet-se","Sektion":"objektsida"}},{"page":{"type":"standard"}},{"property":{"id":8680875,"broker_firm":"One Fastighetsm\\u00e4kleri AB","foreign":false,"location":"Solna","locations":{"country":"Sverige","region":"Stockholms l\\u00e4n","municipality":"Solna kommun","postal_city":"Solna","district":"R\\u00e5sunda","street":"Vinterv\\u00e4gen","city":"Stockholm"},"images_count":23,"new_production":false,"home_swapping":false,"offers_selling_price":true,"status":"for_sale","item_type":"Bostadsr\\u00e4ttsl\\u00e4genhet","main_location":"Solna","street_address":"Vinterv\\u00e4gen 26, v\\u00e5n 4","rooms":2.0,"living_area":45.0,"price_per_m2":64333,"price":2895000,"has_price_change":false,"borattavgift":2432,"upcoming_open_houses":true}}]' 
        soup = HemnetPage.from_file('test.html')
        self.assertEqual( expected, soup.get_datalayer())
        
        
