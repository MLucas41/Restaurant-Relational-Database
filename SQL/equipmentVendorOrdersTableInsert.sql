INSERT INTO equipmentVendorOrders (
    vendor_id,
    equipment_id,
    equipment_quantity,
    total_order_price,
    date_last_ordered_from
) VALUES
-- 1 Chef Knife Set → WebstaurantStore (Vendor 2)
(2,  1,  2,   260.00, '2025-01-15'),
-- 2 Cutting Boards → Restaurant Depot (Vendor 1)
(1,  2,  10,  120.00, '2025-01-12'),
-- 3 Pizza Oven → Commercial Kitchen Co. (Vendor 5)
(5,  3,  1,  7800.00, '2023-08-01'),
-- 4 Pasta Roller Machine → ProBake Supply (Vendor 8)
(8,  4,  1,  950.00, '2024-10-05'),
-- 5 Stainless Steel Prep Tables → SteelCraft Fixtures (Vendor 12)
(12, 5,  2,  1600.00, '2023-12-20'),
-- 6 Stock Pots → WebstaurantStore (Vendor 2)
(2,  6,  4,   320.00, '2024-04-12'),
-- 7 Sauce Pans → Restaurant Depot (Vendor 1)
(1,  7,  6,   270.00, '2024-07-18'),
-- 8 Cast Iron Skillets → WebstaurantStore (Vendor 2)
(2,  8,  3,   150.00, '2024-09-10'),
-- 9 Mixing Bowl Sets → Restaurant Depot (Vendor 1)
(1,  9,  3,    90.00, '2024-12-01'),
-- 10 Commercial Mixer → KitchenTech Services (Vendor 9)
(9, 10, 1,  2400.00, '2024-03-08'),
-- 11 Refrigerator Unit → American Refrigeration (Vendor 7)
(7, 11, 1,  5200.00, '2023-10-22'),
-- 12 Freezer Unit → American Refrigeration (Vendor 7)
(7, 12, 1,  4800.00, '2023-11-30'),
-- 13 Food Storage Containers → Restaurant Depot (Vendor 1)
(1, 13, 5,   100.00, '2025-01-12'),
-- 14 Digital Thermometers → WebstaurantStore (Vendor 2)
(2, 14, 4,    80.00, '2024-06-25'),
-- 15 Garlic Press Tools → Chef’s Choice Tools (Vendor 4)
(4, 15, 3,    45.00, '2025-01-20'),
-- 16 Oven Mitts & Gloves → EcoClean Solutions (Vendor 14)
(14,16, 6,    72.00, '2025-02-02'),
-- 17 Sheet Pans → ProBake Supply (Vendor 8)
(8, 17, 10,  180.00, '2024-12-14'),
-- 18 Food Processor → KitchenTech Services (Vendor 9)
(9, 18, 1,   450.00, '2024-05-19'),
-- 19 Dish Racks → Superior Dishwashers (Vendor 11)
(11,19, 3,   180.00, '2024-10-30'),
-- 20 Rolling Pins → WebstaurantStore (Vendor 2)
(2, 20, 3,    60.00, '2024-11-22');