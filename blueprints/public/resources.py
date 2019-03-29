import logging, json
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from blueprints.item import *
from blueprints.users import *
from blueprints import db
from datetime import date, datetime

bp_public = Blueprint('public', __name__)
api = Api(bp_public)

class PublicResource(Resource):

    def __init__(self):
        pass
    
    def get(self,id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('nama', location='args')
            parser.add_argument('harga', location='args', type=int)
            parser.add_argument('search', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            qry = Items.query
            if args['id'] is not None:
                qry = qry.filter_by(id=args['id'])
            if args['nama'] is not None:
                # qry = qry.filter_by(nama=args['nama'])
                qry = qry.filter(Items.nama.like("%"+args['nama']+"%"))#example
            if args['harga'] is not None:
                qry = qry.filter_by(harga=args['harga'])
            if args['search'] is not None:
                qry = qry.filter(Items.nama.like("%"+args['search']+"%"))
                if qry.first() is None:
                    qry = Items.query.filter(Items.merek.like("%"+args['search']+"%"))
                    if qry.first() is None:
                        qry = Items.query.filter(Items.kategori.like("%"+args['search']+"%"))
                        if qry.first() is None:
                            qry = Items.query.filter(Items.detail.like("%"+args['search']+"%"))
                            if qry.first() is None:
                                return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }                    
            if qry.first() is None:
                return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                temp = marshal(row, Items.respon_fields)
                qry_user = Users.query.get(temp["user_id"])
                temp["merchant'""s name"] = marshal(qry_user, Users.respon_fields)["username"]
                rows.append(temp)

            return {'status': 'OK','message':'success','page':args['p'],'items':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            qry = Items.query.get(id)
            if qry is not None:
                temp = marshal(qry,Items.respon_fields)
                return temp, 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
    
    def put(self):
        return 'Not yet implement', 501


api.add_resource(PublicResource, '','/<int:id>')