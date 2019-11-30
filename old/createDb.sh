@echo off
SET dbname=testDDL
SET user=testUser
SET password=1234
SET hostinfo=localhost
SET RESULT="mysql -u root -ppassword --skip-column-names -e SHOW DATABASES LIKE '%dbname%'"

for /f "delims=" %%i in ('%RESULT%') do set RESULT=%%i

if %RESULT% == "%dbname%" (
    echo "The database already exists. You can use the reinstall function instead."
) else (
    mysql -h localhost -u root -ppassword -e "CREATE USER '%user%'@'%%'"
    mysql -h localhost -u root -ppassword -e "SET PASSWORD FOR '%user%'@'%%' = PASSWORD('%password%')"
    mysql -h localhost -u root -ppassword -e "GRANT USAGE ON * . * TO '%user%'@'%%' IDENTIFIED BY '%password%' WITH MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0"
    mysql -h localhost -u root -ppassword -e "CREATE DATABASE IF NOT EXISTS `%dbname%`"
    mysql -h localhost -u root -ppassword -e "GRANT ALL PRIVILEGES ON `%dbname%` . * TO '%user%'@'%%'"

    echo A new MySQL database has been created for you.
    echo Username: %user%
    echo Password: %password%
    echo Database: %dbname%
    echo Host: %hostinfo%:3306
)
