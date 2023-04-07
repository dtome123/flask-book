from app import db
from model import Book, InputBook, InputBook_Book, Staff, Order, OrderDetail


def get_staff_by_id(staff_id):
    staff = Staff.query.get(staff_id)
    return staff


def auth_user(username, password):
    return Staff.query.filter(Staff.username.__eq__(username),
                              Staff.password.__eq__(password)).first()


def get_book(book_id):
    book = Book.query.get(book_id)
    return book


def list_books():
    books = Book.query.all()
    return books


def list_input_books():
    input_books = InputBook.query.all()
    return input_books


def get_input_book(input_book_id):
    input_book = InputBook.query.get(input_book_id)
    return input_book


def create_input_book(list, staff_id):
    input_book = InputBook(staff_id=staff_id)
    db.session.add(input_book)
    db.session.commit()

    detail = []
    for item in list:
        print(item["book"].id, item["quantity"])
        detail.append(InputBook_Book(
            book_id=item["book"].id,
            input_book_id=input_book.id,
            quantity=item["quantity"]
        ))

    db.session.add_all(detail)
    db.session.commit()

    return input_book


############################### ORDER ##############################
def list_orders():
    orders = Order.query.all()
    return orders


def get_order(order_id):
    order = Order.query.get(order_id)
    return order


def create_order(list, staff_id, customer_id):
    order = Order(staff_id=staff_id)
    if customer_id:
        order.customer_id = customer_id

    db.session.add(order)
    db.session.commit()

    total_price = 0
    detail = []
    for item in list:
        print(item["book"].id, item["quantity"])
        detail.append(OrderDetail(
            book_id=item["book"].id,
            order_id=order.id,
            quantity=item["quantity"],
            price=item["book"].price
        ))
        total_price += item["book"].price * item["quantity"]

    order.total_price = total_price

    db.session.add_all(detail)
    db.session.commit()

    return order
