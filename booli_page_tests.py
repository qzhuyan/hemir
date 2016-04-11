#!/usr/bin/python
import unittest
import inspect
from booli_sold_index import BooliSoldIndexPage

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
         
       
        
