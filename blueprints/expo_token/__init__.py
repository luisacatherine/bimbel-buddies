from blueprints import db
from flask_restful import fields
import datetime

class Token(db.Model):
    __tablename__ = "token"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, unique=True)
    expo_token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'expo_token': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, id, user_id, expo_token, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.expo_token = expo_token
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Token %r>' % self.id # harus string