# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
import unittest
import pdb
from app import app
import random

headers = {}

class AppTestCase(unittest.TestCase):

    randid = lambda self: str(random.randint(1, 10000000))

    def setUp(self) -> None:
        self.app = app
        self.client = self.app.test_client        

    def test_auth(self):
        id = self.randid()
        data = {
            'name': 'Name %s' % id, 
            'email': 'e%s@d%s.com' %(id, id) ,
            'password': 'p%s' % id,
        }
        res = self.client().post('/v1/auth/register', data=data)
        self.assertEqual(res.status_code, 201, res.data)

        res = self.client().post('/v1/auth/register', data=data)
        self.assertEqual(res.status_code, 500, res.data)

        res = self.client().post('/v1/auth/login', data=data)        
        self.assertEqual(res.status_code, 201, res.data)
        
        headers.update({'Authorization':res.json.get('payload').get('token')})
        

    def test_warehouse(self):
        id = self.randid()
        data = {
            'name': "WH/%s" % id,
            'address': "Address %s" % id
        }
        res = self.client().post('/v1/warehouse', data=data, headers=headers)
        self.assertEqual(res.status_code, 201, res.data)

        data = res.json.get('payload')
        
        res = self.client().get('/v1/warehouse', headers=headers)
        self.assertEqual(res.status_code, 200, res.data)
        
        res = self.client().get('/v1/warehouse/%s' % data.get('id'), headers=headers)
        self.assertEqual(res.status_code, 200, res.data)

        data.update({'name': "%s Update" % data.get('name')})
        res = self.client().put('/v1/warehouse/%s' % data.get('id'), data=data,headers=headers)
        self.assertEqual(res.status_code, 201, res.data)

        res = self.client().delete('/v1/warehouse/%s' % data.get('id'), headers=headers)
        self.assertEqual(res.status_code, 204, res.data)

    def test_product(self):
        id = self.randid()
        data = {
            'name': "Name %s" % id,
            'sku': "SKU%s" % id
        }
        res = self.client().post('/v1/product', data=data, headers=headers)
        self.assertEqual(res.status_code, 201, res.data)
        data = res.json.get('payload')
        
        res = self.client().post('/v1/product', data=data, headers=headers)
        self.assertEqual(res.status_code, 500, res.data)
        
        res = self.client().get('/v1/product', headers=headers)
        self.assertEqual(res.status_code, 200, res.data)

        res = self.client().get('/v1/product/%s' % data.get('id'), headers=headers)
        self.assertEqual(res.status_code, 200, res.data)

        res = self.client().get('/v1/product/%s' % data.get('sku'), headers=headers)
        self.assertEqual(res.status_code, 200, res.data)

        data.update({'name': "%s Update" % data.get('name')})
        res = self.client().put('/v1/product/%s' % data.get('id'), data=data,headers=headers)
        self.assertEqual(res.status_code, 201, res.data)
        
        res = self.client().delete('/v1/product/%s' % data.get('id'), headers=headers)
        self.assertEqual(res.status_code, 204, res.data)

if __name__ == '__main__':
    unittest.main()
