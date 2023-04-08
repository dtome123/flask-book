USE book_store;

CREATE TABLE book_store.`customer` (
	id INT PRIMARY key auto_increment ,
	name varchar(100) NOT NULL,
	phone varchar(20),
	address varchar(100)
);

CREATE TABLE book_store.`staff`(
	id INT PRIMARY key auto_increment ,
	name varchar(100) NOT NULL,
	phone varchar(20),
	address varchar(100),
	username varchar(50),
	password varchar(100),
	avatar varchar(100)
);

CREATE TABLE book_store.`book`(
	id INT PRIMARY key auto_increment ,
	name varchar(100),
	description varchar(1000),
	price double ,
	image varchar(100),
	quantity int,
	author varchar(100)
);

CREATE TABLE book_store.`input_book`(
	id INT PRIMARY key auto_increment,
	staff_id int, 
	created_date DATETIME,
	updated_date DATETIME
);

CREATE TABLE book_store.`order`(
	id INT PRIMARY key auto_increment,
	staff_id int,
	customer_id int,
	created_date DATETIME,
	updated_date DATETIME,
	total_price double,
	type int,
	status int
);

create table book_store.`input_book_book`(
	book_id int,
	input_book_id int,
	quantity int
);

CREATE table book_store.`order_detail` (
	order_id int,
	book_id int,
	quantity int,
	price double,
	CONSTRAINT order_detail_pk PRIMARY KEY (order_id,book_id)
);

INSERT into book_store.`customer`(name)
values("Nguyen van b")

insert into book_store.`staff` (name,phone,address, username, password,avatar)
values("nguyen van a", "0909090909","123 ABC","vana","123456","https://imgv3.fotor.com/images/blog-cover-image/part-blurry-image.jpg")
