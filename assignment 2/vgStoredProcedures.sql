DROP PROCEDURE IF EXISTS getSales;
DELIMITER $$
CREATE PROCEDURE getSales( -- helper procedure for gameProfitByRegion and genreRankingByRegion
		IN id BIGINT, -- sales_id
        IN region VARCHAR(2), 
        OUT sales DOUBLE
)
BEGIN 
    CASE region
		WHEN 'WD' THEN 
			SET sales = 
				(SELECT TRUNCATE(na_sales+eu_sales+jp_sales+other_sales, 2) 
				FROM vg_sales WHERE sale_id=id);
		WHEN 'NA' THEN 
			SET sales = (SELECT na_sales FROM vg_sales WHERE sale_id=id);
		WHEN 'EU' THEN 
			SET sales = (SELECT eu_sales FROM vg_sales WHERE sale_id=id);
		WHEN 'JP' THEN 
			SET sales = (SELECT jp_sales FROM vg_sales WHERE sale_id=id);
	END CASE;
END$$
DELIMITER ;
-- CALL getSales(1, 'JP', @s);
-- select @s;

DROP PROCEDURE IF EXISTS gameProfitByRegion;
DELIMITER $$
CREATE PROCEDURE gameProfitByRegion(
		IN profit INT, 
		IN region VARCHAR(2)
)
BEGIN 
	DECLARE counter INT DEFAULT 0;
    DECLARE loops INT DEFAULT (SELECT count(*) FROM vg_sales);
    DECLARE id BIGINT DEFAULT 1; -- current sale_id being examined
    DECLARE sales DOUBLE;
    
	DROP TABLE IF EXISTS t;
    CREATE TABLE t (
		game_name VARCHAR(150),
		sales DOUBLE
    );
    
	WHILE counter < loops DO -- iterate through vg_sales
		IF EXISTS(SELECT * FROM vg_sales WHERE sale_id=id) THEN
			CALL getSales(id, region, sales);
			IF sales > profit THEN
				INSERT INTO t VALUES (
					(SELECT game_name FROM vg_game WHERE game_id=id),
					sales
				);
			END IF;
			SET id = id + 1;
		ELSE -- there is a hole in sale_id's
			SET id = id + 1;
		END IF;
		SET counter = counter + 1;
	END WHILE;
    
    SELECT * FROM t;
    DROP TABLE t;
END$$
DELIMITER ;
-- CALL gameProfitByRegion(10, 'EU');

DROP PROCEDURE IF EXISTS genreRankingByRegion;
DELIMITER $$
CREATE PROCEDURE genreRankingByRegion(
		IN genre VARCHAR(20),
		IN region VARCHAR(2)
)
BEGIN 
	DECLARE gid INT DEFAULT (SELECT genre_id FROM vg_genre WHERE genre_name=genre); -- target genre_id

	CASE region
		WHEN 'NA' THEN 
			WITH rankings AS (
				SELECT 
					RANK() OVER 
						(ORDER BY sum(na_sales) DESC) ranking, 
						genre_id 
				FROM vg_sales INNER JOIN vg_game
					ON vg_sales.game_id = vg_game.game_id
				GROUP BY genre_id
			)
			SELECT ranking
			FROM rankings
			WHERE gid=genre_id;
		WHEN 'EU' THEN
			WITH rankings AS (
				SELECT 
					RANK() OVER 
						(ORDER BY sum(eu_sales) DESC) ranking, 
						genre_id 
				FROM vg_sales INNER JOIN vg_game
					ON vg_sales.game_id = vg_game.game_id
				GROUP BY genre_id
			)
			SELECT ranking
			FROM rankings
			WHERE gid=genre_id;
		WHEN 'JP' THEN
			WITH rankings AS (
				SELECT 
					RANK() OVER 
						(ORDER BY sum(jp_sales) DESC) ranking, 
						genre_id 
				FROM vg_sales INNER JOIN vg_game
					ON vg_sales.game_id = vg_game.game_id
				GROUP BY genre_id
			)
			SELECT ranking
			FROM rankings
			WHERE gid=genre_id;
		WHEN 'WD' THEN
			WITH rankings AS (
				SELECT 
					RANK() OVER 
						(ORDER BY TRUNCATE(sum(na_sales+eu_sales+jp_sales+other_sales), 2) DESC) ranking, 
						genre_id 
				FROM vg_sales INNER JOIN vg_game
					ON vg_sales.game_id = vg_game.game_id
				GROUP BY genre_id
			)
			SELECT ranking
			FROM rankings
			WHERE gid=genre_id;
    END CASE;
END$$
DELIMITER ;
-- CALL genreRankingByRegion('Puzzle', 'NA');


DROP PROCEDURE IF EXISTS publishedReleases;
DELIMITER $$
CREATE PROCEDURE publishedReleases(IN publisher VARCHAR(50), IN genre VARCHAR(20))
BEGIN 
    SELECT count(*) FROM vg_game WHERE 
    genre_id=(SELECT genre_id FROM vg_genre WHERE genre_name=genre) 
    AND publisher_id=(SELECT publisher_id FROM vg_publisher WHERE publisher_name=publisher);
END$$
DELIMITER ;
-- CALL publishedReleases('Electronic Arts', 'Sports');


DROP PROCEDURE IF EXISTS addNewRelease;
DELIMITER $$
CREATE PROCEDURE addNewRelease(
		IN game VARCHAR(150), 
		IN platform VARCHAR(4), 
        IN genre VARCHAR(20),
        IN publisher VARCHAR(50)
)
BEGIN     
    IF NOT EXISTS(SELECT * FROM vg_game WHERE game_name=game) THEN
		-- Game is new.
        -- If genre, publisher, and platform don't exist, insert them into their respective table.
        IF NOT EXISTS(SELECT * FROM vg_genre WHERE genre_name=genre) THEN
			INSERT INTO vg_genre (genre_name) VALUES(genre);
		END IF;
		IF NOT EXISTS(SELECT * FROM vg_publisher WHERE publisher_name=publisher) THEN
			INSERT INTO vg_publisher (publisher_name) VALUES(publisher); 
		END IF;
		IF NOT EXISTS(SELECT * FROM vg_platform WHERE platform_name=platform) THEN
			INSERT INTO vg_platform (platform_name) VALUES(platform); 
		END IF;
        -- Insert new game
		INSERT INTO vg_game (game_name, genre_id, publisher_id) VALUES(
			game,
            (SELECT genre_id FROM vg_genre WHERE genre_name=genre),
            (SELECT publisher_id FROM vg_publisher WHERE publisher_name=publisher)
        ); 
        SELECT CONCAT("Added new game ", game) AS Result;
	ELSE
		-- Game already exists. 
        -- Existing games cannot have new genres nor new publishers. Verify that Genre and Publisher match.
        IF (
				((SELECT genre_id FROM vg_game WHERE game_name=game) !=
				(SELECT genre_id FROM vg_genre WHERE genre_name=genre)) 
                OR
                ((SELECT publisher_id FROM vg_game WHERE game_name=game) !=
				(SELECT publisher_id FROM vg_publisher WHERE publisher_name=publisher))
        ) THEN
			-- Genre/Publisher don't match. To maintain cardinality, don't insert.
            SELECT CONCAT(game, " already exists with genre ", 
					(SELECT genre_name FROM vg_genre WHERE genre_id=
							(SELECT genre_id FROM vg_game WHERE game_name=game)
					), " and publisher ", 
                    (SELECT publisher_name FROM vg_publisher WHERE publisher_id=
							(SELECT publisher_id FROM vg_game WHERE game_name=game)
                    ) ) AS Result;
        ELSE
			-- The game exists, but Platform can potentially be new. 
            IF NOT EXISTS(SELECT * FROM vg_platform WHERE platform_name=platform) THEN
				INSERT INTO vg_platform (platform_name) VALUES(platform); 
			END IF;
        END IF;
    END IF;
END$$
DELIMITER ;