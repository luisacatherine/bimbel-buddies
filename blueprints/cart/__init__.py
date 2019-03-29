import random, logging
from blueprints import db
from flask_restful import fields

#Items CLASS
class Transactions(db.Model): 
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    customer_id = db.Column(db.Integer)
    status = db.Column(db.String(200))
    total_qty = db.Column(db.Integer)
    total_harga = db.Column(db.Integer)
    paid_method = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    respon_fields = {
        'id': fields.Integer,
        'customer_id' : fields.Integer,
        'status' : fields.String,
        'total_qty' : fields.Integer,
        'total_harga' : fields.Integer,
        'paid_method' : fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime

    }

    def __init__(self,id,customer_id,status,total_qty,total_harga,paid_method,created_at,updated_at):
        self.id = id 
        self.customer_id = customer_id
        self.status = status
        self.total_qty = total_qty
        self.total_harga = total_harga
        self.paid_method = paid_method
        self.created_at = created_at 
        self.updated_at = updated_at 

    #return repr harus string
    def __repr__(self):
        return '<Transactions %r>' % self.id
    