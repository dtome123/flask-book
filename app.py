from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'JHGHJGHT&^&*%&^*%&*%^&$^&RFHJGVHJVGHJFGHFGH'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12346@localhost:3307/book_store?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["SESSION_PERMANENT"] = False

db = SQLAlchemy(app)

Session(app)
