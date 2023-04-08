from app import db
from model import Book, InputBook, InputBook_Book, Staff, Order, OrderDetail, OrderType, OrderStatus


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


def add_quantity_book(book_id, quantity):
    book = Book.query.get(book_id)
    book.quantity = book.quantity+quantity
    db.session.commit()


def subtract_quantity_book(book_id, quantity):
    book = Book.query.get(book_id)
    book.quantity = book.quantity-quantity
    db.session.commit()


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

        add_quantity_book(item["book"].id, item["quantity"])

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
    order = Order(staff_id=staff_id, type=OrderType.ONLINE.value,
                  status=OrderStatus.COMPLETED.value)
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

############################### CUSTOMER ORDER ##############################


def list_customer_orders():
    orders = Order.query.all()
    return orders


def get_customer_order(order_id):
    order = Order.query.get(order_id)
    return order


def create_customer_order(list, customer_id):
    order = Order(type=OrderType.OFFLINE.value,
                  status=OrderStatus.PENDING.value)
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


def complete_customer_order(id):
    order = get_customer_order(order_id=id)
    order.status = OrderStatus.COMPLETED.value
    db.session.commit()

    for item in order.details:
        subtract_quantity_book(item.book.id, item.quantity)
