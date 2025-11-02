USE FoodDeliveryDB;

CREATE OR REPLACE VIEW OrderSummary AS
SELECT 
    o.order_id,
    c.customer_name,
    r.rest_name,
    o.order_date,
    o.status,
    o.total_amt
FROM Orders o
JOIN Customer c ON o.customer_id = c.customer_id
JOIN Restaurant r ON o.restaurant_id = r.restaurant_id;

-- To view:
SELECT * FROM OrderSummary;
