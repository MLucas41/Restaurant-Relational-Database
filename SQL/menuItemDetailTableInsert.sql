INSERT INTO menuItemDetail (menuItem_id, ingredient_id, ingredient_quantity, ingredient_unit)
VALUES
-- 1. Lasagna
(1, 12, 2, 'units'),  -- Lasagna Sheets
(1, 3,  1, 'units'),  -- Ricotta Cheese
(1, 14, 1, 'units'),  -- Ground Beef
(1, 4,  1, 'units'),  -- Tomato Sauce
(1, 1,  1, 'units'),  -- Mozzarella Cheese
(1, 2,  1, 'units'),  -- Parmesan Cheese

-- 2. Spaghetti Bolognese
(2, 9,  1, 'units'),  -- Spaghetti Pasta
(2, 4,  1, 'units'),  -- Tomato Sauce
(2, 5,  1, 'units'),  -- Crushed Tomatoes
(2, 14, 1, 'units'),  -- Ground Beef
(2, 6,  1, 'units'),  -- Olive Oil
(2, 7,  1, 'units'),  -- Fresh Garlic
(2, 18, 1, 'units'),  -- Red Onions

-- 3. Fettuccine Alfredo
(3, 10, 1, 'units'),  -- Fettuccine Pasta
(3, 20, 1, 'units'),  -- Heavy Cream
(3, 2,  1, 'units'),  -- Parmesan Cheese
(3, 6,  1, 'units'),  -- Olive Oil
(3, 7,  1, 'units'),  -- Fresh Garlic

-- 4. Chicken Parmesan
(4, 15, 1, 'units'),  -- Chicken Breast
(4, 4,  1, 'units'),  -- Tomato Sauce
(4, 1,  1, 'units'),  -- Mozzarella Cheese
(4, 2,  1, 'units'),  -- Parmesan Cheese
(4, 6,  1, 'units'),  -- Olive Oil
(4, 7,  1, 'units'),  -- Fresh Garlic

-- 5. Penne alla Vodka
(5, 11, 1, 'units'),  -- Penne Pasta
(5, 4,  1, 'units'),  -- Tomato Sauce
(5, 5,  1, 'units'),  -- Crushed Tomatoes
(5, 20, 1, 'units'),  -- Heavy Cream
(5, 6,  1, 'units'),  -- Olive Oil
(5, 7,  1, 'units'),  -- Fresh Garlic
(5, 18, 1, 'units'),  -- Red Onions

-- 6. Margherita Pizza
(6, 19, 1, 'units'),  -- Bread Loaves (as crust)
(6, 4,  1, 'units'),  -- Tomato Sauce
(6, 1,  1, 'units'),  -- Mozzarella Cheese
(6, 8,  1, 'units'),  -- Fresh Basil
(6, 16, 1, 'units'),  -- Fresh Tomatoes
(6, 6,  1, 'units'),  -- Olive Oil

-- 7. Meat Lovers Pizza
(7, 19, 1, 'units'),  -- Bread Loaves (as crust)
(7, 4,  1, 'units'),  -- Tomato Sauce
(7, 1,  1, 'units'),  -- Mozzarella Cheese
(7, 13, 1, 'units'),  -- Italian Sausage
(7, 14, 1, 'units'),  -- Ground Beef
(7, 17, 1, 'units'),  -- Mushrooms
(7, 6,  1, 'units'),  -- Olive Oil

-- 8. Eggplant Parmesan (approximated with existing veg)
(8, 17, 1, 'units'),  -- Mushrooms (stand-in veg)
(8, 4,  1, 'units'),  -- Tomato Sauce
(8, 1,  1, 'units'),  -- Mozzarella Cheese
(8, 2,  1, 'units'),  -- Parmesan Cheese
(8, 6,  1, 'units'),  -- Olive Oil
(8, 7,  1, 'units'),  -- Fresh Garlic
(8, 8,  1, 'units'),  -- Fresh Basil

-- 9. Shrimp Scampi (protein approximated)
(9, 15, 1, 'units'),  -- Chicken Breast (stand-in protein)
(9, 10, 1, 'units'),  -- Fettuccine Pasta
(9, 6,  1, 'units'),  -- Olive Oil
(9, 7,  1, 'units'),  -- Fresh Garlic
(9, 20, 1, 'units'),  -- Heavy Cream
(9, 8,  1, 'units'),  -- Fresh Basil

-- 10. Ravioli Ricotta
(10, 3,  1, 'units'),  -- Ricotta Cheese
(10, 4,  1, 'units'),  -- Tomato Sauce
(10, 2,  1, 'units'),  -- Parmesan Cheese
(10, 6,  1, 'units'),  -- Olive Oil
(10, 7,  1, 'units'),  -- Fresh Garlic
(10, 8,  1, 'units'),  -- Fresh Basil

-- 11. Garlic Bread
(11, 19, 1, 'units'),  -- Bread Loaves
(11, 7,  1, 'units'),  -- Fresh Garlic
(11, 6,  1, 'units'),  -- Olive Oil
(11, 1,  1, 'units'),  -- Mozzarella Cheese

-- 12. Side Caesar Salad (approximate, no lettuce in inventory)
(12, 16, 1, 'units'),  -- Fresh Tomatoes
(12, 18, 1, 'units'),  -- Red Onions
(12, 2,  1, 'units'),  -- Parmesan Cheese
(12, 6,  1, 'units'),  -- Olive Oil
(12, 8,  1, 'units'),  -- Fresh Basil

-- 13. Caprese Salad
(13, 16, 1, 'units'),  -- Fresh Tomatoes
(13, 1,  1, 'units'),  -- Mozzarella Cheese
(13, 8,  1, 'units'),  -- Fresh Basil
(13, 6,  1, 'units'),  -- Olive Oil

-- 14. Meatballs (2)
(14, 14, 1, 'units'),  -- Ground Beef
(14, 13, 1, 'units'),  -- Italian Sausage
(14, 4,  1, 'units'),  -- Tomato Sauce
(14, 7,  1, 'units'),  -- Fresh Garlic
(14, 2,  1, 'units'),  -- Parmesan Cheese
(14, 19, 1, 'units'),  -- Bread Loaves (breadcrumbs)

-- 15. Mozzarella Sticks
(15, 1,  1, 'units'),  -- Mozzarella Cheese
(15, 19, 1, 'units'),  -- Bread Loaves (breading)
(15, 6,  1, 'units'),  -- Olive Oil (frying)
(15, 4,  1, 'units'),  -- Tomato Sauce (dipping)

-- 20. Tiramisu (approximate)
(20, 20, 1, 'units'),  -- Heavy Cream
(20, 3,  1, 'units'),  -- Ricotta Cheese (stand-in for mascarpone)
(20, 19, 1, 'units');  -- Bread Loaves (stand-in for ladyfingers)
