use repairsdb;

-- Table: Customer
CREATE TABLE Customer (
    CustomerID SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(30) NOT NULL,
    LastName VARCHAR(30) NOT NULL,
    Phone VARCHAR(15) NOT NULL CHECK (CHAR_LENGTH(Phone) = 10 AND Phone REGEXP '^[0-9]+$'),
    Email VARCHAR(100)
);


-- Table: Car
CREATE TABLE Car (
    CarID SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    OwnerID SMALLINT UNSIGNED NOT NULL,
    Make VARCHAR(30) NOT NULL,
    Model VARCHAR(100) NOT NULL,
    Year DATE NOT NULL,
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (OwnerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table: Service
CREATE TABLE Service (
    ServiceID TINYINT AUTO_INCREMENT PRIMARY KEY,
    ServiceName VARCHAR(50) NOT NULL UNIQUE,
    ServiceCost DECIMAL(7, 2) NOT NULL DEFAULT 100.00
);
drop table service;

-- Table: Employee
CREATE TABLE Employee (
    EmployeeID SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(30) NOT NULL,
    LastName VARCHAR(30) NOT NULL,
    DateHired DATE NOT NULL,
    EndDate DATE
);

-- Table: CarService
CREATE TABLE CarService (
    CarID SMALLINT UNSIGNED NOT NULL,
    ServiceID TINYINT NOT NULL,
    EmployeeID SMALLINT UNSIGNED NOT NULL,
    DateCompleted DATETIME NOT NULL,
    CompletionStatus ENUM('in queue', 'in progress', 'complete') NOT NULL DEFAULT 'in queue',
    PRIMARY KEY (CarID, ServiceID, EmployeeID, DateCompleted),  -- Ensures uniqueness on the same service per day
    FOREIGN KEY (CarID) REFERENCES Car(CarID) ON DELETE CASCADE,
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);


DELIMITER $$

CREATE PROCEDURE AssignRandomActiveEmployee()
BEGIN
    DECLARE total_active_employees INT;
    DECLARE random_index INT;

    SELECT COUNT(*) INTO total_active_employees FROM Employee WHERE EndDate IS NULL;

    IF total_active_employees > 0 THEN
        SET random_index = FLOOR(RAND() * total_active_employees);
        SET @employee_id = (SELECT EmployeeID FROM Employee WHERE EndDate IS NULL LIMIT random_index, 1);
    ELSE
        SET @employee_id = NULL;
    END IF;
END$$

DELIMITER ;
