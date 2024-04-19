# AutoRepairsDb
Simple Python App to manage a SQL database

This database runs locally on your machine so you will need mySQL downloaded for this python app to work. 
Link to download mySQL: https://dev.mysql.com/downloads/mysql/

You must run the SQL scripts under the SQL folder to create the database, tables, and insert some starter data.

When running main in the python folder, you will be able to insert, delete, and edit all of the tables in the database. 
Note that in order to improve the UX, cars are added from the customer table rather than from the car table. Since there is a foreign key association, to add a car from the car table, you would need to have a way to select a customer to own the car. It makes more sense for you to choose a customer from the customer table and then add a new car to them. The same logic applies for adding services to cars. This is done from the car table. 

Required packages:
PyQt5
MySQL-Connector-Python
MySQL-Connector
