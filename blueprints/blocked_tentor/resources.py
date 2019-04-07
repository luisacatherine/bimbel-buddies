import logging, json, hashlib, requests, re
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
from geopy.geocoders import Nominatim
import random
from . import *
from blueprints import db
from datetime import date, datetime

bp_blocked = Blueprint('blocked', __name__)
api = Api(bp_blocked)

class BlockedResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        status = get_jwt_claims()['tipe']
        if status == "admin" or status == 'client':
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('client_id',type=int, location='args')
            parser.add_argument('id_tentor',type=int, location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']

            qry_blocked = Blocked.query

            if status == 'client':
                client = Clients.query.filter(Clients.user_id == get_jwt_claims()['id']).first()
                qry_blocked = qry_blocked.filter_by(client_id = client.id)
            
            if args['client_id'] is not None:
                qry_blocked = qry_blocked.filter_by(client_id=args['client_id'])

            if args['id_tentor'] is not None:
                qry_blocked = qry_blocked.filter_by(blocked_tentor=args['id_tentor'])

            rows = []
            for row in qry_blocked.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Blocked.response_fields))

            return {'status': 'OK','message':"success",'data_blocked': rows}, 200, { 'Content-Type': 'application/json' }
        else :
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
    
    # ===== Put Blocked Tentors =====
    @jwt_required
    def post(self): 
        tipe = get_jwt_claims()['tipe']
        if tipe != "client":
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
        
        murid = Clients.query.filter(Clients.user_id == get_jwt_claims()['id']).first()

        parser = reqparse.RequestParser()
        parser.add_argument('id_tentor', location='json', type=int, required=True)
        args = parser.parse_args()
        blocked = Blocked.query.filter(Blocked.client_id == murid.id).filter(Blocked.blocked_tentor == args['id_tentor']).first()

        tentor = Tentors.query.filter(Tentors.id == args['id_tentor']).first()
        if tentor is None:
            return {'status': 'gagal', 'message': 'Tentor tidak ditemukan'}, 404, {'Content-Type': 'application/json'}

        if blocked is not None:
            return {'status': 'gagal', 'message': 'Anda sudah memblokir tentor ini!'}, 401, { 'Content-Type': 'application/json' }
        else:
            created_at = datetime.now()
            updated_at = datetime.now()
            temp2 = Blocked(None, murid.id, args['id_tentor'], created_at, updated_at)
            db.session.add(temp2)
            db.session.commit()
        return {'status': 'OK', 'message':"success block tentor", 'tentor': marshal(tentor, Tentors.respon_fields)}, 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def delete(self, id):
        tipe = get_jwt_claims()['tipe']
        if tipe != "client":
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
        murid = Clients.query.filter(Clients.user_id == get_jwt_claims()['id']).first()
        qry = Blocked.query.filter(Blocked.client_id == murid.id).filter(Blocked.blocked_tentor == id).first().id

        qry_delete = Blocked.query.get(qry)

        if qry_delete is None:
            return {'message': 'Anda belum memblokir user ini!'}, 401, {'Content-Type': 'application/json'}

        if qry_delete.client_id != murid.id:
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
        else:
            db.session.delete(qry_delete)
            db.session.commit()
            return {'status': 'deleted'}, 200, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501

api.add_resource(BlockedResources, '','/<int:id>')
