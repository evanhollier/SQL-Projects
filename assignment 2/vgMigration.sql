-- DROP EXISTING TABLES --
DROP TABLE IF EXISTS vg_sales;
DROP TABLE IF EXISTS vg_game;
DROP TABLE IF EXISTS vg_genre;
DROP TABLE IF EXISTS vg_publisher;
DROP TABLE IF EXISTS vg_platform;

-- Create Table Script --
CREATE TABLE vg_genre (
	genre_id BIGINT AUTO_INCREMENT PRIMARY KEY,
	genre_name VARCHAR(20) -- longest existing genre is 12
);

CREATE TABLE vg_publisher (
	publisher_id BIGINT AUTO_INCREMENT PRIMARY KEY,
	publisher_name VARCHAR(50) -- longest existing name is 38
);

CREATE TABLE vg_platform (
	platform_id BIGINT AUTO_INCREMENT PRIMARY KEY,
	platform_name VARCHAR(4) -- longest existing platform is 4
);

CREATE TABLE vg_game (
	game_id BIGINT AUTO_INCREMENT PRIMARY KEY,
	game_name VARCHAR(150) UNIQUE, -- longest existing game is 132
	genre_id BIGINT,
	publisher_id BIGINT,
    -- CONSTRAINT test UNIQUE (game_name, publisher_id),
	CONSTRAINT genre_id_fk FOREIGN KEY (genre_id) REFERENCES vg_genre(genre_id),
	CONSTRAINT publisher_id_fk FOREIGN KEY (publisher_id) REFERENCES vg_publisher(publisher_id)
);

CREATE TABLE vg_sales (
	sale_id BIGINT AUTO_INCREMENT PRIMARY KEY,
	game_id BIGINT,
	platform_id BIGINT,
	year INT,
	na_sales DOUBLE, 
	eu_sales DOUBLE, 
	jp_sales DOUBLE, 
	other_sales DOUBLE, 

	CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES vg_game(game_id),
	CONSTRAINT platform_id_fk FOREIGN KEY (platform_id) REFERENCES vg_platform(platform_id)
);


-- DATA MIGRATION -- 
INSERT INTO vg_genre (genre_name)
	(SELECT genre FROM vg_csv
	GROUP BY genre);

INSERT INTO vg_publisher (publisher_name)
	(SELECT publisher FROM vg_csv
	GROUP BY publisher);
-- SELECT * FROM vg_publisher WHERE publisher_name='N/A';
-- Some publisher data is missing.

INSERT INTO vg_platform (platform_name)
	(SELECT platform FROM vg_csv
	GROUP BY platform);

INSERT IGNORE INTO vg_game (game_name, genre_id, publisher_id)
	SELECT name,
    (SELECT genre_id FROM vg_genre WHERE genre_name = genre), 
	(SELECT publisher_id FROM vg_publisher WHERE publisher_name = publisher)
    FROM vg_csv;
-- SELECT count(*) FROM vg_game GROUP BY game_name HAVING count(*)>1;
-- SHOW WARNINGS;
    
INSERT INTO vg_sales (game_id, platform_id, year, na_sales, eu_sales, jp_sales, other_sales)
	(SELECT 
		(SELECT game_id FROM vg_game WHERE game_name = name), 
		(SELECT platform_id FROM vg_platform WHERE platform_name = platform), 
        (CASE
			WHEN year = 'N/A' THEN 0 -- Set missing year data to 0.
            ELSE year
		END),
        na_sales, eu_sales, jp_sales, other_sales
    FROM vg_csv);