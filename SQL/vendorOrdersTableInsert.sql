INSERT INTO VendorOrders (
    vendor_id,
    ingredient_id,
    ingredient_unit,
    ingredient_quantity,
    totaL_order_price,
    date_last_ordered_from
) VALUES
-- 1 Mozzarella Cheese – Morning Fresh Dairy
(7,  1, 'lbs',    15,  67.50, '2025-02-10'),
-- 2 Parmesan Cheese – Morning Fresh Dairy
(7,  2, 'lbs',    10,  70.00, '2025-02-08'),
-- 3 Ricotta Cheese – Morning Fresh Dairy
(7,  3, 'lbs',    12,  36.00, '2025-02-05'),
-- 4 Tomato Sauce – US Foods
(3,  4, 'gal',     6,  60.00, '2025-02-03'),
-- 5 Crushed Tomatoes – Roma Specialty Foods
(8,  5, 'cans',   24,  60.00, '2025-01-30'),
-- 6 Olive Oil – La Pizzeria Imports
(4,  6, 'gal',     4,  80.00, '2025-01-28'),
-- 7 Fresh Garlic – Chef’s Choice Spices
(12, 7, 'lbs',     8,  12.00, '2025-01-25'),
-- 8 Fresh Basil – FreshPoint Produce
(2,  8, 'lbs',     3,  18.00, '2025-01-24'),
-- 9 Spaghetti Pasta – US Foods
(3,  9, 'lbs',    20,  24.00, '2025-01-22'),
-- 10 Fettuccine Pasta – US Foods
(3, 10, 'lbs',    15,  19.50, '2025-01-20'),
-- 11 Penne Pasta – Golden Grain Mills
(6, 11, 'lbs',    25,  27.50, '2025-01-18'),
-- 12 Lasagna Sheets – US Foods
(3, 12, 'lbs',    10,  15.00, '2025-01-16'),
-- 13 Italian Sausage – High Mountain Meats
(13,13, 'lbs',    15,  60.00, '2025-01-15'),
-- 14 Ground Beef – High Mountain Meats
(13,14, 'lbs',    18,  63.00, '2025-01-13'),
-- 15 Chicken Breast – High Mountain Meats
(13,15, 'lbs',    20,  60.00, '2025-01-12'),
-- 16 Fresh Tomatoes – FreshPoint Produce
(2, 16, 'lbs',    12,  24.00, '2025-01-10'),
-- 17 Mushrooms – Speedy Delivery Produce
(11,17, 'lbs',     8,  20.00, '2025-01-09'),
-- 18 Red Onions – Sysco Foods
(1, 18, 'lbs',    10,  12.00, '2025-01-08'),
-- 19 Bread Loaves – Blue Ribbon Bakery Co.
(14,19, 'loaves', 30,  54.00, '2025-01-07'),
-- 20 Heavy Cream – Morning Fresh Dairy
(7, 20, 'qt',     12,  36.00, '2025-01-05');