import logging, json, hashlib
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
from datetime import date, datetime
#add __init__.py
from . import *
from ..booking import *
from ..Client import *
from blueprints import db

bp_topup = Blueprint('topup', __name__)
api = Api(bp_topup)

class PaymentResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        status = get_jwt_claims()['status']
        if status == "admin":
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('id_booking',type=int, location='args')
            parser.add_argument('created_at', location='args') # Bank / Indo / Alfa / Kantor Pos
            parser.add_argument('updated_at', location='args') # Sukses / Wait tentor / Cancel
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            # qry_client = Clients.query
            qry_payment = Payments.query
            
            if args['id'] is not None:
                qry_payment = qry_payment.filter_by(id=args['id'])

            if args['id_booking'] is not None:
                qry_payment = qry_payment.filter_by(id=args['id_booking'])

            if args['created_at'] is not None:
                qry_payment = qry_payment.filter_by(created_at=args['created_at'])
            
            if args['updated_at'] is not None:
                qry_payment = qry_payment.filter_by(updated_at=args['updated_at'])

            rows = []
            for row in qry_payment.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Payments.respon_fields))

            return {'status': 'OK','message':"success",'data_Payment':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }

    # ===== verifikasi duit admin =====
    @jwt_required
    def put(self,id):
        tipe = get_jwt_claims()['tipe']
        if tipe != "admin":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }            
        qry_payment = Payments.query.get(id)
        payment = marshal(qry_payment, Payments.respon_fields)
        parser = reqparse.RequestParser()
        parser.add_argument('id_booking', location='json', default=payment["id_booking"])
        parser.add_argument('nominal', location='json', default=payment["nominal"])
        parser.add_argument('total_nominal', location='json', default=payment["total_nominal"])
        parser.add_argument('status', location='json', required=True)
        parser.add_argument('created_at', location='json', default=payment["created_at"])
        args = parser.parse_args()

        # Verifikasi Admin
        if qry_payment is not None:
            qry_payment.id_murid = args['id_booking']
            qry_payment.nominal = args['nominal']
            qry_payment.total_nominal = args['total_nominal']
            qry_payment.status = args['status']
            qry_payment.created_at = args['created_at']
            qry_payment.updated_at = datetime.now()
            db.session.commit()
            return {'status': 'OK','message':"success verifikasi pembayaran",'data':marshal(qry_topup, Topups.respon_fields)},200, { 'Content-Type': 'application/json' }        
        return {'status': 'NOT_FOUND','message':'payment not found'},404, { 'Content-Type': 'application/json' }

    # ===== Delete topup =====
    @jwt_required
    def delete(self,id):
        tipe = get_jwt_claims()['tipe']
        if tipe != "admin":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }            
        qry_payment = Payments.query.get(id)
        payment = marshal(qry_payment, Payments.respon_fields)
        parser = reqparse.RequestParser()
        parser.add_argument('id_booking', location='json', default=payment["id_booking"])
        parser.add_argument('nominal', location='json', default=payment["nominal"])
        parser.add_argument('total_nominal', location='json', default=payment["total_nominal"])
        parser.add_argument('status', location='json', required=True)
        parser.add_argument('created_at', location='json', default=payment["created_at"])
        args = parser.parse_args()

        # Verifikasi Admin
        if qry_payment is not None:
            qry_payment.id_murid = args['id_booking']
            qry_payment.nominal = args['nominal']
            qry_payment.total_nominal = args['total_nominal']
            qry_payment.status = args['status']
            qry_payment.created_at = args['created_at']
            qry_payment.updated_at = datetime.now()
            db.session.commit()
            return {'status': 'OK','message':"success menghapus pembayaran",'data':marshal(qry_topup, Topups.respon_fields)},200, { 'Content-Type': 'application/json' }        
        return {'status': 'NOT_FOUND','message':'payment not found'},404, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(PaymentResources, '','/<int:id>')