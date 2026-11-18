USE lukes_lasagna;

CREATE TABLE ingredientVendors(
	vendor_ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    vendor_name VARCHAR(30) NOT NULL,
    date_last_ordered_from DATE,
    vendor_ingredient_notes TEXT,
    
    FOREIGN KEY (employee_id) 
		REFERENCES employees(employee_id)
		ON DELETE SET NULL
		ON UPDATE CASCADE
    )