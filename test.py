# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
import unittest
import pdb
from app import app, commun, db
import random

class AppTestCase(unittest.TestCase):

    randid = lambda self: str(random.randint(1, 10000000))  
    headers= {}
    

    def setUp(self) -> None:
        self.app = app
        self.client = self.app.test_client                
        self.product_id = 0
        self.warehouse_id= 0
        db.create_all()
        

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
        
        self.headers.update({'Authorization':'Bearer '+ res.json.get('payload').get('token')})
        

    def test_warehouse(self):
        if self.warehouse_id != 0:
            return 
        id = self.randid()
        data = {
            'name': "WH/%s" % id,
            'address': "Address %s" % id
        }
        
        res = self.client().post('/v1/warehouse', data=data, headers=self.headers)
        self.assertEqual(res.status_code, 201, res.data)

        data = res.json.get('payload')
        
        self.warehouse_id = data.get('id')

        res = self.client().get('/v1/warehouse', headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)
        
        res = self.client().get('/v1/warehouse/%s' % data.get('id'), headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)

        data.update({'name': "%s Update" % data.get('name')})
        res = self.client().put('/v1/warehouse/%s' % data.get('id'), data=data,headers=self.headers)
        self.assertEqual(res.status_code, 201, res.data)

        #res = self.client().delete('/v1/warehouse/%s' % data.get('id'), headers=self.headers)
        #self.assertEqual(res.status_code, 204, res.data)

    def test_product(self):
        if self.product_id != 0:
            return 
        id = self.randid()
        data = {
            'name': "Name %s" % id,
            'sku': "SKU%s" % id
        }
        res = self.client().post('/v1/product', data=data, headers=self.headers)
        self.assertEqual(res.status_code, 201, res.data)
        data = res.json.get('payload')
        
        self.product_id = data.get('id')

        res = self.client().post('/v1/product', data=data, headers=self.headers)
        self.assertEqual(res.status_code, 500, res.data)
        
        res = self.client().get('/v1/product', headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)

        res = self.client().get('/v1/product/%s' % data.get('id'), headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)

        res = self.client().get('/v1/product/%s' % data.get('sku'), headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)

        data.update({'name': "%s Update" % data.get('name')})
        res = self.client().put('/v1/product/%s' % data.get('id'), data=data,headers=self.headers)
        self.assertEqual(res.status_code, 201, res.data)
        
        #res = self.client().delete('/v1/product/%s' % data.get('id'), headers=self.headers)
        #self.assertEqual(res.status_code, 204, res.data)

    def req_wp(self):
        self.test_product()
        self.test_warehouse()

    def test_purchase(self):
        self.req_wp()
        data = {
            'qty': 100, 
            'product_id': self.product_id, 
            'warehouse_id': self.warehouse_id, 
        }
        res = self.client().post('/v1/purchase', data=data, headers=self.headers)
        self.assertEqual(res.status_code, 201, res.data)


    def test_stock(self):        
        self.test_sale()
        res = self.client().get('/v1/stock', headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)
        
        res = self.client().get('/v1/stock/%s/%s'%(self.product_id, self.warehouse_id), headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)
        
        res = self.client().get('/v1/stock/product/%s'% self.product_id, headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)
        
        res = self.client().get('/v1/stock/warehouse/%s'% self.warehouse_id, headers=self.headers)
        self.assertEqual(res.status_code, 200, res.data)

    def test_sale(self):
        self.test_purchase()
        data = {
            'qty': 23, 
            'product_id': self.product_id, 
            'warehouse_id': self.warehouse_id, 
        }
        res = self.client().post('/v1/sale', data=data, headers=self.headers)        
        self.assertEqual(res.status_code, 201, res.data)

if __name__ == '__main__':
    unittest.main()
