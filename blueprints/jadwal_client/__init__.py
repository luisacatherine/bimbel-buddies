import random, logging
from blueprints import db
from flask_restful import fields

class Jadwalclient(db.Model): 
    __tablename__ = "jadwalclient"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    client_id = db.Column(db.Integer)
    tentor_id = db.Column(db.Integer)
    booking_id = db.Column(db.Integer, unique=True)
    schedule_start = db.Column(db.DateTime)
    schedule_end = db.Column(db.DateTime)
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    response_fields = {
        'id': fields.Integer,
        'client_id' : fields.Integer,
        'tentor_id' : fields.Integer,
        'booking_id' : fields.Integer,
        'schedule_start' : fields.DateTime,
        'schedule_end' : fields.DateTime,
        'status' : fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, id, client_id, tentor_id, booking_id, schedule_start, schedule_end, status, created_at, updated_at):
        self.id = id
        self.client_id = client_id
        self.tentor_id = tentor_id
        self.booking_id = booking_id
        self.schedule_start = schedule_start
        self.schedule_end = schedule_end
        self.status = status 
        self.created_at = created_at
        self.updated_at = updated_at
    
    #return repr harus string
    def __repr__(self):
        return '<Jadwalclient %r>' % self.id
    