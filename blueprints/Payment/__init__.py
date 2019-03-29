import random, logging
from blueprints import db
from flask_restful import fields
import datetime

class Payments(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    id_booking = db.Column(db.Integer)
    nominal = db.Column(db.Integer)
    total_nominal = db.Column(db.Integer)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    respon_fields = {
        'id': fields.Integer,
        'id_booking' : fields.Integer,
        'nominal' : fields.Integer,
        'total_nominal' : fields.Integer,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }
    respon_token = {
        'id': fields.Integer,
        'tipe' : fields.String
    }

    def __init__(self,id,id_booking,nominal,total_nominal,created_at,updated_at):
        self.id = id
        self.id_booking = id_booking
        self.nominal = nominal
        self.total_nominal = total_nominal
        self.created_at = created_at
        self.updated_at = updated_at
    
    #return repr harus string
    def __repr__(self):
        return '<Payments %r>' % self.id
