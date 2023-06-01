CREATE SCHEMA ca ;

use ca;

#code used to create tables 

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

CREATE TABLE User (
UserEmail varchar(100) NOT NULL,
UserFirstName varchar(40),
UserLastName varchar(50),
UserPassword TEXT,
RoleId varchar(30),
PRIMARY KEY (UserEmail),
FOREIGN KEY (RoleId) REFERENCES Role (RoleId)
);

CREATE TABLE Ad (
AdId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
AdDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
Wanted char(1),
CarID varchar(10),
PosterID varchar(100),
Price decimal,
Used char(1) NOT NULL,
CarModel varchar(50),
CarColour varchar(50),
FOREIGN KEY (PosterId) REFERENCES User (UserEmail)
);

CREATE TABLE Likes (
LikeID int NOT NULL AUTO_INCREMENT, 
AdId int,
UserEmail varchar(100),
PRIMARY KEY (LikeId),
FOREIGN KEY (AdId) REFERENCES Ad (AdId),
FOREIGN KEY (UserEmail) REFERENCES User (UserEmail)
);

INSERT INTO Role (RoleID, RoleName)
VALUES ('buyer', 'buyer'),
('seller', 'seller'),
('admin', 'admin');