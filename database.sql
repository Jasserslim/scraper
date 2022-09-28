DROP DATABASE IF EXISTS scraper_db;    

CREATE DATABASE scraper_db;    

\c scraper_db;  
set search_path to <public>      
CREATE TABLE Data (
ID SERIAL PRIMARY KEY,
Name_page varchar(20),
Date_post timestamp,
Post varchar(500),
Likes INT(20),
Comments INT(20),
Shares INT(20),

);   