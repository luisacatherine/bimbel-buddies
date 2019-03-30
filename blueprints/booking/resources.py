import logging
import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from . import *
from sqlalchemy import Date, cast
from flask_jwt_extended import get_jwt_claims, jwt_required
from datetime import datetime, date, timedelta
import requests
from geopy.distance import great_circle

bp_booking = Blueprint('booking', __name__)
api = Api(bp_booking)

class BookingResource(Resource):

    def __init__(self):
        pass
    
    # @jwt_required
    def get(self, id_booking=None):
        # jwtClaims = get_jwt_claims()
        if (id_booking == None):
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('id_tentor', type=int, location='args')
            parser.add_argument('id_murid', type=int, location='args')
            parser.add_argument('tanggal', location='args')
            parser.add_argument('status', type=str, location='args', choices=['waiting', 'accepted', 'cancelled'])
            parser.add_argument('mapel', type=str, choices=['mat', 'fis', 'kim', 'bio'])
            args = parser.parse_args()
            offset = (args['p'] * args['rp']) - args['rp']
            qry = Booking.query

            if args['id_tentor'] is not None:
                qry = qry.filter_by(id_tentor=args['id_tentor'])

            if args['id_murid'] is not None:
                qry = qry.filter_by(id_murid=args['id_murid'])

            if args['status'] is not None:
                qry = qry.filter_by(status=args['status'])

            if args['mapel'] is not None:
                qry = qry.filter_by(mapel=args['mapel'])
            
            if args['tanggal'] is not None:
                qry = qry.filter(cast(Booking.tanggal, Date) == args['tanggal'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Booking.response_fields))
            
            return {'status': 'oke', 'booking': rows}, 200, {'Content-Type': 'application/json'}
        else:
            qry = Booking.query.get(id_booking)
            if qry is not None:
                return {'status': 'oke', 'booking': marshal(qry, Booking.response_fields)}, 200, {'Content-Type': 'application/json'}
            return {'status': 'NOT_FOUND', 'message': 'Booking not found'}, 404, {'Content-Type': 'application/json'}
    
    # @jwt_required
    def put(self, id_booking):
        # jwtClaims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('tanggal', location='json')
        parser.add_argument('mapel', type=str, choices=['mat', 'fis', 'kim', 'bio'])
        parser.add_argument('status', location='json', choices=['waiting', 'accepted', 'cancelled', 'done'])
        # parser.add_argument('id_tentor', location='json', type=int)
        args = parser.parse_args()
        qry = Booking.query.get(id_booking)

        if args['tanggal'] is not None:
            datetime_object = datetime.strptime(args['tanggal'], '%Y-%m-%d %H:%M')
            if datetime_object < datetime.now():
                return {'status': 'gagal', 'message': 'Tanggal sudah terlewat!'}
            elif datetime.now().date() > datetime_object.date() - timedelta(days=1):
                return {'status': 'gagal', 'message': 'Pemesanan paling lambat 1 hari sebelum tanggal les.'}
            elif datetime_object.date() > datetime.now().date() + timedelta(days=7):
                return {'status': 'gagal', 'message': 'Pemesanan hanya bisa dilakukan 7 hari sebelum tanggal les.'}
            qry.tanggal = args['tanggal']
        
        if args['mapel'] is not None:
            qry.mapel = args['mapel']
        
        if args['status'] is not None:
            if args['status'] == 'accepted':
                # Seleksi mentor by gender dan rating di react
                # qry.id_tentor = jwtClaims
                qry.id_tentor = 1
                # Hitung jarak antara tentor dan murid
                # jarak_tentor = great_circle(newport_ri, cleveland_oh).km
                jarak_tentor = 10
                # Tambahkan harga bensin
                qry.harga_bensin += 500 * jarak_tentor
                # Saldo murid dikurangi

            elif args['status'] == 'cancelled':
                # Saldo murid ditambah
                # Kalau masih j-6
                if datetime.now() + timedelta(hours=6) < qry.tanggal:
                    qry.harga_booking = 0
                # Kalau sudah mepet
                else:
                    qry.saldo_admin += 0.5 * qry.harga_booking
                    qry.harga_booking = 0
                    # Saldo tentor dikurangi 50% dan dipindah ke saldo admin
                    # qry.saldo_admin
            
            elif args['status'] == 'done':
                qry.saldo_tentor = 0.8 * qry.harga_booking + qry.harga_bensin
                qry.saldo_admin = 0.2 * qry.harga_booking
                qry.harga_booking = 0
                qry.harga_bensin = 0
            
            qry.status = args['status']
        db.session.commit()
        return {'status': 'oke', 'booking': marshal(qry, Booking.response_fields)}, 200, {'Content-Type': 'application/json'}
        
    # @jwt_required
    def post(self):
        # jwtClaims = get_jwt_claims()
        # id_murid = jwtClaims['id']
        id_murid = 1
        parser = reqparse.RequestParser()
        parser.add_argument('jenis', location='json', choices=['rutin', 'insidentil'], required=True)
        parser.add_argument('tanggal', location='json', required=True)
        parser.add_argument('mapel', type=str, choices=['mat', 'fis', 'kim', 'bio'], required=True)
        args = parser.parse_args()
        datetime_object = datetime.strptime(args['tanggal'], '%Y-%m-%d %H:%M')
        if datetime_object < datetime.now():
            return {'status': 'gagal', 'message': 'Tanggal sudah terlewat!'}
        elif datetime.now().date() > datetime_object.date() - timedelta(days=1):
            return {'status': 'gagal', 'message': 'Pemesanan paling lambat 1 hari sebelum tanggal les.'}
        elif datetime_object.date() > datetime.now().date() + timedelta(days=7):
            return {'status': 'gagal', 'message': 'Pemesanan hanya bisa dilakukan 7 hari sebelum tanggal les.'}
        # Cek tingkat user
        harga_booking = Harga.query.filter(Harga.tingkat == 'SMA').first().harga
        args['created_at'] = datetime.now()
        args['updated_at'] = datetime.now()
        booking = Booking(None, id_murid, 0, args['jenis'], args['tanggal'], args['mapel'], 'waiting', harga_booking, 0, 0, 0, args['created_at'], args['updated_at'])
        db.session.add(booking)
        db.session.commit()
        return {'status': 'oke', 'booking': marshal(booking, Booking.response_fields)}, 200, {'Content-Type': 'application/json'}

api.add_resource(BookingResource, '/<int:id_booking>', '')