# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
from flask_restful import reqparse
from app.product.models import Product as ProductModel
from app.commun import rp, BaseResource, is_int

class Product(BaseResource):

    def reqparse(self):
        post_parse = reqparse.RequestParser()
        post_parse.add_argument('name', dest='name', required=True, 
            help="The product's name")
        post_parse.add_argument('sku', dest='sku', required=True, 
            help="The product's sku")

        return post_parse.parse_args()

    def get(self, id=None):
        if id is not None:
            if is_int(id):
                rows = ProductModel.by(id=int(id)).serialize()
            else: 
                rows = ProductModel.by(sku=id).serialize()
        else: 
            rows = [ a.serialize() for a in ProductModel.all()]
        return rp(success=True, payload=rows)


    def post(self):
        args = self.reqparse()
        row = ProductModel(args.name, args.sku)
        err = row.save()
        if err != None:
            res = rp(message=str(err)), 500
        else: 
            res = rp(success=True, payload=row.serialize()), 201
        return res 
    
    def put(self, id):
        args = self.reqparse()
        if not is_int(id ):
            return rp(message="The ID must be an integer"), 404

        row = ProductModel.by(id=int(id))
        row.name= args.name
        row.sku= args.sku
        err = row.update()
        if err != None:
            res = rp(message=str(err)), 500
        else: 
            res = rp(success=True, payload=row.serialize()), 201
        return res

    def delete(self, id):
        if not is_int(id ):
            return rp(message="The ID must be an integer"), 404
        row = ProductModel.by(id=int(id))
        err = row.delete()
        if err != None:
            res = rp(message=str(err)), 500
        else: 
            res = rp(success=True, payload=row.serialize()), 204
        return res