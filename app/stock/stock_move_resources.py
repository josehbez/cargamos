# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
from flask_restful import reqparse
from app.stock.models import StockMove as StockMoveModel, \
    next_move, stock_product_warehouse
from app.product.models import Product as ProductModel
from app.warehouse.models import Warehouse as WarehouseModel
from app import db
from app.commun import rp, BaseResource, is_int

def stock_move_reqparse():
    post_parse = reqparse.RequestParser()
    post_parse.add_argument('qty', type=int, dest='qty', required=True, 
        help="The quantity")
    post_parse.add_argument('product_id', type=int, dest='product_id', required=True, 
        help="The product id")
    post_parse.add_argument('warehouse_id', type=int, dest='warehouse_id', required=True, 
        help="The warehouse id")
    return post_parse.parse_args()

def stock_move_transfer(ttype):
    args = stock_move_reqparse()
    if args.qty <= 0:
        return rp(message="Quantity must be an integer and greater to zero"), 404
    if args.product_id <= 0:
        return rp(message="Product ID must be an integer. Check /VERSION/product"), 404
    if args.warehouse_id <= 0:
        return rp(message="Warehouse ID must be an integer. Check /VERSION/warehouse"), 404

    product_id = ProductModel.by(id=args.product_id)
    warehouse_id = WarehouseModel.by(id=args.warehouse_id)

    if ttype == 'sale':
        stock = stock_product_warehouse(
            product_id=product_id.id,
            warehouse_id=warehouse_id.id)
        if isinstance(stock, Exception):
            return rp(message=str(stock)), 400
        product_stock = stock[0].get('qty')
        if int(args.qty) > product_stock:
            return rp(
                message="The product %s only has %s stock" % (product_id.id, product_stock),
                ), 400
        type_move = 'out'
    else: # defautl is purchase
        type_move = 'in'

    name = next_move(ttype)

    stock_move = StockMoveModel(name, type_move, args.qty,
        product_id=product_id.id, warehouse_id=warehouse_id.id)
        
    err =stock_move.save()

    if err != None:
        return rp(message=str(err)), 500
    
    return rp(success=True, payload=stock_move.serialize()), 201



class Sale(BaseResource):

    def post(self):
        return stock_move_transfer('sale')

class Purchase(BaseResource):

    def post(self):
        return stock_move_transfer('purchase')

