use repairsdb;

INSERT INTO Customer (FirstName, LastName, Phone, Email) VALUES
('John', 'Doe', '1234567890', 'john.doe@example.com'),
('Jane', 'Smith', '2345678901', 'jane.smith@example.net'),
('Alice', 'Johnson', '3456789012', 'alice.j@example.org');


INSERT INTO Employee (FirstName, LastName, DateHired, EndDate) VALUES
('Bob', 'White', '2017-05-21', NULL),
('Susan', 'Green', '2018-07-15', '2023-01-01'),
('Gary', 'Blue', '2019-11-01', NULL);

INSERT INTO Service (ServiceName, ServiceCost) VALUES
('oil change', 79.99),
('tire rotation', 299.99),
('balance adjustment', 149.99),
('tire replacement', 34.99),
('brake replacement', 300.00);


INSERT INTO Car (OwnerID, Make, Model, Year) VALUES
(1, 'Land Rover', 'Range Rover Evoque', '2018-01-01'),
(2, 'Tesla', 'Model S', '2020-01-01'),
(1, 'Toyota', 'Corolla', '2019-01-01');

INSERT INTO CarService (CarID, ServiceID, EmployeeID, DateCompleted, CompletionStatus) VALUES
(1, 1, 1, '2022-07-15 14:30:00', 'complete'),
(2, 2, 2, '2022-08-20 09:00:00', 'in progress'),
(3, 1, 3, '2022-09-25 10:00:00', 'in queue');
