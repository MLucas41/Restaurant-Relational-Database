CREATE TABLE tables(
	table_id INT PRIMARY KEY AUTO_INCREMENT,
    server_id INT,
    table_seats INT NOT NULL,
    table_notes TEXT,
    
    FOREIGN KEY (server_id)
		REFERENCES employees(employee_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
)