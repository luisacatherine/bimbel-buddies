import logging, json, hashlib, requests, re
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
from . import *
from blueprints import db
from datetime import date, datetime

bp_token = Blueprint('token', __name__)
api = Api(bp_token)

class TokenResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def post(self):
        jwtClaims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('expo_token', location='json', required=True)
        args = parser.parse_args()
        args['user_id'] = jwtClaims['id']
        qry = Token.query.filter_by(user_id = jwtClaims['id']).first()
        if qry is None:
            created_at = datetime.now()
            updated_at = datetime.now()
            token = Token(None, args['user_id'], args['expo_token'], created_at, updated_at)
            db.session.add(token)
            db.session.commit()
            return { 'status': 'Ok', 'data_token': marshal(token, Token.response_fields) }, 200, { 'Content-Type': 'application/json' }
        else:
            qry.expo_token = args['expo_token']
            updated_at = datetime.now()
            db.session.commit()
            return { 'status': 'Ok', 'data_token': marshal(qry, Token.response_fields) }, 200, { 'Content-Type': 'application/json' }

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='args')
        args = parser.parse_args()
        qry = Token.query.filter_by(user_id = args['user_id']).first()
        if qry is not None:
            return { 'status': 'Ok', 'data_token': marshal(qry, Token.response_fields) }, 200, { 'Content-Type': 'application/json' }
        else:
            return { 'status': 'Gagal', 'message': 'Anda tidak diperbolehkan memberi notifikasi pada user ini!' }, 200, { 'Content-Type': 'application/json' }

api.add_resource(TokenResource, '','/<int:id>')