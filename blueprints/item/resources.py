import logging, json
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from . import *
from blueprints import db
from datetime import date, datetime

bp_items = Blueprint('items', __name__)
api = Api(bp_items)

class ItemsResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self,id=None):
        status = get_jwt_claims()['status']
        if status != "merchant" and status != "admin":
            return {'message':'Only merchant or admin'},404, { 'Content-Type': 'application/json' }
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('nama', location='args')
            parser.add_argument('harga', location='args', type=int)
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            user_id = get_jwt_claims()['user_id']
            qry = Items.query.filter_by(user_id=user_id)

            if args['id'] is not None:
                qry = qry.filter_by(id=args['id'])

            if args['nama'] is not None:
                # qry = qry.filter_by(nama=args['nama'])
                qry = qry.filter(Items.nama.like("%"+args['nama']+"%"))#example
            if args['harga'] is not None:
                qry = qry.filter_by(harga=args['harga'])

            if qry.first() is None:
                return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                temp = marshal(row, Items.respon_fields)
                rows.append(temp)

            return {'status': 'OK','message':'success','page':args['p'],'items':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            user_id = get_jwt_claims()['user_id']
            qry = Items.query.filter_by(user_id=user_id).filter_by(id=id).first()
            if qry is not None:
                temp = marshal(qry,Items.respon_fields)
                return {'status': 'OK','message':'success','item':temp}, 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def post(self):
        status = get_jwt_claims()['status']
        if status != "merchant":
            return {'message':'Only merchant can post item'},404, { 'Content-Type': 'application/json' }
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('merek', location='json', required=True)
        parser.add_argument('kategori', location='json', required=True)
        parser.add_argument('detail', location='json')
        parser.add_argument('harga', location='json', type=int, required=True)
        parser.add_argument('stock', location='json', type=int, required=True)
        parser.add_argument('url_picture', location='json', required=True)
        args = parser.parse_args()#sudah jadi dictionary
        
        if (args['kategori'] != "Tenda & Furniture" and args['kategori'] != "Matras Camping" and args['kategori'] != "Sleeping Bag"
            and args['kategori'] != "Cooking Set" and args['kategori'] != "Hammock"):
            return {'message':'only Tenda & Furniture or Matras Camping or Sleeping Bag or Cooking Set or Hammock'},404, { 'Content-Type': 'application/json' }

        user_id = get_jwt_claims()['user_id']
        created_at = datetime.now()
        updated_at = datetime.now()
        # created_at = date.today()
        # updated_at = date.today()
        
        item = Items(None,args['nama'],args['merek'],args['kategori'],args['detail'],args['harga'],args['stock'],args['url_picture'],user_id,created_at,updated_at)
        db.session.add(item)
        db.session.commit()
        feedback = marshal(item,Items.respon_fields) 
        return {'status': 'OK','message':'success post item','item':feedback}, 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def patch(self,id):
        status = get_jwt_claims()['status']
        if status != "merchant" and status != "admin":
            return {'message':'Only merchant and admin'},404, { 'Content-Type': 'application/json' }
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json')
        parser.add_argument('merek', location='json')
        parser.add_argument('kategori', location='json')
        parser.add_argument('detail', location='json')
        parser.add_argument('harga', location='json', type=int)
        parser.add_argument('stock', location='json', type=int)
        parser.add_argument('url_picture', location='json')
        args = parser.parse_args()#sudah jadi dictionary

        user_id = get_jwt_claims()['user_id']
        if status == "merchant":
            qry = Items.query.filter_by(user_id=user_id).filter_by(id=id).first()
        else:
            qry = Items.query.filter_by(id=id).first()

        if qry is not None:
            if args['nama'] is not None:
                qry.nama = args['nama']
            if args['merek'] is not None:
                qry.merek = args['merek']
            if args['kategori'] is not None:
                if (args['kategori'] != "Tenda & Furniture" and args['kategori'] != "Matras Camping" and args['kategori'] != "Sleeping Bag"
                    and args['kategori'] != "Cooking Set" and args['kategori'] != "Hammock"):
                    return {'message':'only Tenda & Furniture or Matras Camping or Sleeping Bag or Cooking Set or Hammock'},404, { 'Content-Type': 'application/json' }
                qry.kategori = args['kategori']
            if args['detail'] is not None:
                qry.detail = args['detail']
            if args['harga'] is not None:
                qry.harga = args['harga']
            if args['stock'] is not None:
                qry.stock = args['stock']
            if args['url_picture'] is not None:
                qry.url_picture = args['url_picture']
            qry.updated_at = datetime.now()
            db.session.commit()
            feedback = marshal(qry, Items.respon_fields)
            return {'status': 'OK','message':'success edit item','item':feedback},200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def delete(self,id):
        status = get_jwt_claims()['status']
        if status != "merchant" and status != "admin":
            return {'message':'Only merchant and admin'},404, { 'Content-Type': 'application/json' }
        user_id = get_jwt_claims()['user_id']
        if status == "merchant":
            qry = Items.query.filter_by(user_id=user_id).filter_by(id=id).first()
        else:
            qry = Items.query.filter_by(id=id).first()
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            feedback = marshal(qry, Items.respon_fields)
            return {'status': 'OK','message':"item has been deleted",'item':feedback},200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }

    def put(self):
        return 'Not yet implement', 501


api.add_resource(ItemsResource, '','/<int:id>')