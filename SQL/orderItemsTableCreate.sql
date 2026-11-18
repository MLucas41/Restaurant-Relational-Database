CREATE TABLE orderItems(
	order_id INT PRIMARY KEY AUTO_INCREMENT,
    seat_id INT NOT NULL,
    menuitem_id INT NOT NULL,
    customer_id INT,
    order_total DECIMAL(10, 2) NOT NULL,
    
    FOREIGN KEY (seat_id)
		REFERENCES seat(seat_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
	FOREIGN KEY (menuitem_id)
		REFERENCES menuitem(menuitem_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

	FOREIGN KEY (customer_id)
		REFERENCES customers(customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)