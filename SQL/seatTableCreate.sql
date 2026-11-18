CREATE TABLE Seat(
	seat_id INT PRIMARY KEY AUTO_INCREMENT,
    table_id int,
    
    FOREIGN KEY (table_id)
		REFERENCES tables(table_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)
