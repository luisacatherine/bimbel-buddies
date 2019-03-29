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
from ..Client import *
from blueprints import db

bp_topup = Blueprint('topup', __name__)
api = Api(bp_topup)

class TopupResource(Resource):

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
            parser.add_argument('id_murid',type=int, location='args')
            parser.add_argument('metode_pembayaran', location='args') # Bank / Indo / Alfa / Kantor Pos
            parser.add_argument('status', location='args') # Sukses / Wait tentor / Cancel
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            # qry_client = Clients.query
            qry_topup = Topups.query
            
            if args['id'] is not None:
                qry_topup = qry_topup.filter_by(id=args['id'])

            if args['id_murid'] is not None:
                qry_topup = qry_topup.filter_by(id=args['id_murid'])

            if args['status'] is not None:
                qry_topup = qry_topup.filter_by(status=args['status'])
            
            if args['username'] is not None:
                qry_topup = qry_topup.filter_by(username=args['username'])

            rows = []
            for row in qry_topup.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Topups.respon_fields))

            return {'status': 'OK','message':"success",'data_TopUp':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }
    
    # ===== Post Topup Client =====
    @jwt_required
    def post(self,id): 
        tipe = get_jwt_claims()['tipe']
        if tipe != "client":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }            
        qry_client = Clients.query.get(get_jwt_claims['id'])
        client = marshal(qry_client, Clients.respon_token)
        parser = reqparse.RequestParser()
        parser.add_argument('nominal', type=int, location='json', required=True),
        parser.add_argument('metode_pembayaran', location='json', required=True)
        args = parser.parse_args()

        # Penjumlahan saldo client
        qry_client.saldo = qry_client.saldo + args['nominal']
        db.session.commit()

        created_at = datetime.now()
        updated_at = datetime.now()
        status = 'Wait for transfer'
        topup = Topups(None, get_jwt_claims()['id'],args['nominal'],args['metode_pembayaran'],status,created_at,updated_at)
        db.session.add(topup)
        db.session.commit()
        return {'status': 'OK','message':"success add topup",'client':client,'data':marshal(topup, Topups.respon_fields)},200, { 'Content-Type': 'application/json' }

    # ===== Put verifikasi bank =====
    @jwt_required
    def put(self,id):
        tipe = get_jwt_claims()['tipe']
        if tipe != "bank":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }            
        qry_topup = Topups.query.get(id)
        topup = marshal(topup, Topups.respon_fields)
        parser = reqparse.RequestParser()
        parser.add_argument('status', location='json', required=True)
        args = parser.parse_args()

        # Verifikasi Bank
        qry_topup.status = args['status']
        qry_topup.updated_at = datetime.now()
        db.session.commit()
        return {'status': 'OK','message':"success verifikasi topup",'data':marshal(qry_topup, Topups.respon_fields)},200, { 'Content-Type': 'application/json' }        
        
    @jwt_required
    def delete(self,id):
        tipe = get_jwt_claims()['tipe']
        if tipe != "client" or tipe != "admin" or tipe != "bank":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }
        qry_topup = Topups.query.get(id)
        if qry is not None:
            qry_topup.status = 'Deleted'
            qry_topup.updated_at = datetime.now()
            # db.session.delete(qry)
            db.session.commit()
            return {'status': 'OK','message':"Topup has been deleted",'data':marshal(qry_topup, Topups.respon_fields)},200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'Topup id not found'},404, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(TopupResource, '','/<int:id>')