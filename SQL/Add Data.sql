use repairsdb;

INSERT INTO Customer (FirstName, LastName, Phone, Email) VALUES
('John', 'Doe', '1234567890', NULL),
('Jane', 'Smith', '2345678901', 'jane.smith@example.com'),
('Michael', 'Johnson', '3456789012', 'michael.johnson@example.com'),
('Emily', 'Davis', '4567890123', 'emily.davis@example.com'),
('Chris', 'Brown', '5678901234', 'chris.brown@example.com'),
('Jessica', 'Miller', '6789012345', NULL),
('Sarah', 'Wilson', '7890123456', 'sarah.wilson@example.com'),
('James', 'Moore', '8901234567', 'james.moore@example.com'),
('Jennifer', 'Taylor', '9012345678', NULL),
('William', 'Anderson', '0123456789', 'william.anderson@example.com'),
('Linda', 'Thomas', '1234509876', 'linda.thomas@example.com'),
('David', 'Jackson', '2345610987', NULL),
('Barbara', 'White', '3456721098', 'barbara.white@example.com'),
('Susan', 'Harris', '4567832109', 'susan.harris@example.com'),
('Joseph', 'Martin', '5678943210', NULL),
('Sandra', 'Thompson', '6789054321', 'sandra.thompson@example.com'),
('Kevin', 'Garcia', '7890165432', 'kevin.garcia@example.com'),
('Karen', 'Martinez', '8901276543', NULL),
('Brian', 'Robinson', '9012387654', 'brian.robinson@example.com'),
('Nancy', 'Clark', '0123498765', 'nancy.clark@example.com'),
('Betty', 'Rodriguez', '1234509876', NULL),
('Gary', 'Lewis', '2345610987', 'gary.lewis@example.com'),
('Pamela', 'Lee', '3456721098', 'pamela.lee@example.com'),
('Nicholas', 'Walker', '4567832109', NULL),
('Deborah', 'Hall', '5678943210', 'deborah.hall@example.com'),
('Edward', 'Allen', '6789054321', NULL),
('Patricia', 'Young', '7890165432', 'patricia.young@example.com'),
('Daniel', 'Hernandez', '8901276543', 'daniel.hernandez@example.com'),
('Lisa', 'King', '9012387654', NULL),
('Mark', 'Wright', '0123498765', 'mark.wright@example.com');


INSERT INTO Car (OwnerID, Make, Model, Year, IsActive)
VALUES
    (1, 'Toyota', 'Camry', '2019-01-01', TRUE),
    (2, 'Honda', 'Civic', '2018-01-01', TRUE),
    (9, 'Ford', 'Fusion', '2017-01-01', TRUE),
    (13, 'Chevrolet', 'Malibu', '2016-01-01', TRUE),
    (14, 'Nissan', 'Altima', '2015-01-01', TRUE),
    (15, 'Toyota', 'Corolla', '2014-01-01', TRUE),
    (16, 'Honda', 'Accord', '2013-01-01', TRUE),
    (17, 'Ford', 'Focus', '2012-01-01', TRUE),
    (18, 'Chevrolet', 'Impala', '2011-01-01', TRUE),
    (19, 'Nissan', 'Maxima', '2010-01-01', TRUE),
    (20, 'Toyota', 'Rav4', '2009-01-01', TRUE),
    (21, 'Honda', 'Pilot', '2008-01-01', TRUE),
    (22, 'Ford', 'Escape', '2007-01-01', TRUE),
    (23, 'Chevrolet', 'Tahoe', '2006-01-01', TRUE),
    (24, 'Nissan', 'Pathfinder', '2005-01-01', TRUE),
    (25, 'Toyota', 'Highlander', '2004-01-01', TRUE),
    (26, 'Honda', 'CR-V', '2003-01-01', TRUE),
    (27, 'Ford', 'Explorer', '2002-01-01', TRUE),
    (28, 'Chevrolet', 'Suburban', '2001-01-01', TRUE),
    (29, 'Nissan', 'Armada', '2000-01-01', TRUE),
    (30, 'Toyota', '4Runner', '1999-01-01', TRUE),
    (31, 'Honda', 'Odyssey', '1998-01-01', TRUE),
    (32, 'Ford', 'F-150', '1997-01-01', TRUE),
    (33, 'Chevrolet', 'Silverado', '1996-01-01', TRUE),
    (34, 'Nissan', 'Frontier', '1995-01-01', TRUE),
    (35, 'Toyota', 'Tacoma', '1994-01-01', TRUE),
    (36, 'Honda', 'Civic', '1993-01-01', TRUE),
    (37, 'Ford', 'Mustang', '1992-01-01', TRUE),
    (38, 'Chevrolet', 'Camaro', '1991-01-01', TRUE),
    (39, 'Nissan', 'GT-R', '1990-01-01', TRUE),
    (40, 'Toyota', 'Corolla', '1989-01-01', TRUE);



INSERT INTO Employee (FirstName, LastName, DateHired)
VALUES
    ('John', 'Smith', '2022-01-01'),
    ('Jane', 'Doe', '2021-12-15'),
    ('Michael', 'Johnson', '2021-11-30'),
    ('Emily', 'Davis', '2021-11-15'),
    ('Chris', 'Brown', '2021-10-31'),
    ('Jessica', 'Miller', '2021-10-15'),
    ('Sarah', 'Wilson', '2021-09-30'),
    ('James', 'Moore', '2021-09-15'),
    ('Jennifer', 'Taylor', '2021-08-31'),
    ('William', 'Anderson', '2021-08-15'),
    ('Linda', 'Thomas', '2021-07-31'),
    ('David', 'Jackson', '2021-07-15'),
    ('Barbara', 'White', '2021-06-30'),
    ('Susan', 'Harris', '2021-06-15'),
    ('Joseph', 'Martin', '2021-05-31'),
    ('Sandra', 'Thompson', '2021-05-15'),
    ('Kevin', 'Garcia', '2021-04-30'),
    ('Karen', 'Martinez', '2021-04-15'),
    ('Brian', 'Robinson', '2021-03-31'),
    ('Nancy', 'Clark', '2021-03-15'),
    ('Betty', 'Rodriguez', '2021-02-28'),
    ('Gary', 'Lewis', '2021-02-15'),
    ('Pamela', 'Lee', '2021-01-31'),
    ('Nicholas', 'Walker', '2021-01-15'),
    ('Deborah', 'Hall', '2020-12-31'),
    ('Edward', 'Allen', '2020-12-15'),
    ('Patricia', 'Young', '2020-11-30'),
    ('Daniel', 'Hernandez', '2020-11-15'),
    ('Lisa', 'King', '2020-10-31'),
    ('Mark', 'Wright', '2020-10-15');

INSERT INTO Service (ServiceName, ServiceCost) VALUES
('oil change', 79.99),
('tire rotation', 299.99),
('balance adjustment', 149.99),
('tire replacement', 34.99),
('brake replacement', 300.00);


INSERT INTO CarService (CarID, ServiceID, EmployeeID, DateCompleted, CompletionStatus)
SELECT
    CarID,
    FLOOR(RAND() * 5) + 1 AS ServiceID,  -- Randomly assign ServiceID between 1 and 5
    FLOOR(RAND() * 10) + 1 AS EmployeeID,  -- Randomly assign EmployeeID between 1 and 10
    NOW() AS DateCompleted,
    CASE
        WHEN RAND() < 0.5 THEN 'in queue'
        WHEN RAND() >= 0.5 AND RAND() < 0.8 THEN 'in progress'
        ELSE 'complete'
    END AS CompletionStatus
FROM Car
ORDER BY RAND()
LIMIT 30;

