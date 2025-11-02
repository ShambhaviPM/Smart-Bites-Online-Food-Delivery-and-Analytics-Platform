USE FoodDeliveryDB;

-- CUSTOMERS
INSERT INTO Customer (customer_name, customer_email, customer_phno, customer_street, customer_city, customer_pin)
VALUES
('Aarav Mehta', 'aarav@gmail.com', '9876543210', 'MG Road', 'Bangalore', '560001'),
('Diya Sharma', 'diya@gmail.com', '9786541230', 'Koramangala', 'Bangalore', '560034');

-- RESTAURANTS
INSERT INTO Restaurant (rest_name, cuisine_type, contact_no, rest_street, rest_city, rest_pin)
VALUES
('SpiceHub', 'Indian', '9988776655', 'Indiranagar', 'Bangalore', '560038'),
('LaPasta', 'Italian', '8877665544', 'HSR Layout', 'Bangalore', '560102');

-- DELIVERY PARTNERS
INSERT INTO DeliveryPartner (partner_name, contact_no, availability_status)
VALUES
('Rohit Singh', '9000011111', 'Available'),
('Priya Das', '9000022222', 'Available'),
('Arjun Rao', '9000033333', 'Busy'),
('Meena Iyer', '9000044444', 'Available'),
('Rahul Jain', '9000055555', 'Busy'),
('Aisha Khan', '9000066666', 'Available'),
('Ravi Nair', '9000077777', 'Available'),
('Kiran Patel', '9000088888', 'Available'),
('Sneha Verma', '9000099999', 'Available'),
('Vikram Malhotra', '9000010000', 'Available');

-- MENU ITEMS
INSERT INTO MenuItem (item_name, price, cuisine_id, restaurant_id)
VALUES
('Paneer Butter Masala', 180.00, 1, 1),
('Masala Dosa', 90.00, 1, 1),
('Butter Chicken', 220.00, 1, 1),
('Margherita Pizza', 250.00, 2, 2),
('Pasta Alfredo', 300.00, 2, 2),
('Lasagna', 280.00, 2, 2),
('Garlic Bread', 150.00, 2, 2),
('Tandoori Roti', 20.00, 1, 1),
('Gulab Jamun', 100.00, 1, 1),
('Cold Coffee', 120.00, 1, 1);
