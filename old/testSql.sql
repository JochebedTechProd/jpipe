drop database if exists test07;
CREATE DATABASE test07;
GRANT ALL PRIVILEGES ON test07.* TO 'test'@'%' with GRANT OPTION;
GRANT ALL PRIVILEGES ON test07.* TO 'test'@'localhost' with GRANT OPTION;

use test07;
drop table if exists COMP;
drop table if exists employee;
drop table if exists Dep;
CREATE TABLE COMP(
    compId int(11),
    compName char(30),
    city char(30),
    PRIMARY KEY (compId));
CREATE TABLE employee
    (empNo int(11),
    empName varchar(20),
    compId int(11),
    depId int(11),
    supervisorId int(11),
    PRIMARY KEY (empNo),
    FOREIGN KEY (compId) REFERENCES COMP(compId),
    FOREIGN KEY (supervisorId) REFERENCES employee(empNo));
CREATE TABLE Dep 
    (depId int(11),
    depName varchar(20),
    compId int(11),
    managerId int(11),
    hrId int(11),
    PRIMARY KEY (depId),
    FOREIGN KEY (compId) REFERENCES COMP(compId),
    FOREIGN KEY (managerId) REFERENCES employee(empNo),
    FOREIGN KEY (hrId) REFERENCES employee(empNo));
ALTER TABLE employee
    ADD FOREIGN KEY (depId) REFERENCES Dep(depId);
