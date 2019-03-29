import logging, json, hashlib
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from blueprints.users import *
from blueprints import db

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):

    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status', location='json'),
        parser.add_argument('email', location='json'),
        parser.add_argument('alamat', location='json'),
        parser.add_argument('contact', location='json')
        args = parser.parse_args()#sudah jadi dictionary
        
        if args['status'] == "admin":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }
        if args['status'] != "merchant" and args['status'] != "customer":
            return {'message':'only merchant or customer'},404, { 'Content-Type': 'application/json' }

        qry = Users.query.filter_by(username=args['username']).first()
        if qry is not None:
            return {'message':'username is already used'} ,404, { 'Content-Type': 'application/json' }
        password = hashlib.md5(args['password'].encode()).hexdigest()
        user = Users(None,args['username'],password,args['status'],args['email'],args['alamat'],args['contact'])
        db.session.add(user)
        db.session.commit()

        return marshal(user, Users.respon_fields), 200, { 'Content-Type': 'application/json' }
    
    def patch(self):
        return 'Not yet implement', 501


api.add_resource(UserResource, '')