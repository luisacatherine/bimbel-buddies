import logging, json, hashlib
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
from . import *
from ..Client import *
from datetime import date, datetime
#add __init__.py
from blueprints import db

bp_topup = Blueprint('topup', __name__)
api = Api(bp_topup)

class TopupResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id=None):
        status = get_jwt_claims()['tipe']
        if status == "admin" or status == 'bank':
            if (id == None):
                parser = reqparse.RequestParser()
                parser.add_argument('p', type=int, location='args', default=1)
                parser.add_argument('rp', type=int, location='args', default=5)
                parser.add_argument('id_murid', type=int, location='args')
                parser.add_argument('metode_pembayaran', location='args', choices=['transfer', 'cash', 'credit']) # Bank / Indo / Alfa / Kantor Pos
                parser.add_argument('status', location='args', choices=['waiting', 'ok']) # Sukses / Wait tentor / Cancel
                args = parser.parse_args() #sudah jadi dictionary    
                
                offset = (args['p'] * args['rp']) - args['rp']
                qry_topup = Topups.query
                
                if args['id_murid'] is not None:
                    qry_topup = qry_topup.filter_by(id_murid=args['id_murid'])

                if args['status'] is not None:
                    qry_topup = qry_topup.filter_by(status=args['status'])
                
                if args['metode_pembayaran'] is not None:
                    qry_topup = qry_topup.filter_by(metode_pembayaran=args['metode_pembayaran'])

                rows = []
                for row in qry_topup.limit(args['rp']).offset(offset).all():
                    rows.append(marshal(row, Topups.respon_fields))
                return {'status': 'OK','message':"success",'data_TopUp':rows}, 200, { 'Content-Type': 'application/json' }
            else:
                qry_topup = Topups.query.get(id)
                if qry_topup is not None:
                    return {'status': 'OK', 'message': 'success', 'data_TopUp': marshal(qry_topup, Topups.respon_fields)}, 200, {'Content-Type': 'application/json'}
                else:
                    return {'status': 'NOT_FOUND','message':'topup not found'}, 404, { 'Content-Type': 'application/json' }
        
        elif status == 'client':
            user_id_murid = get_jwt_claims()['id']
            id_murid = Clients.query.filter(Clients.user_id == user_id_murid).first()
            if (id == None):
                parser = reqparse.RequestParser()
                parser.add_argument('p', type=int, location='args', default=1)
                parser.add_argument('rp', type=int, location='args', default=5)
                parser.add_argument('status', location='args', choices=['waiting', 'ok'])
                args = parser.parse_args()
                offset = (args['p'] * args['rp']) - args['rp']
                qry_topup = Topups.query.filter_by(id_murid=args['id_murid'])

                if args['status'] is not None:
                    qry_topup = qry_topup.filter_by(status=args['status'])
            else:
                qry_topup = Topups.query.get(id)
                if qry_topup is not None:
                    if qry_topup.id_murid == id_murid:
                        return {'status': 'OK', 'message': 'success', 'data_TopUp': marshal(qry_topup, Topups.respon_fields)}, 200, {'Content-Type': 'application/json'}
                    else:
                        return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
                else:
                    return {'status': 'NOT_FOUND','message':'topup not found'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
    
    # ===== Post Topup Client =====
    @jwt_required
    def post(self): 
        jwtClaims = get_jwt_claims()
        tipe = jwtClaims['tipe']

        if tipe != "client":
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
        
        qry_client = Clients.query.filter(Clients.user_id == get_jwt_claims()['id']).first()
        user_id = qry_client.id
        client = marshal(qry_client, Clients.respon_fields)
        parser = reqparse.RequestParser()
        parser.add_argument('nominal', type=int, location='json', required=True),
        parser.add_argument('metode_pembayaran', location='json', required=True, choices=['transfer', 'cash', 'credit'])
        args = parser.parse_args()
        created_at = datetime.now()
        updated_at = datetime.now()
        topup = Topups(None, user_id, args['nominal'], args['metode_pembayaran'], 'waiting', created_at, updated_at)
        db.session.add(topup)
        db.session.commit()
        return {'status': 'OK','message':"success add topup",'client':client,'data': marshal(topup, Topups.respon_fields)}, 200, { 'Content-Type': 'application/json' }

    # ===== Put verifikasi bank =====
    @jwt_required
    def put(self, id):
        tipe = get_jwt_claims()['tipe']
        if tipe != "bank":
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }       
        qry_topup = Topups.query.get(id)
        qry_client = Clients.query.filter(Clients.id == qry_topup.id_murid).first()

        parser = reqparse.RequestParser()
        parser.add_argument('id_murid', location='json', default=qry_topup.id_murid)
        parser.add_argument('nominal', location='json', default=qry_topup.nominal)
        parser.add_argument('metode_pembayaran', location='json', default=qry_topup.metode_pembayaran, choices=['transfer', 'cash', 'credit'])
        parser.add_argument('status', location='json', required=True, choices=['waiting', 'ok'])
        parser.add_argument('created_at', location='json', default=qry_topup.created_at)
        args = parser.parse_args()

        # Verifikasi Bank
        if qry_topup is not None:
            qry_topup.id_murid = args['id_murid']
            qry_topup.nominal = args['nominal']
            qry_topup.metode_pembayaran = args['metode_pembayaran']
            if args['status'] == 'ok':
                # Penjumlahan saldo client
                qry_client.saldo += args['nominal']
            qry_topup.status = args['status']
            qry_topup.created_at = args['created_at']
            qry_topup.updated_at = datetime.now()
            db.session.commit()
            return {'status': 'OK','message': "success verifikasi topup", 'data': marshal(qry_topup, Topups.respon_fields)}, 200, { 'Content-Type': 'application/json' }        
        return {'status': 'NOT_FOUND','message':'topup not found'}, 404, { 'Content-Type': 'application/json' }

    # ===== Delete topup =====
    @jwt_required
    def delete(self, id):
        tipe = get_jwt_claims()['tipe']
        if tipe != "client" or tipe != "admin" or tipe != "bank":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }
        qry_topup = Topups.query.get(id)
        topup = marshal(qry_topup, Topups.respon_fields)

        if qry_topup is not None:
            qry_topup.id_murid = topup['id_murid']
            qry_topup.nominal = topup['nominal']
            qry_topup.metode_pembayaran = topup['metode_pembayaran']
            qry_topup.status = 'Deleted'
            qry_topup.created_at = topup['created_at']
            qry_topup.updated_at = datetime.now()
            # db.session.delete(qry)
            db.session.commit()
            return {'status': 'OK','message':"Topup has been deleted",'data': marshal(qry_topup, Topups.respon_fields)}, 200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'Topup id not found'},404, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(TopupResource, '','/<int:id>')