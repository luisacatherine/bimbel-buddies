import random, logging
from blueprints import db
from flask_restful import fields
import datetime
from blueprints.booking import *

class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    id_murid = db.Column(db.Integer)
    id_tentor = db.Column(db.Integer)
    id_booking = db.Column(db.Integer, unique=True)
    rating = db.Column(db.Integer) # 1 sampai 5
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    respon_fields = {
        'id': fields.Integer,
        'id_murid' : fields.Integer,
        'id_tentor' : fields.Integer,
        'id_booking' : fields.Integer,
        'rating' : fields.Integer,
        'deskripsi' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }
    respon_token = {
        'id': fields.Integer,
        'tipe' : fields.String
    }

    def __init__(self, id, id_murid, id_tentor, id_booking, rating, deskripsi, created_at, updated_at):
        self.id = id
        self.id_murid = id_murid
        self.id_tentor = id_tentor
        self.id_booking = id_booking
        self.rating = rating
        self.deskripsi = deskripsi
        self.created_at = created_at
        self.updated_at = updated_at
    
    #return repr harus string
    def __repr__(self):
        return '<Reviews %r>' % self.id
