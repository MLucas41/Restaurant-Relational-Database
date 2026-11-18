ALTER TABLE orderItems
ADD COLUMN sale_id INT NOT NULL;

ALTER TABLE orderItems
ADD CONSTRAINT fk_orderitems_sale
    FOREIGN KEY (sale_id)
    REFERENCES Sales(sale_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;