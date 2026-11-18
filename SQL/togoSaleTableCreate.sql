CREATE TABLE TogoOrders(
    togo_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    customer_id INT,
    customer_name VARCHAR(60),
    customer_phone VARCHAR(20),
    pickup_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    instructions TEXT,
    
    FOREIGN KEY (customer_id)
		REFERENCES customers(customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    
    FOREIGN KEY (sale_id)
        REFERENCES sales(sale_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);