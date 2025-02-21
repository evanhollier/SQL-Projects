select sum(na_sales) from vg_csv;
select sum(na_sales) from vg_sales;
select genre, sum(na_sales) from vg_csv
group by genre
order by sum(na_sales) desc;

SELECT 
	RANK() OVER 
		(ORDER BY sum(na_sales) DESC) ranking, 
		(select genre_name from vg_genre where genre_id=vg_game.genre_id) genre, sum(na_sales)
FROM vg_sales INNER JOIN vg_game
	ON vg_sales.game_id = vg_game.game_id
GROUP BY genre_id;




select (select genre_name from vg_genre where genre_id=vg_game.genre_id) genre,
na_sales,
 RANK() OVER (
order by na_sales desc
) R
from vg_sales
inner join vg_game
on vg_sales.game_id = vg_game.game_id
group by genre_id;
select * from vg_genre;

select * from vg_sales;
select * from vg_game;
select * from vg_publisher;
select * from vg_genre;
select * from vg_platform;

select * from vg_csv
group by platform
having count(platform)>1;

SELECT game_id, platform_id FROM vg_sales
GROUP BY game_id, platform_id
HAVING count(platform_id)>1;

SELECT name, publisher FROM vg_csv
GROUP BY name, publisher;

select * from vg_csv
where name='Need for Speed: Most Wanted';

select * from vg_csv
where publisher='N/A';

select name from vg_csv
group by name
having count(name)>1;

select name, genre from vg_csv
group by name, genre;

 SELECT "The data has been inserted" AS Result; 

select count(*) from vg_game where genre_id=1 AND publisher_id=1;
select * from vg_csv where publisher='Electronic Arts' AND genre='Sports';


select count(*) from vg_sales;
SELECT EXISTS(SELECT * FROM vg_sales WHERE sale_id=-1);

SELECT TRUNCATE(na_sales+eu_sales+jp_sales+other_sales, 2) FROM vg_sales WHERE sale_id=1;

