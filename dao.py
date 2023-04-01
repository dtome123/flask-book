from app import db
from model import Book, Receipt, BookReceipt


def get_book(book_id):
    book = Book.query.get(book_id)
    return book


def list_books():
    books = Book.query.all()
    return books


def create_receipt(user_id):
    receipt = Receipt(user_id=user_id)
    db.session.add(receipt)
    db.session.commit()

    return receipt


def get_receipt(receipt_id):
    receipts = Receipt.query.get(receipt_id)
    return receipts


def create_book_receipt(book_id, receipt_id, quantity):

    book_receipt = BookReceipt(
        book_id=book_id, receipt_id=receipt_id, quantity=quantity)
    db.session.add(book_receipt)
    db.session.commit()

    return book_receipt
