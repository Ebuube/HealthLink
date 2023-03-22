--  prepares a MySQL server
CREATE DATABASE IF NOT EXISTS hlink_dev_db;
CREATE USER IF NOT EXISTS 'hlink_dev'@'localhost' IDENTIFIED BY 'my_hlink1!';
GRANT ALL PRIVILEGES ON hlink_dev_db.* TO 'hlink_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hlink_dev'@'localhost';
