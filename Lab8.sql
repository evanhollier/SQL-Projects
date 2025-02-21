DROP PROCEDURE IF EXISTS myCreateTable;
DROP PROCEDURE IF EXISTS mySelectTest;

DELIMITER $$
CREATE PROCEDURE myCreateTable(IN entries INT)
BEGIN 
    DECLARE counter INT DEFAULT 0;
	
    DROP TABLE IF EXISTS table1;
    CREATE TABLE table1 (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    num INT(4),
    INDEX (num)
    );
    
    WHILE counter < entries DO
		INSERT INTO table1 (num)
        VALUES (FLOOR(RAND()*(1000)));
        SET counter = counter + 1;
	END WHILE;
END$$
DELIMITER ;

-- 153.578 sec
-- 167.875 sec with index
-- CALL myCreateTable(100000);



DELIMITER $$
CREATE PROCEDURE mySelectTest(IN target INT, IN loops INT, OUT occurrences INT)
BEGIN 
    DECLARE counter INT DEFAULT 0;
    SET occurrences = 0;
    
    WHILE counter < loops DO
		SELECT count(*) 
        INTO occurrences
        FROM table1
        WHERE num=target;
        SET counter = counter + 1;
	END WHILE;
END$$
DELIMITER ;

-- 28.953 sec
-- 0.141 sec with index
-- CALL mySelectTest(50, 1000, @occurrences);
-- SELECT @occurrences;



-- Part 2
DROP TABLE IF EXISTS candy_matview;
DELETE FROM candy_purchase WHERE purch_id=100;

CREATE TABLE candy_matview AS
SELECT cust_name, cust_type_desc, prod_desc, pounds
FROM candy_customer 
INNER JOIN candy_cust_type
INNER JOIN candy_purchase
INNER JOIN candy_product
WHERE candy_customer.cust_type = candy_cust_type.cust_type 
AND candy_customer.cust_id = candy_purchase.cust_id
AND candy_purchase.prod_id = candy_product.prod_id
ORDER BY cust_name;

select * from candy_matview;

DROP TRIGGER IF EXISTS after_purchase_insert;

DELIMITER $$
CREATE TRIGGER after_purchase_insert
    AFTER INSERT
    ON candy_purchase FOR EACH ROW
BEGIN
    INSERT INTO candy_matview VALUES(
    (SELECT cust_name FROM candy_customer WHERE candy_customer.cust_id = NEW.cust_id),
    (SELECT cust_type_desc FROM candy_cust_type 
		INNER JOIN candy_customer 
		ON candy_customer.cust_id = NEW.cust_id 
		WHERE candy_cust_type.cust_type = candy_customer.cust_type),
    (SELECT prod_desc FROM candy_product WHERE candy_product.prod_id = NEW.prod_id),
    NEW.pounds    
    );
END$$    
DELIMITER ;

DELETE FROM candy_purchase WHERE purch_id=100;
INSERT INTO candy_purchase VALUES
(100,
(select prod_id from candy_product where prod_desc = 'Nuts Not Nachos'),
(select cust_id from candy_customer where cust_name = 'The Candy Kid'),
'2020-11-2',
'2020-11-6',
5.2,
'PAID');

select * from candy_matview;
select * from candy_purchase WHERE purch_id=100;

DROP TRIGGER IF EXISTS after_purchase_update;
DELIMITER $$
CREATE TRIGGER after_purchase_update
    AFTER UPDATE
    ON candy_purchase FOR EACH ROW
BEGIN
	UPDATE candy_matview SET
	cust_name = (SELECT cust_name FROM candy_customer WHERE candy_customer.cust_id = NEW.cust_id),
	cust_type_desc = (SELECT cust_type_desc FROM candy_cust_type 
		INNER JOIN candy_customer 
		ON candy_customer.cust_id = NEW.cust_id 
		WHERE candy_cust_type.cust_type = candy_customer.cust_type),
	prod_desc = (SELECT prod_desc FROM candy_product WHERE candy_product.prod_id = NEW.prod_id),
	pounds = NEW.pounds
	WHERE cust_name=(SELECT cust_name FROM candy_customer WHERE candy_customer.cust_id = OLD.cust_id)
	AND cust_type_desc = (SELECT cust_type_desc FROM candy_cust_type 
		INNER JOIN candy_customer 
		ON candy_customer.cust_id = OLD.cust_id 
		WHERE candy_cust_type.cust_type = candy_customer.cust_type)
	AND prod_desc = (SELECT prod_desc FROM candy_product WHERE candy_product.prod_id = OLD.prod_id)
	AND pounds = OLD.pounds;
END$$    
DELIMITER ;

UPDATE candy_purchase 
SET prod_id = 1, cust_id = 1, pounds = 2.5
WHERE purch_id = 100;

select * from candy_matview;
select * from candy_purchase WHERE purch_id=100;


DROP TRIGGER IF EXISTS after_purchase_delete;
DELIMITER $$
CREATE TRIGGER after_purchase_delete
    AFTER DELETE
    ON candy_purchase FOR EACH ROW
BEGIN
	DELETE FROM candy_matview
	WHERE cust_name=(SELECT cust_name FROM candy_customer WHERE candy_customer.cust_id = OLD.cust_id)
	AND cust_type_desc = (SELECT cust_type_desc FROM candy_cust_type 
		INNER JOIN candy_customer 
		ON candy_customer.cust_id = OLD.cust_id 
		WHERE candy_cust_type.cust_type = candy_customer.cust_type)
	AND prod_desc = (SELECT prod_desc FROM candy_product WHERE candy_product.prod_id = OLD.prod_id)
	AND pounds = OLD.pounds;
END$$    
DELIMITER ;

select * from candy_matview;
select * from candy_purchase WHERE purch_id=100;
DELETE FROM candy_purchase WHERE purch_id=100;

-- select * from candy_purchase;
-- select * from candy_cust_type;
-- select * from candy_product;
-- select * from candy_customer;