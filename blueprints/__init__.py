# app.py
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from time import strftime 
from datetime import timedelta
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from flask_cors import CORS

#request.status.code
app = Flask(__name__)
CORS(app)
# @app.route('/')
# def index():
#     return render_template('index.html')
# ini masih database di local
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://azril:Azril_28081995@172.11.111.18/rest_portofolio'
# server
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://azril:azril28081995@172.31.20.239/rest_portofolio'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

app.config['JWT_SECRET_KEY'] = 'alterra'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db',MigrateCommand)

@app.after_request
def after_request(response):
    if request.method=='GET':
        app.logger.warning("REQUEST_LOG\t%s %s", json.dumps({ 'request': request.args.to_dict(), 'response': json.loads(response.data.decode('utf-8')) }),request.method)
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({ 'request': request.get_json(), 'response': json.loads(response.data.decode('utf-8')) }))
    return response

# initiate flask-restful instance
api = Api(app, catch_all_404s=True)

    # db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    # entries = cur.fetchall()
@app.route('/')    
def index():
    return "<h1> Hello : This main route </h1>"

#from namafolder blueprints.namafolder resources.file.py resources

from blueprints.Client.resources import bp_clieent
app.register_blueprint(bp_clieent, url_prefix='/client')

from blueprints.tentor.resources import bp_tentor
app.register_blueprint(bp_tentor, url_prefix='/tentor')

from blueprints.auth import bp_auth
app.register_blueprint(bp_auth, url_prefix='/login')

from blueprints.users.resources import bp_admin
app.register_blueprint(bp_admin, url_prefix='/api/users')

db.create_all()
