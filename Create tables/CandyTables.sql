DROP TABLE IF EXISTS candy_purchase;
DROP TABLE IF EXISTS candy_customer;
DROP TABLE IF EXISTS candy_cust_type;
DROP TABLE IF EXISTS candy_product;

CREATE TABLE candy_cust_type
(cust_type CHAR(1) PRIMARY KEY,
cust_type_desc VARCHAR(10));

CREATE TABLE candy_customer
(cust_id BIGINT AUTO_INCREMENT PRIMARY KEY,
cust_name VARCHAR(30),
cust_type CHAR(1),
cust_addr VARCHAR(30),
cust_zip VARCHAR(15),
cust_phone VARCHAR(15),
username VARCHAR(30),
password VARCHAR(8),
CONSTRAINT candy_customer_cust_type_fk FOREIGN KEY (cust_type) REFERENCES candy_cust_type(cust_type));

CREATE TABLE candy_product(
  prod_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  prod_desc VARCHAR(30),
  prod_cost DECIMAL(5,2),
  prod_price DECIMAL(5,2)
);

CREATE TABLE candy_purchase(
  purch_id BIGINT,
  prod_id BIGINT,
  cust_id BIGINT,
  purch_date DATE,
  delivery_date DATE,
  pounds FLOAT,
  status VARCHAR(10),
  CONSTRAINT candy_purchase_prod_id_fk FOREIGN KEY (prod_id) REFERENCES candy_product(prod_id),
  CONSTRAINT candy_customer_cust_id_fk FOREIGN KEY (cust_id) REFERENCES candy_customer(cust_id),
  CONSTRAINT candy_purch_purch_prod_id_pk PRIMARY KEY (purch_id, prod_id, cust_id)
);

-- insert values into candy_cust_type
-- this must be done prior to inserting into candy_customer
INSERT INTO candy_cust_type VALUES ('P', 'Private');
INSERT INTO candy_cust_type VALUES ('R', 'Retail');
INSERT INTO candy_cust_type VALUES ('W', 'Wholesale');

-- insert values into candy_customer
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Joe Jones', 'P', '1234 Main Street', '91212', '434-1231', 'jonesj', '1234');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Armstrong, Inc.', 'R', '231 Globe Blvd', '91212', '434-7664', 'armstrong', '3333');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Swedish Burgers', 'R', '1889 20th N.E.', '91213', '434-9090', 'swedburg', '2353');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Pickled Pickles', 'R', '194 CityView', '91289', '324-8909', 'pickpick', '5333');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('The Candy Kid', 'W', '2121 Main St.', '91212', '583-4545', 'kidcandy', '2351');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Waterman, Al', 'P', '23 Yankee Blvd.', '91234', NULL, 'wateral', '8900');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Bobby Bon Bons', 'R', '12 NichiCres.', '91212', '434-9045', 'bobbybon', '3011');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Crowsh, Elias', 'P', '7 77th Ave.', '91211', '434-0007', 'crowel', '1033');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Montag, susie', 'P', '981 Montview', '91213', '456-2091', 'montags', '9633');
INSERT INTO candy_customer (cust_name, cust_type, cust_addr, cust_zip, cust_phone, username, password) VALUES
('Columberg Sweets', 'W', '239 East Falls', '91209', '874-9092', 'columswe', '8399');

-- insert values into candy_product
INSERT INTO candy_product (prod_desc, prod_cost, prod_price) VALUES('Celestial Cashew Crunch', 7.45, 10);
INSERT INTO candy_product (prod_desc, prod_cost, prod_price) VALUES('Unbrittle Peanut Paradise', 5.75, 9);
INSERT INTO candy_product (prod_desc, prod_cost, prod_price) VALUES('Mystery Melange', 7.75, 10.50);
INSERT INTO candy_product (prod_desc, prod_cost, prod_price) VALUES('Millionaire''s Macadamia Mix', 12.50, 16);
INSERT INTO candy_product (prod_desc, prod_cost, prod_price) VALUES('Nuts Not Nachos', 6.25, 9.50);
INSERT INTO candy_product (prod_desc, prod_cost, prod_price) VALUES('Chocolate Excess', 15.25, 20.50);

-- insert values into candy_purchase
INSERT INTO candy_purchase VALUES (1, 1, 5, '2007-9-6', '2007-9-6', 3.5, 'PAID');
INSERT INTO candy_purchase VALUES (2, 2, 6, '2007-9-6', '2007-9-7', 15, 'PAID');
INSERT INTO candy_purchase VALUES (3, 1, 9, '2007-9-6', '2007-9-6', 2, 'PAID');
INSERT INTO candy_purchase VALUES (3, 3, 9, '2007-9-6', '2007-9-7', 3.7, 'PAID');
INSERT INTO candy_purchase VALUES (4, 3, 2, '2007-9-6', NULL, 3.7, 'PAID');
INSERT INTO candy_purchase VALUES (5, 1, 7, '2007-9-6', '2007-9-6', 3.7, 'NOT PAID');
INSERT INTO candy_purchase VALUES (5, 2, 7, '2007-9-6', '2007-9-6', 1.2, 'NOT PAID');
INSERT INTO candy_purchase VALUES (5, 3, 7, '2007-9-7', '2007-9-7', 4.4, 'NOT PAID');
INSERT INTO candy_purchase VALUES (6, 2, 7, '2007-9-7', NULL, 3, 'PAID');
INSERT INTO candy_purchase VALUES (7, 2, 10, '2007-9-7', NULL, 14, 'NOT PAID');
INSERT INTO candy_purchase VALUES (7, 5, 10, '2007-9-7', NULL, 4.8, 'NOT PAID');
INSERT INTO candy_purchase VALUES (8, 1, 4, '2007-9-7', '2007-9-8', 1, 'PAID');
INSERT INTO candy_purchase VALUES (8, 5, 4, '2007-9-7', NULL, 7.6, 'PAID');
INSERT INTO candy_purchase VALUES (9, 5, 4, '2007-9-7', '2007-9-8', 3.5, 'NOT PAID');
