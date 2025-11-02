USE FoodDeliveryDB;

-- TRIGGER: AUTO UPDATE ORDER TOTAL
DELIMITER $$
CREATE TRIGGER update_order_total
AFTER INSERT ON OrderItem
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET total_amt = (
        SELECT SUM(subtotal)
        FROM OrderItem
        WHERE OrderItem.order_id = NEW.order_id
    )
    WHERE Orders.order_id = NEW.order_id;
END $$
DELIMITER ;

-- STORED PROCEDURE: PLACE NEW ORDER (Assign partner + update status)
DELIMITER $$
CREATE PROCEDURE PlaceNewOrder (
    IN p_order_id INT
)
BEGIN
    DECLARE random_partner INT;

    -- Pick a random available partner
    SELECT partner_id
    INTO random_partner
    FROM DeliveryPartner
    WHERE availability_status = 'Available'
    ORDER BY RAND()
    LIMIT 1;

    -- Update order
    UPDATE Orders
    SET partner_id = random_partner, status = 'Placed'
    WHERE order_id = p_order_id;

    -- Mark partner busy
    UPDATE DeliveryPartner
    SET availability_status = 'Busy'
    WHERE partner_id = random_partner;

    -- Return confirmation
    SELECT p_order_id AS order_id, random_partner AS assigned_partner;
END $$
DELIMITER ;

-- FUNCTION: AVERAGE RATING PER RESTAURANT
DELIMITER $$
CREATE FUNCTION AvgRestaurantRating(p_restaurant_id INT)
RETURNS DECIMAL(3,2)
DETERMINISTIC
BEGIN
    DECLARE avg_rating DECIMAL(3,2);
    SELECT AVG(rating)
    INTO avg_rating
    FROM Review
    WHERE restaurant_id = p_restaurant_id;
    RETURN IFNULL(avg_rating, 0.00);
END $$
DELIMITER ;
