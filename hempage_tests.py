#!/usr/bin/python
import unittest
from hempage import HemnetPage

EXPECTED_PROPERTY =  {u'borattavgift': 2432,
                      u'broker_firm': u'One Fastighetsm\xe4kleri AB',
                      u'foreign': False,
                      u'has_price_change': False,
                      u'home_swapping': False,
                      u'id': 8680875,
                      u'images_count': 23,
                      u'item_type': u'Bostadsr\xe4ttsl\xe4genhet',
                      u'living_area': 45.0,
                      u'location': u'Solna',
                      u'locations': {u'city': u'Stockholm',
                                     u'country': u'Sverige',
                                     u'district': u'R\xe5sunda',
                                     u'municipality': u'Solna kommun',
                                     u'postal_city': u'Solna',
                                     u'region': u'Stockholms l\xe4n',
                                     u'street': u'Vinterv\xe4gen'},
                      u'main_location': u'Solna',
                      u'new_production': False,
                      u'offers_selling_price': True,
                      u'price': 2895000,
                      u'price_per_m2': 64333,
                      u'rooms': 2.0,
                      u'status': u'for_sale',
                      u'street_address': u'Vinterv\xe4gen 26, v\xe5n 4',
                      u'upcoming_open_houses': True}

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
        self.assertEqual(expected, brokerprop['name'])
        self.assertEqual('mailto:jennifer@onemakleri.se', brokerprop['email'])
        self.assertEqual( u'One Fastighetsm\xe4kleri AB', brokerprop['link'])
        self.assertEqual( u'08-522 191 33', brokerprop['phone'])

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
        self.maxDiff = None
        expected =  {'broker_name': u'Jennifer Malmstr\xf6m', 'borattavgift': 2432, 'locations_country': u'Sverige', 'living_area': 45.0, 'rooms': 2.0, 'stats_visits': 3082, 'id': 8680875, 'new_production': False, 'broker_firm': u'One Fastighetsm\xe4kleri AB', 'broker_link': u'One Fastighetsm\xe4kleri AB', 'upcoming_open_houses': True, 'broker_phone': u'08-522 191 33', 'stats_start_date': u'2016-03-30T00:00:00+0000', 'locations_city': u'Stockholm', 'location': u'Solna', 'locations_postal_city': u'Solna', 'home_swapping': False, 'has_price_change': False, 'status': u'for_sale', 'price': 2895000, 'broker_email': u'mailto:jennifer@onemakleri.se', 'main_location': u'Solna', 'offers_selling_price': True, 'locations_street': u'Vinterv\xe4gen', 'locations_region': u'Stockholms l\xe4n', 'images_count': 23, 'foreign': False, 'item_type': u'Bostadsr\xe4ttsl\xe4genhet', 'locations_municipality': u'Solna kommun', 'price_per_m2': 64333, 'locations_district': u'R\xe5sunda', 'street_address': u'Vinterv\xe4gen 26, v\xe5n 4'}
        htmldata = open('test.html').read()
        soup = HemnetPage(htmldata, 'html.parser')
        doc = soup.to_doc()
        # timestamp changes
        del doc['timestamp']
        self.assertEqual(expected, doc)

    def test_send_to_elk(self):
        expected = 1
        soup = HemnetPage.from_file('test.html')
        res = soup.send_to_elk(index = 'unittest')
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
        expected = [{u'taxonomy': {u'Sektion': u'objektsida', u'Sajt': u'hemnet-se'}}, {u'page': {u'type': u'standard'}}, {u'property': {u'status': u'for_sale', u'new_production': False, u'borattavgift': 2432, u'living_area': 45.0, u'street_address': u'Vinterv\xe4gen 26, v\xe5n 4', u'broker_firm': u'One Fastighetsm\xe4kleri AB', u'price': 2895000, u'locations': {u'city': u'Stockholm', u'postal_city': u'Solna', u'district': u'R\xe5sunda', u'country': u'Sverige', u'region': u'Stockholms l\xe4n', u'municipality': u'Solna kommun', u'street': u'Vinterv\xe4gen'}, u'images_count': 23, u'foreign': False, u'item_type': u'Bostadsr\xe4ttsl\xe4genhet', u'main_location': u'Solna', u'location': u'Solna', u'price_per_m2': 64333, u'home_swapping': False, u'has_price_change': False, u'upcoming_open_houses': True, u'id': 8680875, u'offers_selling_price': True, u'rooms': 2.0}}]
        soup = HemnetPage.from_file('test.html')
        self.assertEqual( expected, soup.get_datalayer())
        
        
