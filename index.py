from flask import render_template, jsonify, session, request, redirect
from app import app, login
from dao import list_books, get_staff_by_id, auth_user, get_book, list_input_books, create_input_book, get_input_book, create_order, list_orders, get_order
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from model import Book


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login")
def my_login():
    return render_template("login.html")


@app.route("/login", methods=['post'])
def login_process():
    username = request.form['username']
    password = request.form['password']
    u = auth_user(username, password)
    if u:
        login_user(u)

        return redirect("/")

    return render_template("login.html")


@app.route('/logout')
def my_logout():
    logout_user()
    return redirect("/login")


@app.errorhandler(401)
def unauthorized_page(error):
    return render_template("401.html"), 401


@app.route('/book')
def list_book():
    books = list_books()
    return render_template('list_book.html', books=books)


@app.route('/book/<int:book_id>')
def view_book(book_id):
    book = get_book(book_id)
    return render_template('book.html', book=book)


@app.route('/me')
@login_required
def get_me():

    staff = get_staff_by_id(current_user.id)
    return render_template("me.html", staff=staff)

############################## Input Book ##############################

# Thêm sách vào danh sách giỏ để đặt hàng


@app.route('/input_book/create', methods=['POST'])
def input_book_create_post():

    id = request.form['book_id']

    # Lấy thông tin sách từ DB
    book = get_book(id)

    # Lấy số lượng nhập từ form thêm sách
    quantity = request.form['quantity']
    books = []

    # Kiểm tra danh sách sách chuẩn bị đặt đã lưu trên sessiong chưa
    if 'input_book' in session:
        # Nếu có thì thêm mới vào đối với sách chưa có trong danh sách để tạm, nếu có thì tăng số lượng
        items = session["input_book"]

        # Kiểm tra sách theo id trả về có trong db không, nếu không có báo lỗi không tìm thấy
        if book is None:
            list = list_books()
            return render_template('create_input_book.html', books=list, cart=items, error="Không tìm thấy sách này")

        # kiểm tra sách này đã có trong giỏ hàng chưa nếu có thì tăng số lượng
        is_exist = False

        for item in items:
            if item["book"].id == int(id):
                item["quantity"] += int(quantity)
                is_exist = True

            books.append(item)

        # Nếu sách này chưa có trong giỏ hàng thì thêm vào
        if not is_exist:
            books.append({"book": book, "quantity": int(quantity)})
    else:
        if book:
            books.append({"book": book, "quantity": int(quantity)})
        else:
            list = list_books()
            return render_template('create_input_book.html', books=list, cart=[], error="Không tìm thấy sách này")

    if books.__len__() > 0:
        session["input_book"] = books

    return redirect('/input_book/create')


@app.route('/input_book/create')
def input_book_create():

    books = list_books()

    cart = []
    if 'input_book' in session:
        cart = session["input_book"]

    return render_template('create_input_book.html', books=books, cart=cart)


@app.route('/input_book/clear')
def clear_input_book():
    if 'input_book' in session:
        del session["input_book"]
    return redirect('/input_book/create')


@app.route('/input_book/create/submit', methods=['POST'])
def input_book_create_submit():
    cart = session["input_book"]

    staff_id = current_user.id

    input = create_input_book(cart, staff_id)

    del session["input_book"]

    return redirect('/input_book/'+str(input.id))


@app.route('/input_book/<int:id>')
def view_detail_input_book(id):
    res = get_input_book(id)

    return render_template('detail_input_book.html', input=res)


@app.route('/input_book')
def view_list_input_book():
    res = list_input_books()

    return render_template('list_input_book.html', list=res)

############################################# ORDER ##############################################


@app.route('/order/create', methods=['POST'])
def order_create_post():

    id = request.form['book_id']

    # Lấy thông tin sách từ DB
    book = get_book(id)

    quantity = request.form['quantity']
    books = []

    # Kiểm tra danh sách sách order đã lưu trên session chưa
    if 'order' in session:
        items = session["order"]

        # Kiểm tra sách theo id trả về có trong db không, nếu không có báo lỗi không tìm thấy
        if book is None:
            list = list_books()
            return render_template('create_order.html', books=list, cart=items, error="Không tìm thấy sách này")

        # kiểm tra sách này đã có trong giỏ hàng chưa nếu có thì tăng số lượng
        is_exist = False
        for item in items:
            if item["book"].id == int(id):
                item["quantity"] += int(quantity)
                is_exist = True

            books.append(item)

        # Nếu sách này chưa có trong giỏ hàng thì thêm vào
        if not is_exist:
            books.append({"book": book, "quantity": int(quantity)})
    else:
        if book:
            books.append({"book": book, "quantity": int(quantity)})
        else:
            list = list_books()
            return render_template('create_order.html', books=list, cart=[], error="Không tìm thấy sách này")

    if books.__len__() > 0:
        session["order"] = books

    return redirect('/order/create')


@app.route('/order/create')
def order_create():

    books = list_books()

    cart = []
    sum = 0
    if 'order' in session:
        cart = session["order"]

        for item in cart:
            sum += item["book"].price * item["quantity"]

    return render_template('create_order.html', books=books, cart=cart, sum=sum)


@app.route('/order/clear')
def clear_order():
    if 'order' in session:
        del session["order"]
    return redirect('/order/create')


@app.route('/order/create/submit', methods=['POST'])
def order_create_submit():
    cart = session["order"]

    staff_id = current_user.id

    customer_id = request.form['customer_id']

    order = create_order(cart, staff_id, customer_id)

    del session["order"]

    return redirect('/order/'+str(order.id))


@app.route('/order/<int:id>')
def view_detail_order(id):
    res = get_order(id)

    return render_template('detail_order.html', order=res)


@app.route('/order')
def view_list_order():
    res = list_orders()

    return render_template('list_order.html', list=res)


@login.user_loader
def get_user(staff_id):
    return get_staff_by_id(staff_id=staff_id)
