import logging, json, hashlib
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.users import *
#buat token
from time import strftime 
from logging.handlers import RotatingFileHandler
import random

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()
        qry = Users.query.filter_by(username=args['username']).filter_by(
            password=password).first()
        if qry is not None:
            status = qry.status
            token = create_access_token(marshal(qry,Users.respon_token))
        else:
            return {'status':'UNAUTHORIZED','message':'invalid username or password or not registered yet'}, 401, { 'Content-Type': 'application/json' } 
        return {'status':'success','token':token,"stat":status}, 200, { 'Content-Type': 'application/json' } 

api.add_resource(CreateTokenResources, '')