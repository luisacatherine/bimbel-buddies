import logging, json, hashlib
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from . import *
from blueprints import db

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

class AdminResource(Resource):

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
            parser.add_argument('status', location='args')
            parser.add_argument('username', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            qry = Users.query
            
            if args['id'] is not None:
                qry = qry.filter_by(user_id=args['id'])

            if args['status'] is not None:
                qry = qry.filter_by(status=args['status'])
            
            if args['username'] is not None:
                qry = qry.filter_by(username=args['username'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Users.respon_fields))

            return {'status': 'OK','message':"success",'users':rows}, 200, { 'Content-Type': 'application/json' }
        else :
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def put(self,id):
        status = get_jwt_claims()['status']
        if status != "admin":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }            
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
        
        if args['status'] != "admin" and args['status'] != "merchant" and args['status'] != "customer":
            return {'message':'only merchant or customer or admin'},404, { 'Content-Type': 'application/json' }

        qry = Users.query.get(id)
            # select * from where id = id
        if qry is not None:
            qry.username = args['username']
            qry.password = hashlib.md5(args['password'].encode()).hexdigest()
            qry.status = args['status']
            qry.email = args['email']
            qry.alamat = args['alamat']
            qry.contact = args['contact']
            db.session.commit()
            return {'status': 'OK','message':"success edit user",'user':marshal(qry, Users.respon_fields)},200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def delete(self,id):
        status = get_jwt_claims()['status']
        if status != "admin":
            return {'message':'UNAUTHORIZED'},404, { 'Content-Type': 'application/json' }
        qry = Users.query.get(id)
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return {'status': 'OK','message':"user has been deleted",'user':marshal(qry, Users.respon_fields)},200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(AdminResource, '','/<int:id>')