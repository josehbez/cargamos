# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
from flask import request
from app.commun import rp, BaseResource
from flask_restful import reqparse
from app.auth.models import User as UserModel
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app import app

def jwt_required():
    authorization = request.headers.get('Authorization')[7:]
    path = request.path
    exclude =[
        '/v1/auth/login',
        '/v1/auth/register',
        '/',
        '',
    ]
    if path not in exclude:
        try:
            payload = jwt.decode(authorization, app.config.get('SECRET_KEY'))
            UserModel.by(id=payload['sub'])
        except jwt.ExpiredSignatureError:
            return rp(message='Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            return rp(message='Invalid token. Please log in again.')
        except Exception as e:
            return rp(message=str(e))

    return None

def current_identity():
    authorization = request.headers.get('Authorization')[7:]
    payload = jwt.decode(authorization, app.config.get('SECRET_KEY'))
    return UserModel.by(id=payload['sub'])


class Register(BaseResource):

    def reqparse(self):
        post_parse = reqparse.RequestParser()
        post_parse.add_argument('name', dest='name', required=True, 
            help="The user's name")
        post_parse.add_argument('email', dest='email', required=True, 
            help="The user's email")
        post_parse.add_argument('password', dest='password', required=True, 
            help="The user's email")

        return post_parse.parse_args()

    def post(self):
        args = self.reqparse()
        row = UserModel(args.name, args.email, generate_password_hash(args.password))        
        err = row.save()
        if err != None:
            return rp(message=str(err)), 500
        return rp(success=True, payload=row.serialize()), 201
    
class Login(BaseResource):

    def reqparse(self):
        post_parse = reqparse.RequestParser()
        post_parse.add_argument('email', dest='email', required=True, 
            help="The user's email")
        post_parse.add_argument('password', dest='password', required=True, 
            help="The user's email")

        return post_parse.parse_args()

    def post(self):
        args = self.reqparse()
        user = UserModel.by(email=args.email)
        
        if check_password_hash(user.password, args.password):
            jwt_payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user.id
            }
            try:
                token = jwt.encode(jwt_payload, app.config.get('SECRET_KEY'), algorithm='HS256')
                user.token = token.decode()
                err = user.update()
                if err != None:
                    raise err
                resp = rp(success=True, payload=user.serialize()), 201
            except Exception as e:
                resp = rp(message=str(e)), 500            
        else:
            resp = rp(message='The passsword is incorrect'), 404

        return resp