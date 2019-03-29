import random, logging
from blueprints import db
from flask_restful import fields

#Items CLASS
class Cart(db.Model): 
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    transaction_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    nama_item = db.Column(db.String(200))
    url_picture = db.Column(db.String(200))
    qty = db.Column(db.Integer)
    harga = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    status = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    respon_fields = {
        'id': fields.Integer,
        'transaction_id' : fields.Integer,
        'item_id' : fields.Integer,
        'nama_item' : fields.String,
        'url_picture' : fields.String,
        'qty' : fields.Integer,
        'harga' : fields.Integer,
        'customer_id' : fields.Integer,
        'status' : fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime

    }

    def __init__(self,id,transaction_id,item_id,nama_item,url_picture,qty,harga,customer_id,status,created_at,updated_at):
        self.id = id 
        self.transaction_id = transaction_id
        self.item_id = item_id
        self.nama_item = nama_item 
        self.url_picture = url_picture
        self.qty = qty
        self.harga = harga
        self.customer_id = customer_id
        self.status =status
        self.created_at = created_at 
        self.updated_at = updated_at 

    #return repr harus string
    def __repr__(self):
        return '<Cart %r>' % self.id
    