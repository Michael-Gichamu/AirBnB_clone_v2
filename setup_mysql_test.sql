-- prepares a MySQL server for the project
-- creates testing database named: hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- creates user if not exists named: hbnb_test with password: hbnb_test_pwd
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- granting all privileges on database: hbnb_test_db to user: hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES
-- granting select privileges on database: perfomance_schema to user: hbnb_test
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES
