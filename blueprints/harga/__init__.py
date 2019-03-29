from blueprints import db
from flask_restful import fields
import datetime

class Harga(db.Model):
    __tablename__ = "harga"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    tingkat = db.Column(db.String(5), nullable=False)
    harga = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    response_fields = {
        'id': fields.Integer,
        'tingkat': fields.String,
        'harga': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, id, tingkat, harga, created_at, updated_at):
        self.id = id
        self.tingkat = tingkat
        self.harga = harga
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Harga %r>' % self.id # harus string