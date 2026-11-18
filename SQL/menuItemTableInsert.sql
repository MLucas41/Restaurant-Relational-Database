INSERT INTO menuItem (
    menuItem_name,
    menuItem_isAvailable,
    menuItem_cost,
    menuItem_type
) VALUES
-- ENTRES
('Lasagna', TRUE, 15.99, 'Entre'),
('Spaghetti Bolognese', TRUE, 13.49, 'Entre'),
('Fettuccine Alfredo', TRUE, 14.99, 'Entre'),
('Chicken Parmesan', TRUE, 16.49, 'Entre'),
('Penne alla Vodka', TRUE, 13.99, 'Entre'),
('Margherita Pizza', TRUE, 12.99, 'Entre'),
('Meat Lovers Pizza', TRUE, 15.99, 'Entre'),
('Eggplant Parmesan', FALSE, 14.49, 'Entre'),
('Shrimp Scampi', TRUE, 17.99, 'Entre'),
('Ravioli Ricotta', TRUE, 13.99, 'Entre'),

-- SIDES
('Garlic Bread', TRUE, 4.99, 'Side'),
('Side Caesar Salad', TRUE, 5.99, 'Side'),
('Caprese Salad', TRUE, 7.49, 'Side'),
('Meatballs (2)', TRUE, 4.49, 'Side'),
('Mozzarella Sticks', TRUE, 6.99, 'Side'),

-- DRINKS
('Italian Soda', TRUE, 3.49, 'Drink'),
('Espresso', TRUE, 2.99, 'Drink'),
('House Red Wine', TRUE, 6.99, 'Drink'),
('Sparkling Water', TRUE, 2.49, 'Drink'),

-- DESSERTS
('Tiramisu', TRUE, 6.49, 'Dessert');