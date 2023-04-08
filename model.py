from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import enum

from app import db


class OrderStatus(enum.Enum):
    PENDING = 0
    COMPLETED = 1


class OrderType(enum.Enum):
    ONLINE = 0
    OFFLINE = 1


class Customer(db.Model):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    phone = Column(String(20))
    address = Column(String(100))


class Staff(db.Model, UserMixin):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    phone = Column(String(20))
    address = Column(String(100))
    avatar = Column(String(100))


class Book (db.Model):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    quantity = Column(Integer, default=0)
    author = Column(String(100))


class InputBook_Book(db.Model):
    __tablename__ = 'input_book_book'
    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)
    input_book_id = Column(Integer, ForeignKey(
        "input_book.id"), primary_key=True)
    quantity = Column(Integer)

    book = relationship(Book)


class InputBook(db.Model):
    __tablename__ = 'input_book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey(Staff.id))
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now())

    details = relationship('InputBook_Book', backref='order', lazy=True)

    staff = relationship(Staff)


class Order (db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey(Staff.id))
    customer_id = Column(Integer, ForeignKey(Customer.id))
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now())
    total_price = Column(Float, default=0)
    status = Column(Integer, default=OrderStatus.PENDING.value)
    type = Column(Integer, default=OrderType.OFFLINE.value)

    details = relationship('OrderDetail', backref='order', lazy=True)

    staff = relationship(Staff)
    customer = relationship(Customer)

    def isCancel(self):
        return self.status == OrderStatus.PENDING.value and (self.created_date + timedelta(hours=48)) < datetime.now()


class OrderDetail (db.Model):
    __tablename__ = 'order_detail'
    order_id = Column(Integer, ForeignKey(Order.id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id), primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)

    book = relationship(Book)
