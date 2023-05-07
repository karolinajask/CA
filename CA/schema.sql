# create tables 

DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Car;
DROP TABLE IF EXISTS Ad;

CREATE TABLE User (
    UserId int NOT NULL AUTO_INCREMENT,
    UserEmail varchar(100) NOT NULL,
    UserPassword varchar(20) NOT NULL,
    UserFirstName varchar(40),
    UserLastName varchar(50),
    PRIMARY KEY (UserId)
);

CREATE TABLE Car (
    CarId varchar(10) NOT NULL,
    IsCarUsed char(1) NOT NULL,
    CarPrice decimal NOT NULL,    
    CarModel varchar(50),
    CarColour varchar(50),
    PRIMARY KEY (CarId)
);

CREATE TABLE Ad (
  AdId varchar(15), NOT NULL,
  UserId int,
  CarId varchar(10),
  PRIMARY KEY (AdId),
  FOREIGN KEY (UserId) REFERENCES User (UserId),
  FOREIGN KEY (CarId) REFERENCES Car (CarId),
);