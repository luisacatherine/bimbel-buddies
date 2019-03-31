import random, logging
from blueprints import db
from flask_restful import fields
from blueprints.user import *
from blueprints.Client import *
from blueprints.tentor import *

class Blocked(db.Model): 
    __tablename__ = "blocked"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    client_id = db.Column(db.Integer)
    blocked_tentor = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    response_fields = {
        'id': fields.Integer,
        'client_id' : fields.Integer,
        'blocked_tentor' : fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, id, client_id, blocked_tentor, created_at, updated_at):
        self.id = id
        self.client_id = client_id
        self.blocked_tentor = blocked_tentor
        self.created_at = created_at
        self.updated_at = updated_at
    
    #return repr harus string
    def __repr__(self):
        return '<Blocked %r>' % self.id
    