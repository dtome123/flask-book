from flask import render_template, jsonify, session, request, redirect
from app import app
from dao import get_book, create_receipt, create_book_receipt, get_receipt, list_books
from model import Book


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input_book/create', methods=['POST'])
def input_book_create_post():

    id = request.form['id']

    book = Book(name="Chapter 1", description="Chapter 1",
                price=100, quantity=100)

    quantity = request.form['quantity']

    books = session["sell_books"]

    isExists = False
    for book in books:
        if book.id == id:
            book.quantity += int(quantity)
            isExists = True

    if isExists == False:
        books.append({book: book, quantity: quantity})

    return redirect('/input_book/create')


@app.route('/input_book/create')
def input_book_create():
    books = list_books()
    cart = session["sell_books"]

    return render_template('create_input_book.html', books=books, cart=cart)


@app.route('/input_book/create/submit', methods=['POST'])
def input_book_create_submit():
    cart = session["sell_books"]

    staff_id = 1

    receipt = create_receipt(staff_id)

    del session["sell_books"]

    return redirect('/input_book/' + str(receipt.id))


@app.route('/create_receipt')
def create_receipt_index():
    res = get_receipt(4)
    print(res.books[0].name)

    return jsonify()
