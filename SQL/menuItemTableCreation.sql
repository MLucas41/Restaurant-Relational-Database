USE lukes_lasagna;

CREATE TABLE menuItem(
	menuItem_id INT PRIMARY KEY AUTO_INCREMENT,
    menuItem_name VARCHAR(30) NOT NULL,
    menuItem_isAvailable BOOL NOT NULL DEFAULT TRUE,
    menuItem_cost DECIMAL(10, 2) NOT NULL,
    menuItem_type ENUM("Entre", "Side", "Drink", "Dessert")
)