import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app import db


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    user_role = Column(String(20), default='USER')


class BookReceipt(db.Model):
    __tablename__ = 'book_receipt'
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"), primary_key=True)
    quantity = Column(Integer)

    # book = relationship('Book',back_populates="receipts")
    # receipt = relationship('Receipt',back_populates="books")


class Book (db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    quantity = Column(Integer, default=0)
    author = Column(String(100))

    receipts = relationship(
        'Receipt', secondary='book_receipt', back_populates="books")


class Receipt(db.Model):
    __tablename__ = 'receipts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    books = relationship('Book', secondary='book_receipt',
                         back_populates="receipts")
