USE FoodDeliveryDB;

-- Nested query: Top restaurants above overall average rating
SELECT r.rest_name, ROUND(AVG(rv.rating), 2) AS avg_rating
FROM Review rv
JOIN Restaurant r ON rv.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id
HAVING avg_rating > (
    SELECT AVG(rating) FROM Review
)
ORDER BY avg_rating DESC;

-- Average restaurant rating using function
SELECT rest_name, AvgRestaurantRating(restaurant_id) AS avg_rating
FROM Restaurant;

-- Orders placed today
SELECT * FROM Orders WHERE order_date = CURDATE();

-- List customers who ordered more than once
SELECT c.customer_name, COUNT(o.order_id) AS total_orders
FROM Customer c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING total_orders > 1;
