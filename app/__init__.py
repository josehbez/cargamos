# -*- coding: utf-8 -*-
#  Copyright (c) 2021 The Project Cargamos Authors
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os

app = Flask(__name__)

# Load config
config_name = os.getenv('APP_SETTINGS', 'dev')
app.config.from_json("../deployments/%s/config.json" %  config_name)

# DB manager 
db = SQLAlchemy(app)
                                            
# API manager 
api = Api(app, prefix='/v1')

def api_load_resources():
    from app.auth.resources import Register, Login
    api.add_resource(Register, "/auth/register")
    api.add_resource(Login, "/auth/login")
    
    from app.warehouse.resources import Warehouse as RSWarehouse
    api.add_resource(RSWarehouse, "/warehouse", "/warehouse/<int:id>")
    
    from app.product.resources import Product as RSProduct
    api.add_resource(RSProduct, "/product", "/product/<string:id>")

api_load_resources()

@app.route("/")
def index():
    return render_template("index.html")


@app.before_request
def _jwt_required():
    from app.auth.resources import jwt_required
    err = jwt_required()
    if err != None:
        return err, 404

db.create_all()