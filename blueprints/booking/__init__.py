from blueprints import db
from flask_restful import fields
import datetime
from blueprints.Client import *
from blueprints.tentor import *
from blueprints.harga import *
from blueprints.Payment import *
from blueprints.jadwal_tentor import *

class Booking(db.Model):
    __tablename__ = "booking"
    id_booking = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    id_murid = db.Column(db.Integer, nullable=False)
    id_tentor = db.Column(db.Integer)
    jenis = db.Column(db.String(10), nullable=False)
    tanggal = db.Column(db.DateTime)
    mapel = db.Column(db.String(50))
    status = db.Column(db.String(10), nullable=False)
    harga_booking = db.Column(db.Integer)
    harga_bensin = db.Column(db.Integer)
    saldo_tentor = db.Column(db.Integer)
    saldo_admin = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    response_fields = {
        'id_booking': fields.Integer,
        'id_murid': fields.Integer,
        'id_tentor': fields.Integer,
        'jenis': fields.String,
        'tanggal': fields.DateTime,
        'mapel': fields.String,
        'status': fields.String,
        'harga_booking': fields.Integer,
        'harga_bensin': fields.Integer,
        'saldo_tentor': fields.Integer,
        'saldo_admin': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    tentor_fields = {
        'id_booking': fields.Integer,
        'id_murid': fields.Integer,
        'id_tentor': fields.Integer,
        'jenis': fields.String,
        'tanggal': fields.DateTime,
        'mapel': fields.String,
        'status': fields.String,
        'harga_booking': fields.Integer,
        'harga_bensin': fields.Integer,
        'saldo_tentor': fields.Integer,
        'saldo_admin': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    murid_fields = {
        'id_booking': fields.Integer,
        'id_murid': fields.Integer,
        'id_tentor': fields.Integer,
        'jenis': fields.String,
        'tanggal': fields.DateTime,
        'mapel': fields.String,
        'status': fields.String,
        'harga_booking': fields.Integer,
        'harga_bensin': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, id_booking, id_murid, id_tentor, jenis, tanggal, mapel, status, harga_booking, harga_bensin, saldo_tentor, saldo_admin, created_at, updated_at):
        self.id_booking = id_booking
        self.id_murid = id_murid
        self.id_tentor = id_tentor
        self.jenis = jenis
        self.tanggal = tanggal
        self.mapel = mapel
        self.status = status
        self.harga_booking = harga_booking
        self.harga_bensin = harga_bensin
        self.saldo_tentor = saldo_tentor
        self.saldo_admin = saldo_admin
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Items %r>' % self.id_booking # harus string