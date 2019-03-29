import logging, json
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from blueprints.users import *
from blueprints import db

bp_user_me = Blueprint('user_me', __name__)
api = Api(bp_user_me)

class UserDetailResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):    
        # id = get_jwt_claims()
        # return id,200, { 'Content-Type': 'application/json' }
        id = get_jwt_claims()['user_id']
        qry = Users.query.get(id)
            # select * from where id(pk) = id
        if qry is not None:
            return marshal(qry, Users.respon_fields),200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def put(self):
        id = get_jwt_claims()['user_id']
        qry = Users.query.get(id)
        temp = marshal(qry, Users.respon_fields)            
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', default=temp["username"])
        parser.add_argument('password', location='json', default=temp["password"])
        parser.add_argument('status', location='json', default=temp["status"]),
        parser.add_argument('email', location='json', default=temp["email"]),
        parser.add_argument('alamat', location='json', default=temp["alamat"]),
        parser.add_argument('contact', location='json', default=temp["contact"])
        args = parser.parse_args()
        
        if args['status'] != "merchant" and args['status'] != "customer":
            return {'message':'only merchant or customer'},404, { 'Content-Type': 'application/json' }

        qry = Users.query.get(id)
            # select * from where id = id
        if qry is not None:
            qry.username = args['username']
            qry.password = args['password']
            qry.status = args['status']
            qry.email = args['email']
            qry.alamat = args['alamat']
            qry.contact = args['contact']
            db.session.commit()
            return marshal(qry, Users.respon_fields),200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self):
        id = get_jwt_claims()['user_id']
        qry = Users.query.get(id)
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return marshal(qry, Users.respon_fields),200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501

api.add_resource(UserDetailResource, '')