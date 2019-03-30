import random, logging
from blueprints import db
from flask_restful import fields
import datetime


class Topups(db.Model):
    __tablename__ = "topups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    id_murid = db.Column(db.Integer)
    nominal = db.Column(db.Integer)
    metode_pembayaran = db.Column(db.String(50)) # Bank / Indo / Alfa / Kantor Pos
    status = db.Column(db.String(50)) # Sukses / Wait payment
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    respon_fields = {
        'id': fields.Integer,
        'id_murid' : fields.Integer,
        'nominal' : fields.Integer,
        'metode_pembayaran' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }
    respon_token = {
        'id': fields.Integer,
        'tipe' : fields.String
    }

    def __init__(self,id,id_murid,nominal,metode_pembayaran,status,created_at,updated_at):
        self.id = id
        self.id_murid = id_murid
        self.nominal = nominal
        self.metode_pembayaran = metode_pembayaran
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
    
    #return repr harus string
    def __repr__(self):
        return '<Topups %r>' % self.id
