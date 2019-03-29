import random, logging
from blueprints import db
from flask_restful import fields
import datetime

#Client CLASS

class Clients(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    nama = db.Column(db.String(100))
    address = db.Column(bd.Text)
    phone = db.Column(db.String(30))
    image = db.Column(bd.Text)
    tgl_lahir = db.Column(db.DateTime)
    gender = db.Column(db.String(20))
    tingkat = db.Column(db.String(20))
    gender_tentor = db.Column(db.String(20))
    ortu = db.Column(db.String(100))
    saldo = db.Column(db.Integer)
    tipe = db.Column(db.String(30))# String[panjang string, default 255],nullable boleh kosong
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    respon_fields = {
        'id': fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'nama' : fields.String,
        'address' : fields.Text,
        'phone' : fields.String,
        'image' : fields.Text,
        'tgl_lahir' : fields.DateTime,
        'gender' : fields.String,
        'tingkat' : fields.String,
        'gender_tentor' : fields.String,
        'ortu' : fields.String,
        'saldo': fields.Integer,
        'tipe' : fields.String,
        'lat' : fields.Float,
        'lon' : fields.Float,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }
    respon_token = {
        'id': fields.Integer,
        'tipe' : fields.String
    }

    def __init__(self,id,username,password,nama,address,phone,image,tgl_lahir,gender,tingkat,
        gender_tentor,ortu,saldo,tipe,lat,lon,created_at,updated_at):
        self.id = id
        self.username = username
        self.password = password
        self.nama = nama
        self.address = address
        self.phone = phone
        self.image = image
        self.tgl_lahir = tgl_lahir
        self.gender = gender
        self.tingkat = tingkat
        self.gender_tentor = gender_tentor
        self.ortu = ortu
        self.saldo = saldo
        self.tipe = tipe
        self.lat = lat
        self.lon = lon
        self.created_at = created_at
        self.updated_at = updated_at
    
    #return repr harus string
    def __repr__(self):
        return '<Clients %r>' % self.id
