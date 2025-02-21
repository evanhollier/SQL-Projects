-- Calls to game profit by region
call gameProfitByRegion(35, 'WD');
call gameProfitByRegion(12, 'EU');
call gameProfitByRegion(10, 'JP');
-- Calls to genre ranking by region
call genreRankingByRegion('Sports', 'WD');
call genreRankingByRegion('Role-playing', 'NA');
call genreRankingByRegion('Role-playing', 'JP');
-- Calls to published releases
call publishedReleases('Electronic Arts', 'Sports');
call publishedReleases('Electronic Arts', 'Action');
-- Calls to add new release
call addNewRelease('Foo Attacks', 'X360', 'Strategy', 'Stevenson Studios');
-- Note that to show this works properly, you will need to perform some selects 
-- based on your table design to show that the data did in fact get inserted.
SELECT * FROM vg_game WHERE game_name='Foo Attacks';
SELECT * FROM vg_platform WHERE platform_name='X360'; -- already there
SELECT * FROM vg_genre WHERE genre_name='Strategy'; -- matches genre_id of vg_game results
SELECT * FROM vg_publisher WHERE publisher_name='Stevenson Studios'; -- matches publisher_id of vg_game results