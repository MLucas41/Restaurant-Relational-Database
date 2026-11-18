CREATE TABLE Sales(
	sale_id INT PRIMARY KEY AUTO_INCREMENT,
    waitstaff_id INT,
    table_id INT NOT NULL,
    sale_total DECIMAL(10, 2) NOT NULL,
    sale_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (waitstaff_id)
		REFERENCES employees(employee_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
        
	FOREIGN KEY (table_id)
		REFERENCES tables(table_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)