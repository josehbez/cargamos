# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
from typing import Any
from flask_restful import Resource
from . import db

def rp(success=False, message=None, payload=None):
    """
        rp (aka, response payload) return standard payload
    """
    return{
        'success': success,
        'message': message, 
        'payload': payload,
    }

    
class BaseResource(Resource):

    def reqparse(self) -> Any: 
        raise NotImplementedError


class BaseModel(db.Model):

    __abstract__ = True   
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                            onupdate=db.func.current_timestamp())

    def __repr__(self) -> str:
        return '<%s %s> %s' % (self.__class__.__name__, self.id, self.name)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            return e
        return None

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            return e
        return None
        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            return e
        return None
    
    def serialize(self):
        raise NotImplementedError

    @staticmethod
    def by(**kwargs):
        raise NotImplementedError

    @staticmethod
    def all():
        raise NotImplementedError