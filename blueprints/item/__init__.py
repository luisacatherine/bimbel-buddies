import random, logging
from blueprints import db
from flask_restful import fields

#Items CLASS
class Items(db.Model): 
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    nama = db.Column(db.String(200))
    merek = db.Column(db.String(200))
    kategori = db.Column(db.String(200))
    detail = db.Column(db.String(500))
    harga = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    url_picture = db.Column(db.String(200))
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    respon_fields = {
        'id': fields.Integer,
        'nama' : fields.String,
        'merek' : fields.String,
        'kategori' : fields.String,
        'detail' : fields.String,
        'harga' : fields.Integer,
        'stock' : fields.Integer,
        'url_picture' : fields.String,
        'user_id' : fields.Integer,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime

    }

    def __init__(self,id,nama,merek,kategori,detail,harga,stock,url_picture,user_id,created_at,updated_at):
        self.id = id
        self.nama = nama
        self.merek = merek
        self.kategori = kategori
        self.detail = detail
        self.harga = harga
        self.stock = stock 
        self.url_picture = url_picture 
        self.user_id = user_id 
        self.created_at = created_at 
        self.updated_at = updated_at 

    #return repr harus string
    def __repr__(self):
        return '<Item %r>' % self.id
    