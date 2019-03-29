import logging
import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from . import *
from flask_jwt_extended import get_jwt_claims, jwt_required
import datetime

bp_harga = Blueprint('harga', __name__)
api = Api(bp_harga)

class HargaResource(Resource):

    def __init__(self):
        pass
    
    def get(self, id=None):
        if (id == None):
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('tingkat', choices=['SD', 'SMP', 'SMA'])
            args = parser.parse_args()
            offset = (args['p'] * args['rp']) - args['rp']
            qry = Harga.query

            if args['tingkat'] is not None:
                qry = qry.filter_by(tingkat=args['tingkat'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Harga.response_fields))
            return {'status': 'oke', 'harga': rows}, 200, {'Content-Type': 'application/json'}
        else:
            qry = Harga.query.get(id)
            if qry is not None:
                return {'status': 'oke', 'harga': marshal(qry, Harga.response_fields)}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'harga not found'}, 404, {'Content-Type': 'application/json'}

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tingkat', location='json')
        parser.add_argument('harga', location='json')
        args = parser.parse_args()
        qry = Harga.query.filter(Harga.tingkat == args['tingkat']).first()
        qry.harga = args['harga']
        qry.updated_at = datetime.datetime.now()
        db.session.commit()
        return {'status': 'oke', 'harga': marshal(qry, Harga.response_fields)}, 200, {'Content-Type': 'application/json'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tingkat', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        args = parser.parse_args()
        args['created_at'] = datetime.datetime.now()
        args['updated_at'] = datetime.datetime.now()
        harga = Harga(None, args['tingkat'], args['harga'], args['created_at'], args['updated_at'])
        db.session.add(harga)
        db.session.commit()
        return {'status': 'oke', 'harga': marshal(harga, Harga.response_fields)}, 200, {'Content-Type': 'application/json'}

api.add_resource(HargaResource, '/<int:id>', '')

