# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
from app.stock.models import stock_all, stock_product_warehouse,\
    stock_product, stock_warehouse
from app.commun import rp, BaseResource, is_int

class Stock(BaseResource):

    def get(self, product_id:int=0, warehouse_id:int=0):
        
        if product_id>0 and warehouse_id>0:
            rows = stock_product_warehouse(product_id, warehouse_id)
        else:
            rows = stock_all()
        
        if isinstance(rows, Exception):
            return rp(message=str(rows)), 404

        return rp(success=True,payload=rows), 200


class StockProduct(BaseResource):

    def get(self, product_id:int=0):
        
        if product_id>0:
            rows = stock_product(product_id)
        else:
            return rp(message="The product ID must be an integer and greate zero"), 404
        
        if isinstance(rows, Exception):
            return rp(message=str(rows)), 404

        return rp(success=True,payload=rows), 200

class StockWarehouse(BaseResource):

    def get(self, warehouse_id:int=0):
        
        if warehouse_id>0:
            rows = stock_warehouse(warehouse_id)
        else:
            return rp(message="The warehouse ID must be an integer and greate zero"), 404
        
        if isinstance(rows, Exception):
            return rp(message=str(rows)), 404

        return rp(success=True,payload=rows), 200