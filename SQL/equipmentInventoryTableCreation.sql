USE lukes_lasagna;

CREATE TABLE equipmentInventory
(
	equipment_id INT PRIMARY KEY AUTO_INCREMENT,
    equipment_name VARCHAR(50) NOT NULL,
    equipment_unit VARCHAR(10),
    equipment_quantity INT NOT NULL,
    equipment_date_last_purchased DATE NOT NULL,
    equipment_lifespan_days INT NOT NULL,
    equipment_replacement_date DATE
    AS (DATE_ADD(equipment_date_last_purchased, INTERVAL equipment_lifespan_days DAY)) STORED,
    equipment_info TEXT
)