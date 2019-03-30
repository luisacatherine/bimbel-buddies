import logging, json, hashlib, requests, re
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
from geopy.geocoders import Nominatim
import random
#add __init__.py
from . import *
from blueprints.user import *
from blueprints import db
from datetime import date, datetime

bp_clieent = Blueprint('clients', __name__)
api = Api(bp_clieent)

class ClientResource(Resource):
    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('nama', location='json', required=True),
        parser.add_argument('jalan', location='json', required=True),
        parser.add_argument('kota', location='json', required=True),
        parser.add_argument('kelurahan', location='json'),
        parser.add_argument('phone', location='json', required=True),
        parser.add_argument('image', location='json'),
        parser.add_argument('tgl_lahir', location='json', required=True),
        parser.add_argument('gender', location='json', required=True),
        parser.add_argument('tingkat', location='json', required=True),
        parser.add_argument('gender_tentor', location='json'),
        parser.add_argument('ortu', location='json')
        args = parser.parse_args()#sudah jadi dictionary

        qry_user = User.query.filter_by(username=args['username']).first()
        if qry_user is not None:
            return {'message':'username is already used'} ,404, { 'Content-Type': 'application/json' }
        # password = "Azril7812"
        created_at = datetime.now()
        updated_at = datetime.now()
        password = args['password']
        if re.match(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', password):
            print('match')
        else:
            print('not match')
            return {'message':'password harus ada huruf besar, kecil dan angka'} ,404, { 'Content-Type': 'application/json' }
        password = hashlib.md5(args['password'].encode()).hexdigest()
        saldo = 0
        tipe = "client"
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        alamat=""
        if args["kelurahan"] is not None:
            alamat = "Jalan " + args["jalan"] +" "+ args["kelurahan"] +" Kota "+ args["kota"]
        else:
            alamat = "Jalan " + args["jalan"] +" Kota "+ args["kota"]
        location = geolocator.geocode(alamat)
        if location is None:
            return {'message':'alamat kurang yakin'} ,404, { 'Content-Type': 'application/json' }
        print(location.address)
        print((location.latitude, location.longitude))
        lat = location.latitude
        lon = location.longitude
        print(location.raw)
        user = User(None,args['username'],password,tipe)
        db.session.add(user)
        db.session.commit()
        client = Clients(None,user.id,args['nama'],alamat,args['phone'],args['image'],
        args['tgl_lahir'],args['gender'],args['tingkat'],args['gender_tentor'],args['ortu'],
        saldo,lat,lon,created_at,updated_at)
        db.session.add(client)
        db.session.commit()

        return {"status": "OK", "data user":marshal(user, User.respon_fields), "data client":marshal(client, Clients.respon_fields)},200, { 'Content-Type': 'application/json' }

    @jwt_required
    def get(self):    
        # id = get_jwt_claims()
        # return id,200, { 'Content-Type': 'application/json' }
        id = get_jwt_claims()['id']
        qry_user = User.query.get(id)
        qry_client = Clients.query.filter_by(user_id=id).first()
            # select * from where id(pk) = id
        if qry_user is not None and qry_client is not None:
            return {"status": "OK", "data user":marshal(user, User.respon_fields), "data client":marshal(client, Clients.respon_fields)},200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def put(self):
        id = get_jwt_claims()['id']
        qry_user = User.query.get(id)
        qry_client = Clients.query.filter_by(user_id=id).first()
        temp = marshal(qry_user, User.respon_fields)
        temp1 = marshal(qry_client, Clients.respon_fields)
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', default=temp["username"])
        parser.add_argument('password', location='json', default=temp["password"])
        parser.add_argument('nama', location='json' , default=temp1["nama"]),
        parser.add_argument('jalan', location='json'),
        parser.add_argument('kota', location='json'),
        parser.add_argument('kelurahan', location='json'),
        parser.add_argument('phone', location='json' , default=temp1["phone"]),
        parser.add_argument('image', location='json' , default=temp1["image"]),
        parser.add_argument('tgl_lahir', location='json' , default=temp1["tgl_lahir"]),
        parser.add_argument('gender', location='json' , default=temp1["gender"]),
        parser.add_argument('tingkat', location='json' , default=temp1["tingkat"]),
        parser.add_argument('gender_tentor', location='json' , default=temp1["gender_tentor"]),
        parser.add_argument('ortu', location='json' , default=temp1["ortu"])
        args = parser.parse_args()
        
        # if args['status'] != "merchant" and args['status'] != "customer":
        #     return {'message':'only merchant or customer'},404, { 'Content-Type': 'application/json' }

        qry_user = User.query.get(id)
        qry_client = Clients.query.filter_by(user_id=id).first()
            # select * from where id = id
        if qry_user is not None and qry_client is not None:
            if (args["kota"] is not None and args["jalan"] is not None):
                geolocator = Nominatim(user_agent="specify_your_app_name_here")
                alamat=""
                if args["kelurahan"] is not None:
                    alamat = "Jalan " + args["jalan"] +" "+ args["kelurahan"] +" Kota "+ args["kota"]
                else:
                    alamat = "Jalan " + args["jalan"] +" Kota "+ args["kota"]
                location = geolocator.geocode(alamat)
                if location is None:
                    return {'message':'alamat kurang yakin'} ,404, { 'Content-Type': 'application/json' }
                else:
                    print(location.address)
                    print((location.latitude, location.longitude))
                    lat = location.latitude
                    lon = location.longitude
                    print(location.raw)
                    qry_client.address = alamat
                    qry_client.lat = lat
                    qry_client.lon = lon
            
            qry_user.username = args['username']
            qry_user.password = args['password']
            qry_client.nama = args['nama']
            qry_client.phone = args['phone']
            qry_client.image = args['image']
            qry_client.tgl_lahir = args['tgl_lahir']
            qry_client.gender = args['gender']
            qry_client.tingkat = args['tingkat']
            qry_client.gender_tentor = args['gender_tentor']
            qry_client.ortu = args['ortu']
            db.session.commit()
            return {"status":"OK", "message":"Updated", "data user":marshal(qry_user, User.respon_fields), "data client":marshal(qry_client, Clients.respon_fields)}, 200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self):
        id = get_jwt_claims()['id']
        qry_user = User.query.get(id)
        qry_client = Clients.query.filter_by(user_id=id).first()
        if qry_user is not None:
            qry_user.tipe = "unavailable"
            db.session.commit()
            return {"status":"OK", "message":"Deleted", "data user":marshal(qry_user, User.respon_fields), "data client":marshal(qry_client, Clients.respon_fields)}, 200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(ClientResource, '','/<int:id>')