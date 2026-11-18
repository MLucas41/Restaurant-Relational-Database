USE lukes_lasagna;

CREATE TABLE ingredientInventory
(
	ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    ingredient_name VARCHAR(50) NOT NULL,
    ingredient_unit VARCHAR(10),
    ingredient_quantity INT NOT NULL,
    ingredient_info TEXT
)