-- SMART BITES DATABASE CREATION
CREATE DATABASE IF NOT EXISTS FoodDeliveryDB;
USE FoodDeliveryDB;

-- CUSTOMER TABLE
CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(100) UNIQUE,
    customer_phno VARCHAR(15),
    customer_street VARCHAR(100),
    customer_city VARCHAR(100),
    customer_pin VARCHAR(10)
);

-- USER AUTH TABLE
CREATE TABLE UserAuth (
    username VARCHAR(50) PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- RESTAURANT TABLE
CREATE TABLE Restaurant (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    rest_name VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(50),
    contact_no VARCHAR(15),
    rest_street VARCHAR(100),
    rest_city VARCHAR(100),
    rest_pin VARCHAR(10)
);

-- MENU ITEM TABLE
CREATE TABLE MenuItem (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    cuisine_id INT,
    restaurant_id INT,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

-- DELIVERY PARTNER TABLE
CREATE TABLE DeliveryPartner (
    partner_id INT AUTO_INCREMENT PRIMARY KEY,
    partner_name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15),
    availability_status ENUM('Available', 'Busy') DEFAULT 'Available'
);

-- ORDERS TABLE
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    restaurant_id INT,
    order_date DATE,
    status VARCHAR(50) DEFAULT 'Pending',
    total_amt DECIMAL(10,2),
    partner_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (partner_id) REFERENCES DeliveryPartner(partner_id)
);

-- ORDER ITEM TABLE
CREATE TABLE OrderItem (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (item_id) REFERENCES MenuItem(item_id)
);

-- PAYMENT TABLE
CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    pay_method VARCHAR(50),
    pay_status VARCHAR(20),
    transaction_date DATE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- REVIEW TABLE
CREATE TABLE Review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    customer_id INT,
    restaurant_id INT,
    rating DECIMAL(3,2),
    comment VARCHAR(255),
    review_date DATE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);
