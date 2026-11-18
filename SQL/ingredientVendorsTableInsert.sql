USE lukes_lasagna;

INSERT INTO ingredientVendors (
    employee_id,
    vendor_name,
    date_last_ordered_from,
    vendor_ingredient_notes
) VALUES
(2,   'Sysco Foods',             '2025-02-10', 'Primary supplier for dry goods.'),
(2,   'FreshPoint Produce',      '2025-01-28', 'Used mainly for fruits and vegetables.'),
(8,   'US Foods',                '2025-02-03', 'Bulk pasta and canned items.'),
(8,   'La Pizzeria Imports',     '2025-02-15', 'Specialty cheeses and cured meats.'),
(2,'Pacific Seafood Co.',     '2025-01-12', 'Occasional seafood orders.'),
(2,   'Golden Grain Mills',      '2024-12-20', 'Flour and grains; ordered monthly.'),
(8,   'Morning Fresh Dairy',     '2025-02-05', 'Milk, cream, and butter supply.'),
(2,   'Roma Specialty Foods',    '2024-11-30', 'Imported Italian ingredients.'),
(8,'Evergreen Paper Supply',  '2025-01-17', 'Paper goods and to-go containers.'),
(8,   'Acme Cleaning Supplies',  '2025-02-01', 'Cleaning chemicals and sanitation.'),
(2,   'Speedy Delivery Produce', '2025-02-09', 'Backup produce vendor.'),
(8,   'Chef’s Choice Spices',    '2025-01-25', 'Bulk herbs and seasoning blends.'),
(2,   'High Mountain Meats',     '2024-12-28', 'Occasional specialty meat orders.'),
(8,   'Blue Ribbon Bakery Co.',  '2025-02-14', 'Fresh breads delivered weekly.'),
(2,   'Sunrise Eggs Co.',        '2025-02-06', 'Egg shipments, large weekly orders.');