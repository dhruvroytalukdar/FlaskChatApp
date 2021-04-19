from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '5646addsknc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b54626acf43cea:d298619a@us-cdbr-east-03.cleardb.com/heroku_f4837d222bcfda3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
migrate = Migrate()


db = SQLAlchemy(app)
migrate.init_app(app,db)
socketio = SocketIO(app, cors_allowed_origins="*")

from app import routes