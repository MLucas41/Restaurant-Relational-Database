CREATE TABLE equipmentVendorOrders(
	order_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    equipment_id INT NOT NULL,
    equipment_quantity INT,
    total_order_price DECIMAL(10, 2),
    date_last_ordered_from DATE,
    
    FOREIGN KEY (vendor_id) 
		REFERENCES equipmentvendors(vendor_equipment_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY (equipment_id) 
		REFERENCES equipmentinventory(equipment_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
    )