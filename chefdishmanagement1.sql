USE chefdishmanagement;

CREATE TABLE Chef (
    ChefID INT PRIMARY KEY,
    Name VARCHAR(50),
    Specialty VARCHAR(100),
    Password VARCHAR(50)
);
CREATE TABLE Dish (
    DishID INT PRIMARY KEY,
    Name VARCHAR(50),
    ChefID INT,
    Description VARCHAR(255),
    FOREIGN KEY (ChefID) REFERENCES Chef(ChefID)
);
CREATE TABLE Admin (
    AdminID INT PRIMARY KEY,
    Name VARCHAR(50),
    Password VARCHAR(50)
);
INSERT INTO Chef (ChefID, Name, Specialty, Password) VALUES (1, 'Chef A', 'Chinese Cuisine', 'password1');
INSERT INTO Chef (ChefID, Name, Specialty, Password) VALUES (2, 'Chef B', 'Italian Cuisine', 'password2');
INSERT INTO Dish (DishID, Name, ChefID, Description) VALUES (1, 'Dish A', 1, 'This is a delicious Chinese dish.');
INSERT INTO Dish (DishID, Name, ChefID, Description) VALUES (2, 'Dish B', 2, 'This is a delicious Italian dish.');
INSERT INTO Admin (AdminID, Name, Password) VALUES (1, 'Admin A', 'adminpassword1');
INSERT INTO Chef (ChefID, Name, Specialty, Password) VALUES (1, 'Chef A', 'Chinese Cuisine', 'password1');
INSERT INTO Dish (DishID, Name, ChefID, Description) VALUES (1, 'Dish A', 1, 'This is a delicious Chinese dish.');

DESC my_table;
