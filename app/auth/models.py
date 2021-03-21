# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors

from app import db, commun

class User(commun.BaseModel):
    
    __tablename__ = "users"

    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    token = db.Column(db.String(250), nullable=True)
    
    def __init__(self, name, email, password) -> None:
        self.name = name
        self.email = email
        self.password = password

    def serialize(self):
        return {
            'name':self.name,
            'email':self.email, 
            'token':self.token,
        }

    @staticmethod
    def by(**kwargs):
        return User.query.filter_by(**kwargs).first_or_404(description='Record with %s is not available'.format(str(kwargs)))