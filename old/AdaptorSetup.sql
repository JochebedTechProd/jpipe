#drop database if exists testDDL;
CREATE DATABASE testDDL;
#use testDDL;
#CREATE USER 'test'@'localhost' IDENTIFIED BY 'test';
#IF (SELECT EXISTS(SELECT 1 FROM `mysql`.`user` WHERE `user` = '{{ test }}')) = 0 THEN
#    CREATE USER '{{ test }}'@'localhost' IDENTIFIED BY '{{ test }}'
#END IF;
GRANT ALL PRIVILEGES ON testDDL.* TO 'test'@'%' with GRANT OPTION;
GRANT ALL PRIVILEGES ON testDDL.* TO 'test'@'localhost' with GRANT OPTION;

use testDDL;
drop table if exists JP_Device_Data;
CREATE TABLE JP_Device_Data
    (ROLL_NO int(3),
    NAME varchar(20),
    changed varchar(20));



#SET @dbCheck="select SCHEMA_NAME into @dbName from information_schema.SCHEMATA where SCHEMA_NAME='JpipeDB'";
#PREPARE pstmt FROM@dbCheck;
#EXECUTE pstmt;
#select @dbName from dual;
#IFNULL @dbName THEN
    #select currentdate from dual;
#ELSE
drop database if exists testDDL;
#END IF;
#
#CREATE DATABASE testDDL;
#USE testDDL;
#SET @a=(show tables like `JP_Device_Data`);
#IF @a>0 
#THEN 
    #drop table JP_Device_Data;
#END IF
#CREATE TABLE JP_Device_Data 
    #(ROLL_NO int(3),
    #NAME varchar(20),
    ##SUBJECT varchar(20));
