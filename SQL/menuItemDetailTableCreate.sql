CREATE TABLE menuItemDetail(
	line_number INT PRIMARY KEY AUTO_INCREMENT,
	menuItem_id INT NOT NULL,
	ingredient_id INT NOT NULL,
    ingredient_quantity INT NOT NULL DEFAULT 1,
    ingredient_unit VARCHAR(10),
    
    FOREIGN KEY (menuItem_id)
		REFERENCES menuitem(menuItem_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        
	FOREIGN KEY (ingredient_id)
		REFERENCES ingredientinventory(ingredient_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
)
    