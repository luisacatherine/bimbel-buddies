import random, logging
from blueprints import db
from flask_restful import fields
import datetime

#Client CLASS

class Tentors(db.Model):
    __tablename__ = "tentors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer)
    nama = db.Column(db.String(100))
    address = db.Column(db.Text)
    ktp = db.Column(db.String(16))#KTP tidak lebih 16 angka
    phone = db.Column(db.String(30))
    image = db.Column(db.Text)
    tgl_lahir = db.Column(db.DateTime)
    gender = db.Column(db.String(20))
    fokus = db.Column(db.String(20))
    tingkat = db.Column(db.String(20))
    pendidikan = db.Column(db.String(20))
    ket = db.Column(db.String(30))
    # tipe = db.Column(db.String(30))# String[panjang string, default 255],nullable boleh kosong
    rekening = db.Column(db.String(30))
    pemilik_nasabah = db.Column(db.String(100))
    available = db.Column(db.String(30))
    range_jam = db.Column(db.String(30))
    saldo = db.Column(db.Integer)
    rating = db.Column(db.Float)
    qty_rating = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    respon_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'nama' : fields.String,
        'address' : fields.String,
        'ktp' : fields.String,
        'phone' : fields.String,
        'image' : fields.String,
        'tgl_lahir' : fields.DateTime,
        'gender' : fields.String,
        'fokus' : fields.String,
        'tingkat' : fields.String,
        'pendidikan' : fields.String,
        'ket' : fields.String,
        'rekening' : fields.String,
        'pemilik_nasabah' : fields.String,
        'available' : fields.String,
        'range_jam' : fields.String,
        'saldo': fields.Integer,
        'rating' : fields.Float,
        'qty_rating': fields.Integer,
        'lat' : fields.Float,
        'lon' : fields.Float,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self,id,user_id,nama,address,ktp,phone,image,tgl_lahir,gender,fokus,tingkat,
        pendidikan,ket,rekening,pemilik_nasabah,available,range_jam,saldo,rating,qty_rating,lat,
        lon,status,created_at,updated_at):
        self.id = id
        self.user_id = user_id
        self.nama = nama
        self.address = address
        self.ktp = ktp
        self.phone = phone
        self.image = image
        self.tgl_lahir = tgl_lahir
        self.gender = gender
        self.fokus = fokus
        self.tingkat = tingkat
        self.pendidikan = pendidikan
        self.ket = ket
        self.rekening = rekening
        self.pemilik_nasabah = pemilik_nasabah
        self.available = available
        self.range_jam = range_jam
        self.saldo = saldo
        self.rating = rating
        self.qty_rating = qty_rating
        self.lat = lat
        self.lon = lon
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
    
    #return repr harus string
    def __repr__(self):
        return '<Tentors %r>' % self.id
