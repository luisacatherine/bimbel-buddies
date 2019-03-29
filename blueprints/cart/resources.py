import logging, json
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from . import *
from blueprints.users import *
from blueprints.cart_detail import *
from blueprints import db
from datetime import date, datetime

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)

class TransactionsResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self,id=None):
        status = get_jwt_claims()['status']
        if status != "customer" and status != "admin":
            return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('status', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            customer_id = get_jwt_claims()['user_id']
            if status == "customer":
                qry = Transactions.query.filter_by(customer_id=customer_id)
            else:
                qry = Transactions.query

            if args['status'] is not None:
                qry = qry.filter_by(status=args['status'])

            if args['id'] is not None:
                qry = qry.filter_by(id=args['id'])
            
            if qry.first() is None:
                return {'status': 'NOT_FOUND','message':'transaction not found'},404, { 'Content-Type': 'application/json' }
            
            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                temp = marshal(row, Transactions.respon_fields)
                cart = Cart.query.filter_by(customer_id=customer_id).filter_by(transaction_id=row.id)
                details=[]
                for bar in cart.all():
                    result = marshal(bar, Cart.respon_fields)
                    details.append(result)
                temp["detail"] = details
                rows.append(temp)


            return {'status': 'OK','message':'success','page':args['p'],'transaction':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            customer_id = get_jwt_claims()['user_id']
            if status == "customer":
                qry = Transactions.query.filter_by(customer_id=customer_id).filter_by(id=id).first()
            else:
                qry = Transactions.query.filter_by(id=id).first()
            if qry is not None:
                tr = marshal(qry, Transactions.respon_fields)
                
                cart = Cart.query.filter_by(customer_id=customer_id).filter_by(transaction_id=id)

                details=[]
                for row in cart.all():
                    temp = marshal(row, Cart.respon_fields)
                    details.append(temp)
                tr["detail"]=details

                return {'status': 'OK','message':'success','transaction':tr}, 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND','message':'transaction not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def post(self):
        status = get_jwt_claims()['status']
        if status != "customer":
            return {'message':'Only customer can post transaction'},404, { 'Content-Type': 'application/json' }
        parser = reqparse.RequestParser()
        parser.add_argument('paid_method', location='json', default="ngutang")
        args = parser.parse_args()#sudah jadi dictionary

        customer_id = get_jwt_claims()['user_id']
        status = "waiting"
        created_at = datetime.now()
        updated_at = datetime.now()

        cart = Cart.query.filter_by(customer_id=customer_id).filter_by(transaction_id=0)
        if cart.first() is None:
            return {'status': 'NOT_FOUND','message':'cart not found'},404, { 'Content-Type': 'application/json' }

        total_qty = 0 
        total_harga = 0 
        for row in cart.all():
            temp = marshal(row, Cart.respon_fields)    
            total_qty += temp["qty"]
            total_harga += temp["harga"]

        tr = Transactions(None,customer_id,status,total_qty,total_harga,args["paid_method"],created_at,updated_at)
        db.session.add(tr)
        db.session.commit()
        
        for row in cart.all():
            row.transaction_id = tr.id
            row.status = "paid"
        db.session.commit()
        
        cart = Cart.query.filter_by(customer_id=customer_id).filter_by(transaction_id=tr.id)                           

        details=[]
        for row in cart.all():
            temp = marshal(row, Cart.respon_fields)
            details.append(temp)

        feedback = marshal(tr,Transactions.respon_fields) 
        feedback["detail"]=details
        return {'status': 'OK','message':'success transaction','transaction':feedback}, 200, { 'Content-Type': 'application/json' }
    
    # @jwt_required
    # def delete(self,id):
    #     status = get_jwt_claims()['status']
    #     if status != "customer" and status != "admin":
    #         return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
    #     customer_id = get_jwt_claims()['user_id']
    #     if status == "customer":
    #         qry = Cart.query.filter_by(customer_id=customer_id).filter_by(id=id).first()
    #     else:
    #         qry = Cart.query.filter_by(id=id).first()
    #     if qry is not None:
    #         db.session.delete(qry)
    #         db.session.commit()
    #         return str(marshal(qry, Cart.respon_fields))+"has been deleted",200, { 'Content-Type': 'application/json' }
    #     return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }

    def put(self):
        return 'Not yet implement', 501


api.add_resource(TransactionsResource, '','/<int:id>')