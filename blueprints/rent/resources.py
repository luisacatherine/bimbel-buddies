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
from blueprints.book import Books 
from blueprints.user import Users

bp_rent = Blueprint('rent', __name__)
api = Api(bp_rent)

class RentResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self,rent_id=None):
        if rent_id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('book_id',type=int, location='args')
            parser.add_argument('user_id',type=int, location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            qry = Rents.query

            if args['book_id'] is not None:
                qry = qry.filter_by(book_id=args['book_id'])
                # qry = qry.filter(Persons.name.like("%"+args['name']+"%"))#example
            if args['user_id'] is not None:
                qry = qry.filter_by(user_id=args['user_id'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                
                temp = marshal(row, Rents.respon_fields)
                qry1 = Users.query.get(temp['user_id'])
                qry2 = Books.query.get(temp['book_id'])
                
                temp['user']= marshal(qry1, Users.respon_fields)
                temp['book']= marshal(qry2, Books.respon_fields)
                rows.append(temp)

            return rows, 200, { 'Content-Type': 'application/json' }
        else :
            qry = Rents.query.get(rent_id)
                # select * from where id = id
            if qry is not None:
                temp = marshal(qry,Rents.respon_fields)
                qry1 = Users.query.get(temp['user_id'])
                qry2 = Books.query.get(temp['book_id'])
                temp['user']= marshal(qry1, Users.respon_fields)
                temp['book']= marshal(qry2, Books.respon_fields) 
                return temp, 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND','messae':'gak ada orang'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('book_id', location='json', type=int, required=True)
        parser.add_argument('user_id', location='json', type=int, required=True)
        
        args = parser.parse_args()#sudah jadi dictionary

        qry1 = Users.query.get(args['user_id'])
        qry2 = Books.query.get(args['book_id'])

        if qry1 is None or qry2 is None:
            return {'Message': 'User ID or Book ID invalid'},404, { 'Content-Type': 'application/json' }

        post_by = get_jwt_claims()['client_id']
        return_date = "2019/2/29"
        rent = Rents(None, args['book_id'], args['user_id'], return_date, post_by)
        db.session.add(rent)
        db.session.commit()
        temp = marshal(rent,Rents.respon_fields)
        temp['user']= marshal(qry1, Users.respon_fields)
        temp['book']= marshal(qry2, Books.respon_fields) 
        return temp, 200, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(RentResource, '','/<int:rent_id>')