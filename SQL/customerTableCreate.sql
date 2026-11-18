CREATE TABLE customers(
	customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_fname VARCHAR(30),
    customer_lname VARCHAR(30),
    customer_usual_menuitem INT,
    customer_timesvisited INT,
    customer_lastvisit_date DATE,
    customer_notes TEXT,
    
    FOREIGN KEY (customer_usual_menuitem)
		REFERENCES menuitem(menuItem_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
)