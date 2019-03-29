import random, logging
from blueprints import db
from flask_restful import fields
from ..book import * 
from ..user import *

#Rent CLASS
class Rents(db.Model): 
    __tablename__ = "rent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    return_date = db.Column(db.String(200))# String[panjang string, default 255],nullable boleh kosong
    post_by = db.Column(db.Integer)

    respon_fields = {
        'id': fields.Integer,
        'book_id' : fields.Integer,
        'user_id' : fields.Integer,
        'return_date' : fields.String,
        'post_by' : fields.Integer
    }

    def __init__(self,id,book_id,user_id,return_date,post_by):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.return_date = return_date
        self.post_by = post_by 
    
    #return repr harus string
    def __repr__(self):
        return '<Rent %r>' % self.id
    