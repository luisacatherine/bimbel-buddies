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
        parser.add_argument('phone', location='json', required=True),
        parser.add_argument('image', location='json'),
        parser.add_argument('tgl_lahir', location='json', required=True),
        parser.add_argument('gender', location='json', required=True),
        parser.add_argument('tingkat', location='json', required=True)
        args = parser.parse_args()#sudah jadi dictionary

        qry_user = User.query.filter_by(username=args['username']).first()
        if qry_user is not None:
            return {'message':'username is already used'} ,404, { 'Content-Type': 'application/json' }
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
        alamat = args["jalan"] + " " + args["kota"]
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + alamat + "&key=AIzaSyAC0QSYGS_Ii3d0mdCjdIOXN9u0nQmYQyg")
        location = response.json()
        if location is None:
            return {'message':'alamat kurang yakin'} ,404, { 'Content-Type': 'application/json' }
        lat = location['results'][0]['geometry']['location']['lat']
        lon = location['results'][0]['geometry']['location']['lng']
        user = User(None,args['username'],password,tipe)
        db.session.add(user)
        db.session.commit()
        client = Clients(None,user.id,args['nama'],alamat,args['phone'],args['image'],
        args['tgl_lahir'],args['gender'],args['tingkat'],saldo,lat,lon,created_at,updated_at)
        db.session.add(client)
        db.session.commit()

        return {"status": "OK", "data_user": marshal(user, User.respon_fields), "data_client": marshal(client, Clients.respon_fields)},200, { 'Content-Type': 'application/json' }

    @jwt_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location='args', default=1)
        parser.add_argument('rp', location='args', default=5)
        args = parser.parse_args()
        jwtClaims = get_jwt_claims()
        if (id == None):
            if jwtClaims['tipe'] == 'client':
                id = get_jwt_claims()['id']
                qry_user = User.query.get(id)
                qry_client = Clients.query.filter_by(user_id=id).first()
                if qry_user is not None and qry_client is not None:
                    return {"status": "OK", "data_user": marshal(qry_user, User.respon_fields), "data_client": marshal(qry_client, Clients.respon_fields)},200, { 'Content-Type': 'application/json' }
                return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }
            else:
                offset = (args['p'] * args['rp']) - args['rp']
                qry = Clients.query
                rows = []
                for row in qry.limit(args['rp']).offset(offset).all():
                    temp = marshal(row, Clients.respon_fields)
                    user = User.query.get(row.user_id)
                    temp['user'] = marshal(user, User.respon_fields)
                    rows.append(temp)            
                return {'status': 'oke', 'clients': rows}, 200, {'Content-Type': 'application/json'}     
        else:
            if jwtClaims['tipe'] == 'client':
                id = get_jwt_claims()['id']
                qry_user = User.query.get(id)
                qry_client = Clients.query.filter_by(user_id=id).first()
                if qry_user is not None and qry_client is not None:
                    return {"status": "OK", "data_user": marshal(qry_user, User.respon_fields), "data_client": marshal(qry_client, Clients.respon_fields)},200, { 'Content-Type': 'application/json' }
                return {'status': 'NOT_FOUND','message':'user not found'}, 404, { 'Content-Type': 'application/json' }
            else:
                qry_client = Clients.query.get(id)
                qry_user = User.query.get(qry_client.user_id)
                if qry_user is not None and qry_client is not None:
                    return {"status": "OK", "data_user": marshal(qry_user, User.respon_fields), "data_client": marshal(qry_client, Clients.respon_fields)},200, { 'Content-Type': 'application/json' }
                return {'status': 'NOT_FOUND','message':'user not found'}, 404, { 'Content-Type': 'application/json' }
    
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
            return {"status":"OK", "message":"Updated", "data_user":marshal(qry_user, User.respon_fields), "data_client":marshal(qry_client, Clients.respon_fields)}, 200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self):
        id = get_jwt_claims()['id']
        qry_user = User.query.get(id)
        qry_client = Clients.query.filter_by(user_id=id).first()
        if qry_user is not None:
            qry_user.tipe = "unavailable"
            db.session.commit()
            return {"status":"OK", "message":"Deleted", "data_user":marshal(qry_user, User.respon_fields), "data_client":marshal(qry_client, Clients.respon_fields)}, 200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'user not found'},404, { 'Content-Type': 'application/json' }

    def patch(self):
        return 'Not yet implement', 501


api.add_resource(ClientResource, '','/<int:id>')