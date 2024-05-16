CREATE DATABASE IF NOT EXISTS taskaholic_dev_db;
CREATE USER IF NOT EXISTS taskaholic_dev@localhost IDENTIFIED BY 'taskaholic_dev_pwd';
GRANT ALL PRIVILEGES ON taskaholic_dev_db.* TO taskaholic_dev@localhost;
GRANT SELECT ON performance_schema.* TO taskaholic_dev@localhost;
FLUSH PRIVILEGES;
