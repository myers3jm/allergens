DROP DATABASE IF EXISTS dunkin_allergens;
DROP USER IF EXISTS 'dunkin_admin'@'localhost';
CREATE DATABASE dunkin_allergens;
CREATE USER   'dunkin_admin'@'localhost' IDENTIFIED BY 'TODO CHANGE ME';
GRANT ALL ON dunkin_allergens.* TO 'dunkin_admin'@'localhost';