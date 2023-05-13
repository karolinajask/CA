# create tables 

DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS Car;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Ad;
DROP TABLE IF EXISTS Likes;

CREATE TABLE Role (
RoleId varchar(30) NOT NULL,
RoleName varchar(50) NOT NULL,
PRIMARY KEY (RoleId)
);

CREATE TABLE Car (
CarId varchar(10) NOT NULL,
Used char(1) NOT NULL,
CarModel varchar(50),
CarColour varchar(50),
PRIMARY KEY (CarId)
);

CREATE TABLE User (
UserEmail varchar(100) NOT NULL,
UserFirstName varchar(40),
UserLastName varchar(50),
UserPassword varchar(20),
RoleId varchar(30),
PRIMARY KEY (UserEmail),
FOREIGN KEY (RoleId) REFERENCES Role (RoleId)
);

CREATE TABLE Ad (
AdId varchar(15) NOT NULL,
AdDate date,
Wanted char(1),
CarID varchar(10),
PosterID varchar(100),
Price decimal,
PRIMARY KEY (AdId),  
FOREIGN KEY (CarId) REFERENCES Car (CarId),
FOREIGN KEY (PosterId) REFERENCES User (UserEmail)
);

CREATE TABLE Likes (
LikeID int NOT NULL AUTO_INCREMENT, 
AdId varchar(15),
UserEmail varchar(100),
PRIMARY KEY (LikeId),
FOREIGN KEY (AdId) REFERENCES Ad (AdId),
FOREIGN KEY (UserEmail) REFERENCES User (UserEmail)
);