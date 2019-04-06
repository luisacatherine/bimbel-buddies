import logging, requests, re
import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from . import *
from blueprints.jadwal_client import *
from sqlalchemy import Date, cast
from flask_jwt_extended import get_jwt_claims, jwt_required
from datetime import datetime, date, timedelta
import requests
from geopy.distance import great_circle, geodesic

bp_booking = Blueprint('booking', __name__)
api = Api(bp_booking)

class BookingResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self, id_booking=None):
        jwtClaims = get_jwt_claims()
        if (id_booking == None):
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=100)
            parser.add_argument('id_tentor', type=int, location='args')
            parser.add_argument('id_murid', type=int, location='args')
            parser.add_argument('tanggal', location='args')
            parser.add_argument('status', type=str, location='args', choices=['waiting', 'requested', 'accepted', 'cancelled', 'not_accepted', 'done'])
            parser.add_argument('mapel', type=str, choices=['mat', 'fis', 'kim', 'bio'])
            args = parser.parse_args()
            offset = (args['p'] * args['rp']) - args['rp']
            qry = Booking.query
            
            check_exp = Booking.query.filter_by(status="requested").all()
            for check_exp in check_exp:
                if (datetime.now()  > check_exp.updated_at + timedelta(hours=1)):
                    print("---- requested jadi waiting ----",check_exp.updated_at)
                    check_exp.status = "waiting"
                    check_exp.updated_at= datetime.now()
                    db.session.commit()

            check_exp = Booking.query.filter_by(status="waiting").all()
            for check_exp in check_exp:
                if (datetime.now() + timedelta(hours=12) > check_exp.tanggal):
                    print("---- check exp ----",check_exp.tanggal)
                    check_exp.status = "expired"
                    check_exp.updated_at= datetime.now()
                    db.session.commit()

            if jwtClaims['tipe'] == 'tentor':
                tentor = Tentors.query.filter(Tentors.user_id == jwtClaims['id']).first()
                qry = qry.filter_by(id_tentor=tentor.id)
            
            if jwtClaims['tipe'] == 'client':
                client = Clients.query.filter(Clients.user_id == jwtClaims['id']).first()
                qry = qry.filter_by(id_murid=client.id)

            if args['id_tentor'] is not None:
                qry = qry.filter_by(id_tentor=args['id_tentor'])

            if args['id_murid'] is not None:
                qry = qry.filter_by(id_murid=args['id_murid'])

            if args['status'] is not None:
                qry = qry.filter_by(status=args['status'])

            if args['mapel'] is not None:
                qry = qry.filter_by(mapel=args['mapel'])
            
            if args['tanggal'] is not None:
                # qry = qry.filter_by(tanggal=args['tanggal'])
                qry = qry.filter(cast(Booking.tanggal, Date) == args['tanggal'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                temp = marshal(row, Booking.response_fields)
                tentor = Tentors.query.filter(Tentors.id == row.id_tentor).first()
                murid = Clients.query.filter(Clients.id == row.id_murid).first()
                temp['tentor'] = marshal(tentor, Tentors.respon_fields)
                temp['murid'] = marshal(murid, Clients.respon_fields)
                rows.append(temp)            
            return {'status': 'oke', 'booking': rows}, 200, {'Content-Type': 'application/json'}
        else:
            qry = Booking.query.get(id_booking)
            if qry is None:
                return {'status': 'NOT_FOUND', 'message': 'Booking not found'}, 404, {'Content-Type': 'application/json'}
            if jwtClaims['tipe'] == 'tentor':
                tentor = Tentors.query.filter(Tentors.user_id == jwtClaims['id']).first()
                if qry.id_tentor != tentor.id:
                    return {'status': 'UNAUTHORIZED'}, 401, {'Content-Type': 'application/json'}
            elif jwtClaims['tipe'] == 'client':
                client = Clients.query.filter(Clients.user_id == jwtClaims['id']).first()
                if qry.id_murid != client.id:
                    return {'status': 'UNAUTHORIZED'}, 401, {'Content-Type': 'application/json'}
            temp = marshal(qry, Booking.response_fields)
            tentor = Tentors.query.filter(Tentors.id == qry.id_tentor).first()
            murid = Clients.query.filter(Clients.id == qry.id_murid).first()
            temp['tentor'] = marshal(tentor, Tentors.respon_fields)
            temp['murid'] = marshal(murid, Clients.respon_fields)
            return {'status': 'oke', 'booking': temp}, 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def put(self, id_booking):
        jwtClaims = get_jwt_claims()
        if jwtClaims['tipe'] == 'client':
            qry_murid = Clients.query.filter(Clients.user_id == jwtClaims['id']).first()
        elif jwtClaims['tipe'] == 'tentor':
            qry_tentor = Tentors.query.filter(Tentors.user_id == jwtClaims['id']).first()
        parser = reqparse.RequestParser()
        parser.add_argument('tanggal', location='json')
        parser.add_argument('id_tentor', location='json', type=int)
        parser.add_argument('mapel', type=str, choices=['mat', 'fis', 'kim', 'bio'])
        parser.add_argument('status', location='json', choices=['waiting', 'requested', 'accepted', 'cancelled', 'done', 'not_accepted'])
        args = parser.parse_args()
        qry = Booking.query.get(id_booking)
        

        if args['tanggal'] is not None:
            if jwtClaims['tipe'] != 'client' and qry.id_murid != qry_murid.id:
                return {'status': 'UNAUTHORIZED'}, 401, {'Content-Type': 'application/json'}
            datetime_object = datetime.strptime(args['tanggal'], '%Y-%m-%d %H:%M')
            if datetime_object < datetime.now():
                return {'status': 'gagal', 'message': 'Tanggal sudah terlewat!'}
            elif datetime.now().date() > datetime_object.date() - timedelta(days=1):
                return {'status': 'gagal', 'message': 'Pemesanan paling lambat 1 hari sebelum tanggal les.'}
            elif datetime_object.date() > datetime.now().date() + timedelta(days=7):
                return {'status': 'gagal', 'message': 'Pemesanan hanya bisa dilakukan 7 hari sebelum tanggal les.'}
            qry.tanggal = args['tanggal']
            qry.status = 'waiting'

            # Delete jadwal tentor
            qry_jadwal = Jadwaltentor.query.filter(Jadwaltentor.booking_id == id_booking).first()
            db.session.delete(qry_jadwal)
            jadwal_client =Jadwalclient.query.filter(Jadwaltentor.booking_id == id_booking).first()
            db.session.delete(jadwal_client)
            db.session.commit()


        if args['mapel'] is not None:
            qry.mapel = args['mapel']
        
        if args['status'] is not None:
            if jwtClaims['tipe'] == 'tentor':
                tentor = Tentors.query.filter(Tentors.user_id == jwtClaims['id']).first()
            if jwtClaims['tipe'] == 'client':
                tentor = Tentors.query.filter(Tentors.id == args['id_tentor']).first()
            murid = Clients.query.filter(Clients.id == qry.id_murid).first()

            if args['status'] == 'requested':
                qry.id_tentor = args['id_tentor']

            elif args['status'] == 'waiting':
                qry.id_tentor = 0

            elif args['status'] == 'not_accepted':
                qry.id_tentor = 0
                args['status'] = 'waiting'

            elif args['status'] == 'accepted':
                # Seleksi mentor by gender dan rating di react
                qry.id_tentor = tentor.id

                # Hitung jarak antara tentor dan murid
                resp = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + tentor.address + "&destinations=" + murid.address + "&key=AIzaSyAC0QSYGS_Ii3d0mdCjdIOXN9u0nQmYQyg")
                resp = resp.json()
                jarak = resp['rows'][0]['elements'][0]['distance']['text']
                angka = re.findall(r'([1-9]|\.)', jarak)
                angka = float(''.join(angka))
                satuan = re.findall(r'([a-z])', jarak)
                satuan = ''.join(satuan)
                if satuan == 'mi':
                    angka = angka * 1609 / 1000
                if satuan == 'ft':
                    angka = angka * 3048 / 10000
                jarak_tentor = angka
                # Tambahkan harga bensin
                qry.harga_bensin += 700 * jarak_tentor
                murid.saldo -= (qry.harga_bensin + qry.harga_booking)
                qry.saldo_admin += (qry.harga_bensin + qry.harga_booking)

                # Tambah jadwal tentor
                # new_schedule = Jadwaltentor(None, murid.id, tentor.id, qry.id_booking, qry.tanggal, qry.tanggal + timedelta(hours=1.5), 'waiting', datetime.now(), datetime.now())
                # db.session.add(new_schedule)
                # qry.status = args['status']
                # db.session.commit()
                # temp=marshal(qry, Booking.response_fields)
                # temp["jarak"]=jarak_tentor
                # return {'status': 'oke', 'booking': temp}, 200, {'Content-Type': 'application/json'}
            elif args['status'] == 'cancelled':
                qry_tentor = Jadwaltentor.query.filter(Jadwaltentor.booking_id == id_booking).first()
                db.session.delete(qry_tentor)
                db.session.commit()

                qry_client = Jadwalclient.query.filter(Jadwalclient.booking_id == id_booking).first()
                db.session.delete(qry_client)
                db.session.commit()

                # Kalau masih j-6
                if datetime.now() + timedelta(hours=6) < qry.tanggal:
                    if qr.status == 'requested':
                        murid.saldo += (qry.harga_booking + qry.harga_bensin)
                        qry.saldo_admin = 0
                        qry.harga_booking = 0
                        qry.harga_bensin = 0
                    
                    elif qr.status == 'accepted':
                        murid.saldo += (qry.harga_booking + qry.harga_bensin)
                        qry.saldo_admin -= (qry.harga_booking + qry.harga_bensin)
                        qry.harga_booking = 0
                        qry.harga_bensin = 0

                # Kalau sudah mepet
                else:
                    if jwtClaims['tipe'] == 'tentor':
                        murid.saldo += (qry.harga_booking + qry.harga_bensin)
                        qry.saldo_tentor -= 0.5 * qry.harga_booking
                        tentor.saldo += qry.saldo_tentor
                        qry.saldo_admin -= (0.5 * qry.harga_booking + qry.harga_bensin)
                        qry.harga_booking = 0
                        qry.harga_bensin = 0

                    elif jwtClaims['tipe'] == 'client':
                        murid.saldo += (0.5 * qry.harga_booking + qry.harga_bensin)
                        qry.saldo_admin -= (0.5 * qry.harga_booking + qry.harga_bensin)
                        qry.harga_booking = 0
                        qry.harga_bensin = 0

            
            elif args['status'] == 'done':
                qry.saldo_tentor = 0.8 * qry.harga_booking + qry.harga_bensin
                # return qry.saldo_tentor
                tentor.saldo += qry.saldo_tentor
                qry.saldo_admin -= (0.8 * qry.harga_booking + qry.harga_bensin)
            qry.status = args['status']
        qry.updated_at= datetime.now()
            # return qry.id_tentor
        db.session.commit()
        return {'status': 'oke', 'booking': marshal(qry, Booking.response_fields)}, 200, {'Content-Type': 'application/json'}
        
    @jwt_required
    def post(self):
        jwtClaims = get_jwt_claims()
        murid = Clients.query.filter(Clients.user_id == jwtClaims['id']).first()
        
        id_murid = murid.id
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

        #Cek jadwal yang sama
        jadwal = Jadwalclient.query.filter_by(client_id=id_murid)
        jadwal = jadwal.filter_by(schedule_start=datetime_object).first()
        if jadwal is not None:
            return {'status': 'gagal', 'message': 'Pemesanan tidak bisa di waktu yang sama'}
        # Cek tingkat user
        harga_booking = Harga.query.filter(Harga.tingkat == murid.tingkat).first().harga
        if murid.saldo < (harga_booking + 3500):
            return {'status': 'gagal', 'message': 'Saldo Anda tidak mencukupi, silakan top up saldo terlebih dahulu'}
        args['created_at'] = datetime.now()
        args['updated_at'] = datetime.now()
        booking = Booking(None, id_murid, 0, args['jenis'], args['tanggal'], args['mapel'], 'waiting', harga_booking, 0, 0, 0, 0, args['created_at'], args['updated_at'])
        db.session.add(booking)
        db.session.commit()
        jadwal_client = Jadwalclient(None, id_murid, 0, booking.id_booking, datetime_object, datetime_object + timedelta(hours=1.5), 'waiting', datetime.now(), datetime.now())
        db.session.add(jadwal_client)
        db.session.commit()
        return {'status': 'oke', 'booking': marshal(booking, Booking.response_fields), 'murid': marshal(murid, Clients.respon_fields)}, 200, {'Content-Type': 'application/json'}

api.add_resource(BookingResource, '/<int:id_booking>', '')