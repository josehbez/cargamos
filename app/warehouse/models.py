# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors

from app import db, commun

class Warehouse(commun.BaseModel):
    
    __tablename__ = "warehouse"

    address = db.Column(db.String(250), nullable=False)
    
    def __init__(self, name, address) -> None:
        self.name = name
        self.address = address

    def serialize(self):

        return {
            'id': self.id, 
            'name': self.name,
            'address': self.address,
        }

    @staticmethod
    def by(**kwargs):
        return Warehouse.query.filter_by(**kwargs).first_or_404(description='Record with {} is not available'.format(str(kwargs)))
    
    @staticmethod
    def all():
        return Warehouse.query.all()
    