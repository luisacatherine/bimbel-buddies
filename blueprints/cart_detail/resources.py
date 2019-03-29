import logging, json
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from . import *
from blueprints.item import *
from blueprints import db
from datetime import date, datetime

bp_cartdetail = Blueprint('cartdetail', __name__)
api = Api(bp_cartdetail)

class CartsDetailResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self,id=None):
        status = get_jwt_claims()['status']
        if status != "customer" and status != "admin":
            return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
        if id is None:
            customer_id = get_jwt_claims()['user_id']
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('nama_item', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            if status == "customer":
                qry = Cart.query.filter_by(customer_id=customer_id).filter_by(status="not yet paid")
            else:
                qry = Cart.query

            if args['id'] is not None:
                qry = qry.filter_by(id=args['id'])
            if args['nama_item'] is not None:
                qry = qry.filter(Cart.nama_item.like("%"+args['nama_item']+"%"))

            # if qry.first() is None:
            #     return {'status': 'NOT_FOUND','message':'cart not found'},404, { 'Content-Type': 'application/json' }

            rows = []
            total_harga=0
            for row in qry.limit(args['rp']).offset(offset).all():
                total_harga += row.harga
                temp = marshal(row, Cart.respon_fields)
                rows.append(temp)

            return {'status': 'OK','message':'success',"totalHarga":total_harga,'page':args['p'],'carts':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            customer_id = get_jwt_claims()['user_id']
            if status == "customer":
                qry = Cart.query.filter_by(customer_id=customer_id).filter_by(status="not yet paid").filter_by(id=id).first()
            else:
                qry = Cart.query.filter_by(id=id).first()
            
            if qry is not None:
                temp = marshal(qry, Cart.respon_fields)
                return {'status': 'OK','message':'success','cart':temp}, 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND','message':'cart not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def post(self):
        status = get_jwt_claims()['status']
        if status != "customer":
            return {'message':'Only customer can post cart detail'},404, { 'Content-Type': 'application/json' }
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', location='json', type=int, required=True)
        parser.add_argument('qty', location='json', type=int, required=True)
        args = parser.parse_args()#sudah jadi dictionary
        
        qry = Items.query.get(args["item_id"])
        if qry is None:
            return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
        qry.stock -= args["qty"]
        # db.session.commit()
        json_item = marshal(qry,Items.respon_fields)
        nama_item = json_item["nama"]
        url_picture = json_item["url_picture"]
        
        if json_item["stock"] < args["qty"]:
            return {'status': 'NOT_FOUND','message':'not enough stock'},404, { 'Content-Type': 'application/json' }
        
        harga = json_item["harga"] * args["qty"]
        customer_id = get_jwt_claims()['user_id']
        created_at = datetime.now()
        updated_at = datetime.now()

        cart_detail = Cart(None,0,args["item_id"],nama_item,url_picture,args["qty"],harga,customer_id,"not yet paid",created_at,updated_at)
        db.session.add(cart_detail)
        db.session.commit()
        feedback = marshal(cart_detail,Cart.respon_fields) 
        return {'status': 'OK','message':'success carting','cart':feedback}, 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def delete(self,id):
        status = get_jwt_claims()['status']
        customer_id = get_jwt_claims()['user_id']
        if status != "customer" and status != "admin":
            return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
        if status == "customer":
            qry = Cart.query.filter_by(customer_id=customer_id).filter_by(status="not yet paid").filter_by(id=id).first()
        else:
            qry = Cart.query.filter_by(id=id).filter_by(status="not yet paid").first()
        if qry is not None:
            item = Items.query.get(qry.item_id)
            item.stock += qry.qty
            db.session.delete(qry)
            db.session.commit()
            return {'status': 'OK','message':"cart item has been deleted",'item':marshal(qry, Cart.respon_fields)},200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'cart item not found'},404, { 'Content-Type': 'application/json' }

    def put(self):
        return 'Not yet implement', 501


api.add_resource(CartsDetailResource, '','/<int:id>')