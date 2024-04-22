from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox, QDialog, QFormLayout, QLineEdit
import mysql.connector
from Car_View import CarView


class CustomerView(QWidget):
    customer_deleted = pyqtSignal(str)
    customer_edited = pyqtSignal()
    car_added = pyqtSignal()  # Signal to notify that a car has been added
    def __init__(self, connection, main_window):
        super().__init__()
        self.connection = connection
        self.main_window = main_window
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout()
        title = QLabel("Customer Table")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5) 
        self.table.setHorizontalHeaderLabels(['Customer ID', 'First Name', 'Last Name', 'Phone', 'Email'])
        self.load_customer_data()

        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(4, 250)


        # Add Buttons
        self.back_button = QPushButton("Back")
        self.add_customer_button = QPushButton("Add Customer")
        self.delete_customer_button = QPushButton("Delete Customer")
        self.edit_customer_button = QPushButton("Edit Customer Information")
        self.add_car_button = QPushButton("Add Car") 

        # Add actions to buttons
        self.add_customer_button.clicked.connect(self.add_customer)
        self.delete_customer_button.clicked.connect(self.delete_customer)
        self.edit_customer_button.clicked.connect(self.edit_customer)
        self.back_button.clicked.connect(self.switch_back)
        self.add_car_button.clicked.connect(self.add_car) 

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_customer_button)
        button_layout.addWidget(self.delete_customer_button)
        button_layout.addWidget(self.edit_customer_button)
        button_layout.addWidget(self.add_car_button)  
        button_layout.addWidget(self.back_button)  

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        self.setLayout(layout)


    def load_customer_data(self):
        query = """
        SELECT CustomerID, FirstName, LastName, Phone, Email
        FROM Customer
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.table.setRowCount(0)

        for row_number, (customer_id, first_name, last_name, phone, email) in enumerate(cursor):
            self.table.insertRow(row_number)
            values = [customer_id, first_name, last_name, phone, email]
            
            for column_number, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_number, column_number, item)
        cursor.close()

    def switch_back(self):
        self.main_window.show_initial_view()  

    def delete_customer(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            customer_id_item = self.table.item(selected_row, 0) 
            customer_id = customer_id_item.text()

            # Confirmation dialog before deleting
            reply = QMessageBox.question(self, 'Delete Customer', f"Delete customer with ID {customer_id}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Delete customer from the database
                query = f"DELETE FROM Customer WHERE CustomerID = {customer_id}"
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()

                # Remove the row from the table
                self.table.removeRow(selected_row)
                self.load_customer_data()
                self.customer_deleted.emit(customer_id)
                QMessageBox.information(self, 'Success', 'Customer deleted successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please select a customer to delete.')

    def add_customer(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Customer")

        form_layout = QFormLayout()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("Email (Optional):", self.email_input)

        submit_button = QPushButton("Add")
        submit_button.clicked.connect(self.submit_customer)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)

        form_layout.addRow(button_layout)
        dialog.setLayout(form_layout)

        dialog.exec_()

    def submit_customer(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if first_name and last_name and phone:
            # Insert new customer into the database
            query = f"INSERT INTO Customer (FirstName, LastName, Phone, Email) VALUES ('{first_name}', '{last_name}', '{phone}', '{email}')"
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()

            # Reload customer data after adding a new customer
            self.load_customer_data()

            QMessageBox.information(self, 'Success', 'Customer added successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all required fields (First Name, Last Name, Phone).')

    
    def add_car(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            customer_id_item = self.table.item(selected_row, 0)  # Customer ID is in the first column
            customer_id = customer_id_item.text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Add Car")

            layout = QVBoxLayout()

            make_label = QLabel("Car Make:")
            self.make_input = QLineEdit()

            model_label = QLabel("Car Model:")
            self.model_input = QLineEdit()

            year_label = QLabel("Car Year:")
            self.year_input = QLineEdit()

            layout.addWidget(make_label)
            layout.addWidget(self.make_input)
            layout.addWidget(model_label)
            layout.addWidget(self.model_input)
            layout.addWidget(year_label)
            layout.addWidget(self.year_input)

            submit_button = QPushButton("Add Car")
            submit_button.clicked.connect(lambda: self.submit_car(customer_id))
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.reject)

            layout.addWidget(submit_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()

        else:
            QMessageBox.warning(self, 'Error', 'Please select a customer to add a car.')


    def submit_car(self, customer_id):
        make = self.make_input.text()
        model = self.model_input.text()
        year = self.year_input.text()

        if make and model and year:
            try:
                # Convert year to a date (first day of the year)
                year_date = QDate(int(year), 1, 1)
                year_str = year_date.toString(Qt.ISODate)

                # Insert car for the selected customer into the database
                query = f"INSERT INTO Car (OwnerID, Make, Model, Year) VALUES ({customer_id}, '{make}', '{model}', '{year_str}')"
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                self.car_added.emit()  # Emit the signal



                QMessageBox.information(self, 'Success', 'Car added successfully!')
            except ValueError:
                QMessageBox.warning(self, 'Error', 'Invalid year format. Please enter a valid 4-digit year.')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all required fields (Make, Model, Year).')


    def edit_customer(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            customer_id_item = self.table.item(selected_row, 0) 
            first_name_item = self.table.item(selected_row, 1)  
            last_name_item = self.table.item(selected_row, 2) 
            phone_item = self.table.item(selected_row, 3)
            email_item = self.table.item(selected_row, 4) 

            customer_id = customer_id_item.text()
            first_name = first_name_item.text()
            last_name = last_name_item.text()
            phone = phone_item.text()
            email = email_item.text() if email_item is not None else ""

            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Customer")

            layout = QVBoxLayout()

            first_name_label = QLabel("New First Name:")
            self.first_name_input = QLineEdit(first_name)

            last_name_label = QLabel("New Last Name:")
            self.last_name_input = QLineEdit(last_name)

            phone_label = QLabel("New Phone:")
            self.phone_input = QLineEdit(phone)

            email_label = QLabel("New Email (Optional):")
            self.email_input = QLineEdit(email)

            submit_button = QPushButton("Update Customer")
            submit_button.clicked.connect(self.submit_customer_edit)
            submit_button.setProperty("customer_id", customer_id)  
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.reject)

            layout.addWidget(first_name_label)
            layout.addWidget(self.first_name_input)
            layout.addWidget(last_name_label)
            layout.addWidget(self.last_name_input)
            layout.addWidget(phone_label)
            layout.addWidget(self.phone_input)
            layout.addWidget(email_label)
            layout.addWidget(self.email_input)
            layout.addWidget(submit_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a customer to edit.')

    def submit_customer_edit(self):
        customer_id = self.sender().property("customer_id")  # Retrieve customer_id from the clicked button's property
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        # Update customer information in the database
        query = f"UPDATE Customer SET FirstName = '{first_name}', LastName = '{last_name}', Phone = '{phone}', Email = '{email}' WHERE CustomerID = {customer_id}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

        # Reload customer data after updating the customer
        self.load_customer_data()
        self.customer_edited.emit()
        QMessageBox.information(self, 'Success', 'Customer information updated successfully!')

