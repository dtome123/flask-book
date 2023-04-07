from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'JHGHJGHT&^&*%&^*%&*%^&$^&RFHJGVHJVGHJFGHFGH'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:abc123456@localhost:3306/book_store?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)
login = LoginManager(app=app)
Session(app)
