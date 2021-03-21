# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors

from app import db, commun

class Product(commun.BaseModel):
    
    __tablename__ = "product"

    sku = db.Column(db.String(250), nullable=False, unique=True)
    
    def __init__(self, name, sku):
        self.name = name
        self.sku = sku

    def serialize(self):

        return {
            'id': self.id, 
            'name': self.name,
            'sku': self.sku,
        }

    @staticmethod
    def by(**kwargs):
        return Product.query.filter_by(**kwargs).first_or_404(description='Record with {} is not available'.format(str(kwargs)))
    
    @staticmethod
    def all():
        return Product.query.all()