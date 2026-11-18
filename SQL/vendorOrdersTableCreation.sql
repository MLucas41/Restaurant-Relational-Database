USE lukes_lasagna;

CREATE TABLE VendorOrders(
	order_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    ingredient_unit VARCHAR(10),
    ingredient_quantity INT,
    total_order_price DECIMAL(10, 2),
    date_last_ordered_from DATE,
    
    FOREIGN KEY (vendor_id) 
		REFERENCES ingredientvendors(vendor_ingredient_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY (ingredient_id) 
		REFERENCES ingredientinventory(ingredient_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
    )