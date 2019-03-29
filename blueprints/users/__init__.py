import random, logging
from blueprints import db
from flask_restful import fields

#Client CLASS

class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    status = db.Column(db.String(20))# String[panjang string, default 255],nullable boleh kosong
    email = db.Column(db.String(250))
    alamat = db.Column(db.String(250))
    contact = db.Column(db.String(30))


    respon_fields = {
        'user_id': fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.String,
        'email' : fields.String,
        'alamat' : fields.String,
        'contact' : fields.String
    }
    respon_token = {
        'user_id': fields.Integer,
        'status' : fields.String
    }

    def __init__(self,user_id,username,password,status,email,alamat,contact):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.status = status 
        self.email = email 
        self.alamat = alamat 
        self.contact = contact 

    
    #return repr harus string
    def __repr__(self):
        return '<Users %r>' % self.user_id
