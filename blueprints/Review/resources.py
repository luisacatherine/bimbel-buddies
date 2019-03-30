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
from ..booking import *
from blueprints import db

bp_review = Blueprint('review', __name__)
api = Api(bp_review)

class ReviewResources(Resource):

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
            parser.add_argument('id_tentor',type=int, location='args')
            parser.add_argument('rating', type=int, location='args') # 1 sampai 5
            parser.add_argument('created_at', location='args')
            parser.add_argument('updated_at', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            # qry_client = Clients.query
            qry_review = Reviews.query
            
            if args['id'] is not None:
                qry_review = qry_review.filter_by(id=args['id'])

            if args['id_murid'] is not None:
                qry_review = qry_review.filter_by(id_murid=args['id_murid'])

            if args['id_tentor'] is not None:
                qry_review = qry_review.filter_by(id_tentor=args['id_tentor'])

            if args['rating'] is not None:
                qry_review = qry_review.filter_by(rating=args['rating'])
            
            if args['deskripsi'] is not None:
                qry_review = qry_review.filter_by(deskripsi=args['deskripsi'])
            
            if args['created_at'] is not None:
                qry_review = qry_review.filter_by(created_at=args['created_at'])

            if args['updated_at'] is not None:
                qry_review = qry_review.filter_by(updated_at=args['updated_at'])

            rows = []
            for row in qry_review.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Reviews.respon_fields))

            return {'status': 'OK','message':"success",'data_review':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }
    
    # ===== Post Review Client =====
    @jwt_required
    def post(self,id): 
        tipe = get_jwt_claims()['tipe']
        if tipe != "client":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }            
        qry_client = Clients.query.get(get_jwt_claims['id'])
        client = marshal(qry_client, Clients.respon_token)
        qry_booking = Booking.query
        qry_booking = qry_booking.filter_by(id_murid=get_jwt_claims()['id']) 
        
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, location='json', required=True),
        parser.add_argument('deskripsi', location='json', required=True)
        args = parser.parse_args()

        created_at = datetime.now()
        updated_at = datetime.now()
        review = Reviews(None, get_jwt_claims()['id'],qry_booking.id_tentor,args['rating'],args['deskripsi'],created_at,updated_at)
        db.session.add(review)
        db.session.commit()
        return {'status': 'OK','message':"success add review",'client':client,'data':marshal(review, Reviews.respon_fields)},200, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(ReviewResources, '','/<int:id>')