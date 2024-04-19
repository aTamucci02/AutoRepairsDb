from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox, QDialog, QFormLayout, QLineEdit
import mysql.connector


class EmployeeView(QWidget):
    def __init__(self, connection, main_window):
        super().__init__()
        self.connection = connection
        self.main_window = main_window
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout()
        title = QLabel("Employee Table")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Employee ID', 'First Name', 'Last Name', 'Date Hired', 'End Date'])

        self.load_employee_data()

        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)

        #Add Buttons
        self.back_button = QPushButton("Back")
        self.add_employee_button = QPushButton("Add employee")
        self.delete_employee_button = QPushButton("Delete employee")
        self.edit_employee_button = QPushButton("Edit employee Information")

        #Add actions to buttons
        self.add_employee_button.clicked.connect(self.add_employee)
        self.delete_employee_button.clicked.connect(self.delete_employee)
        self.edit_employee_button.clicked.connect(self.edit_employee)
        self.back_button.clicked.connect(self.switch_back)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_employee_button)
        button_layout.addWidget(self.delete_employee_button)
        button_layout.addWidget(self.edit_employee_button)

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def load_employee_data(self):
        query = """
        SELECT EmployeeID, FirstName, LastName, DateHired, EndDate
        FROM Employee
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(cursor):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_number, column_number, item)
        cursor.close()

    def switch_back(self):
        self.main_window.show_initial_view()

    def delete_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            employee_id_item = self.table.item(selected_row, 0) 
            employee_id = employee_id_item.text()

            # Confirmation dialog before deleting
            reply = QMessageBox.question(self, 'Delete employee', f"Delete employee with ID {employee_id}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Delete employee from the database
                query = f"DELETE FROM employee WHERE EmployeeID = {employee_id}"
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()

                # Remove the row from the table
                self.table.removeRow(selected_row)
                self.load_employee_data()
                QMessageBox.information(self, 'Success', 'employee deleted successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please select a employee to delete.')

    def add_employee(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Employee")

        form_layout = QVBoxLayout()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.date_hired_input = QLineEdit()
        self.end_date_input = QLineEdit()

        form_layout.addWidget(QLabel("First Name:"))
        form_layout.addWidget(self.first_name_input)
        form_layout.addWidget(QLabel("Last Name:"))
        form_layout.addWidget(self.last_name_input)
        form_layout.addWidget(QLabel("Date Hired (YYYY-MM-DD):"))
        form_layout.addWidget(self.date_hired_input)
        form_layout.addWidget(QLabel("End Date (Optional - YYYY-MM-DD):"))
        form_layout.addWidget(self.end_date_input)

        submit_button = QPushButton("Add")
        submit_button.clicked.connect(self.submit_employee)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)

        form_layout.addLayout(button_layout)
        dialog.setLayout(form_layout)

        dialog.exec_()

    
    def submit_employee(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_hired = self.date_hired_input.text()
        end_date = self.end_date_input.text()

        # Check if end date is empty and set it to None (NULL) if so
        end_date = None if end_date == '' else end_date

        if first_name and last_name and date_hired:
            # Insert new employee into the database
            query = f"INSERT INTO Employee (FirstName, LastName, DateHired, EndDate) VALUES (%s, %s, %s, %s)"
            values = (first_name, last_name, date_hired, end_date)  # Tuple of values for the query
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()

            # Reload employee data after adding a new employee
            self.load_employee_data()

            QMessageBox.information(self, 'Success', 'Employee added successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all required fields (First Name, Last Name, Date Hired).')




    def edit_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            employee_id_item = self.table.item(selected_row, 0)  
            first_name_item = self.table.item(selected_row, 1)  
            last_name_item = self.table.item(selected_row, 2)  
            date_hired_item = self.table.item(selected_row, 3)  
            end_date_item = self.table.item(selected_row, 4)  

            employee_id = employee_id_item.text()
            first_name = first_name_item.text()
            last_name = last_name_item.text()
            date_hired = date_hired_item.text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Employee")

            layout = QVBoxLayout()

            first_name_label = QLabel("New First Name:")
            self.first_name_input = QLineEdit(first_name)

            last_name_label = QLabel("New Last Name:")
            self.last_name_input = QLineEdit(last_name)

            date_hired_label = QLabel("New Date Hired:")
            self.date_hired_input = QLineEdit(date_hired)

            end_date_label = QLabel("New End Date:")
            self.end_date_input = QLineEdit()

            submit_button = QPushButton("Update Employee")
            submit_button.clicked.connect(lambda: self.submit_employee_edit(employee_id)) #Pass employeeID to the submit function
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.reject)

            layout.addWidget(first_name_label)
            layout.addWidget(self.first_name_input)
            layout.addWidget(last_name_label)
            layout.addWidget(self.last_name_input)
            layout.addWidget(date_hired_label)
            layout.addWidget(self.date_hired_input)
            layout.addWidget(end_date_label)
            layout.addWidget(self.end_date_input)
            layout.addWidget(submit_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()
        else:
            QMessageBox.warning(self, 'Error', 'Please select an employee to edit.')


    def submit_employee_edit(self, employee_id):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        date_hired = self.date_hired_input.text()
        end_date = self.end_date_input.text().strip()

        # Prepare values properly for SQL insertion/update
        # Convert empty string to None for SQL NULL representation
        end_date = None if not end_date else end_date

        values = (first_name, last_name, date_hired, end_date, employee_id)
        query = "UPDATE Employee SET FirstName = %s, LastName = %s, DateHired = %s, EndDate = %s WHERE EmployeeID = %s"

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
            self.load_employee_data()
            QMessageBox.information(self, 'Success', 'Employee information updated successfully!')
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Failed to update employee', f'An error occurred: {err}')