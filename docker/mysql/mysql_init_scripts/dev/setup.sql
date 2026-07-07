-- Revoke existing privileges
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'portfolio_user'@'%';

-- Grant user minimal privileges on "real" database
GRANT ALTER, CREATE, DELETE, DROP, INDEX, INSERT, SELECT, REFERENCES, UPDATE on portfolio_db.* to 'portfolio_user'@'%';

-- Grant user minimal privileges on test database
GRANT ALTER, CREATE, DELETE, DROP, INDEX, INSERT, SELECT, REFERENCES, UPDATE on portfolio_test_db.* to 'portfolio_user'@'%';
FLUSH PRIVILEGES;
