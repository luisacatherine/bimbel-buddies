import logging, json, hashlib
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from . import *
from ..Client import *
from datetime import date, datetime
from blueprints import db

bp_review = Blueprint('review', __name__)
api = Api(bp_review)

class ReviewResources(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        status = get_jwt_claims()['tipe']
        if status == "admin" or status == 'tentor':
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('id_murid',type=int, location='args')
            parser.add_argument('id_tentor',type=int, location='args')
            parser.add_argument('rating', type=int, location='args') # 1 sampai 5
            parser.add_argument('created_at', location='args')
            parser.add_argument('updated_at', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']

            qry_review = Reviews.query

            if status == 'tentor':
                tentor = Tentors.query.filter(Tentors.user_id == get_jwt_claims()['id']).first()
                qry_review = qry_review.filter_by(id_tentor = tentor.id)
            
            if args['id'] is not None:
                qry_review = qry_review.filter_by(id=args['id'])

            if args['id_murid'] is not None:
                qry_review = qry_review.filter_by(id_murid=args['id_murid'])

            if args['id_tentor'] is not None:
                qry_review = qry_review.filter_by(id_tentor=args['id_tentor'])

            if args['rating'] is not None:
                qry_review = qry_review.filter_by(rating=args['rating'])
            
            if args['created_at'] is not None:
                qry_review = qry_review.filter_by(created_at=args['created_at'])

            if args['updated_at'] is not None:
                qry_review = qry_review.filter_by(updated_at=args['updated_at'])

            rows = []
            for row in qry_review.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Reviews.respon_fields))

            return {'status': 'OK','message':"success",'data_review': rows}, 200, { 'Content-Type': 'application/json' }
        else :
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
    
    # ===== Post Review Client =====
    @jwt_required
    def post(self): 
        tipe = get_jwt_claims()['tipe']
        if tipe != "client":
            return {'message':'UNAUTHORIZED'}, 401, { 'Content-Type': 'application/json' }
        
        murid = Clients.query.filter(Clients.user_id == get_jwt_claims()['id']).first()

        parser = reqparse.RequestParser()
        parser.add_argument('id_booking', location='json', type=int, required=True)
        parser.add_argument('rating', type=int, location='json', required=True, choices=[1, 2, 3, 4, 5]),
        parser.add_argument('deskripsi', location='json', required=True)
        args = parser.parse_args()

        # Cek apakah client tersebut berhak menulis review pada bookingan ini
        # Cek apakah bookingan tersebut diselesaikan oleh client ini
        qry_booking = Booking.query.filter(Booking.id_booking == args['id_booking']).first()
        if (qry_booking.id_murid != murid.id):
            return {'status': 'gagal', 'message': 'Anda tidak berhak menulis review untuk sesi pelajaran ini!'}, 401, { 'Content-Type': 'application/json' }
        
        if (qry_booking.status != 'done'):
            return {'status': 'gagal', 'message': 'Selesaikan dahulu sesi pelajaran Anda sebelum menulis review!'}, 401, {'Content-Type': 'application/json'}

        qry_review = Reviews.query.filter(Reviews.id_booking == args['id_booking']).first()
        if qry_review is not None:
            return {'status': 'gagal', 'message': 'Anda sudah pernah menulis review untuk sesi pelajaran ini!'}, 401, { 'Content-Type': 'application/json' }

        # Ubah rating keseluruhan tentor
        qry_tentor = Tentors.query.filter(Tentors.id == qry_booking.id_tentor).first()
        qry_tentor.rating = ((qry_tentor.rating * qry_tentor.qty_rating + args['rating']) / (qry_tentor.qty_rating + 1))
        qry_tentor.qty_rating += 1
        
        created_at = datetime.now()
        updated_at = datetime.now()
        review = Reviews(None, murid.id, qry_booking.id_tentor, args['id_booking'], args['rating'], args['deskripsi'], created_at, updated_at)
        db.session.add(review)
        db.session.commit()
        return {'status': 'OK', 'message':"success add review", 'client': marshal(murid, Clients.respon_fields), 'data': marshal(review, Reviews.response_fields)}, 200, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(ReviewResources, '','/<int:id>')