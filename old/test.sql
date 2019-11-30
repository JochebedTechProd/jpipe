drop database if exists testDDL;
CREATE DATABASE testDDL;
GRANT ALL ON `testDDL`.* TO 'test'@'localhost' with GRANT OPTION;
GRANT ALL ON `testDDL`.* TO 'test'@'%' with GRANT OPTION;
use testDDL;
drop table if exists testTable;
create table testTable (
    id int,
    name char(30));
