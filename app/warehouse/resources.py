# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
from flask_restful import reqparse
from app.warehouse.models import Warehouse as WarehouseModel
from app.commun import rp, BaseResource

class Warehouse(BaseResource):

    def reqparse(self):
        post_parse = reqparse.RequestParser()
        post_parse.add_argument('name', dest='name', required=True, 
            help="The warehouse's name")
        post_parse.add_argument('address', dest='address', required=True, 
            help="The warehouse's address")

        return post_parse.parse_args()

    def get(self, id:int=0):
        if id > 0:
            rows = WarehouseModel.by(id=id).serialize()
        else: 
            rows = [ a.serialize() for a in WarehouseModel.all()]
        return rp(success=True, payload=rows)


    def post(self):
        args = self.reqparse()
        row = WarehouseModel(args.name, args.address)
        err = row.save()
        if err != None:
            res = rp(message=str(err)), 500
        else: 
            res = rp(success=True, payload=row.serialize()), 201
        return res 
    
    def put(self, id:int):
        args = self.reqparse()
        row = WarehouseModel.by(id=id)
        row.name= args.name
        row.address= args.address
        err = row.update()
        if err != None:
            res = rp(message=str(err)), 500
        else: 
            res = rp(success=True, payload=row.serialize()), 201
        return res

    def delete(self, id:int):
        row = WarehouseModel.by(id=id)
        err = row.delete()
        if err != None:
            res = rp(message=str(err)), 500
        else: 
            res = rp(success=True, payload=row.serialize()), 204
        return res