import random, logging
from blueprints import db
from flask_restful import fields

#Client CLASS

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    tipe = db.Column(db.String(30))# String[panjang string, default 255],nullable boleh kosong

    respon_fields = {
        'id': fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'tipe' : fields.String
    }
    respon_token = {
        'id': fields.Integer,
        'tipe' : fields.String
    }

    def __init__(self,id,username,password,tipe):
        self.id = id
        self.username = username
        self.password = password
        self.tipe = tipe 
    
    #return repr harus string
    def __repr__(self):
        return '<User %r>' % self.id
