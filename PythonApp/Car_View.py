from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox, QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import Qt, QDate, pyqtSignal
import mysql.connector
import random

class CarView(QWidget):
    task_added = pyqtSignal()  # Define a signal for task addition
    car_deleted = pyqtSignal()
    car_edited = pyqtSignal()

    def __init__(self, connection, main_window):
        super().__init__()
        self.connection = connection
        self.main_window = main_window  
        self.initializeUI()

    def initializeUI(self):
        self.layout = QVBoxLayout()
        title = QLabel("Car Table")
        title.setAlignment(Qt.AlignCenter)
        
        # Set up the table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Car ID', 'Owner (ID)', 'Make', 'Model', 'Year', 'IsActive'])
        self.load_car_data()

        self.table.setColumnWidth(1, 150) 
        self.table.setColumnWidth(2, 150) 
        self.table.setColumnWidth(3, 200)  



        # Buttons for Car table operations
        self.add_task_button = QPushButton("Add Task")
        self.delete_car_button = QPushButton("Delete Car")
        self.edit_car_button = QPushButton("Edit Car Information")
        self.back_button = QPushButton("Back")

        # Connect buttons to their functions
        self.back_button.clicked.connect(self.switch_back)
        self.add_task_button.clicked.connect(self.add_task)
        self.delete_car_button.clicked.connect(self.delete_car)
        self.edit_car_button.clicked.connect(self.edit_car)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_task_button)
        button_layout.addWidget(self.delete_car_button)
        button_layout.addWidget(self.edit_car_button)
        
        # Add widgets to the layout
        self.layout.addWidget(title)
        self.layout.addWidget(self.table)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)

    def load_car_data(self):
        query = """
        SELECT Car.CarID, Customer.FirstName, Customer.LastName, Customer.CustomerID, Car.Make, Car.Model, Car.Year, Car.IsActive
        FROM Car
        JOIN Customer ON Car.OwnerID = Customer.CustomerID
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(cursor):
            self.table.insertRow(row_number)
            owner_info = f"{row_data[1]} {row_data[2]} ({row_data[3]})"
            is_active = "Yes" if row_data[7] else "No"
            values = [row_data[0], owner_info, row_data[4], row_data[5], row_data[6].strftime('%Y'), is_active]

            for column_number, data in enumerate(values):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_number, column_number, item)
        cursor.close()

    def switch_back(self):
        self.main_window.show_initial_view()  

    def add_task(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            car_id_item = self.table.item(selected_row, 0)  # Car ID is in the first column
            car_id = car_id_item.text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Add Task")

            layout = QVBoxLayout()

            task_label = QLabel("Select Task:")
            task_combo = QComboBox()
            
            # Retrieve all service names from the Service table
            query = "SELECT ServiceName FROM Service"
            cursor = self.connection.cursor()
            cursor.execute(query)
            services = [service[0] for service in cursor.fetchall()]  # Fetch all service names
            
            task_combo.addItems(services)  # Populate the dropdown menu with service names

            submit_button = QPushButton("Add Task")
            submit_button.clicked.connect(lambda: self.submit_task(car_id, task_combo.currentText()))
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.reject)

            layout.addWidget(task_label)
            layout.addWidget(task_combo)
            layout.addWidget(submit_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a car to add a task.')


    def submit_task(self, car_id, task_name):
        # Insert task (service) for the selected car into the database
        query = f"INSERT INTO CarService (CarID, ServiceID, EmployeeID, DateCompleted, CompletionStatus) VALUES ({car_id}, (SELECT ServiceID FROM Service WHERE ServiceName = '{task_name}'), 1, NOW(), 'in queue')"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        self.task_added.emit()  # Emit the signal after adding the task

        QMessageBox.information(self, 'Success', f'Task "{task_name}" added to Car ID {car_id} successfully!')


        
    def delete_car(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            car_id_item = self.table.item(selected_row, 0)  # Car ID is in the first column
            car_id = car_id_item.text()

            # Confirmation dialog before deleting
            reply = QMessageBox.question(self, 'Delete Car', f"Delete car with ID {car_id}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Delete car from the database
                query = f"DELETE FROM Car WHERE CarID = {car_id}"
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()

                # Remove the row from the table
                self.table.removeRow(selected_row)
                self.load_car_data()
                QMessageBox.information(self, 'Success', 'Car deleted successfully!')
                self.car_deleted.emit()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a car to delete.')

    def edit_car(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            car_id_item = self.table.item(selected_row, 0) 
            make_item = self.table.item(selected_row, 2)  #  Make 
            model_item = self.table.item(selected_row, 3)  #  Model 
            year_item = self.table.item(selected_row, 4)  #  Year 
            owner_item = self.table.item(selected_row, 1)  #  Owner
            is_active_item = self.table.item(selected_row, 5)  #  IsActive

            car_id = car_id_item.text()
            make = make_item.text()
            model = model_item.text()
            year = year_item.text()
            owner = owner_item.text()
            is_active = is_active_item.text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Car")

            layout = QVBoxLayout()

            make_label = QLabel("New Make:")
            self.make_input = QLineEdit(make)

            model_label = QLabel("New Model:")
            self.model_input = QLineEdit(model)

            year_label = QLabel("New Year:")
            self.year_input = QLineEdit(year)

            is_active_label = QLabel("Is Active:")
            self.is_active_combo = QComboBox()
            self.is_active_combo.addItems(["True", "False"])  
            self.is_active_combo.setCurrentText(is_active)

            submit_button = QPushButton("Update Car")
            submit_button.clicked.connect(lambda: self.submit_car_edit(car_id))
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.reject)

            layout.addWidget(make_label)
            layout.addWidget(self.make_input)
            layout.addWidget(model_label)
            layout.addWidget(self.model_input)
            layout.addWidget(year_label)
            layout.addWidget(self.year_input)
            layout.addWidget(is_active_label)
            layout.addWidget(self.is_active_combo)
            layout.addWidget(submit_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a car to edit.')

    def submit_car_edit(self, car_id):
        make = self.make_input.text()
        model = self.model_input.text()
        year = self.year_input.text()
        is_active_text = self.is_active_combo.currentText()  # Get the selected text from the combo box

        # Map the text to 1 (True) or 0 (False) for database storage
        is_active = 1 if is_active_text == "True" else 0

        if make and model and year:
            try:
                # Convert year to a date (first day of the year)
                year_date = QDate(int(year), 1, 1)
                year_str = year_date.toString(Qt.ISODate)

                # Update car information in the database
                query = f"UPDATE Car SET Make = '{make}', Model = '{model}', Year = '{year_str}', IsActive = {is_active} WHERE CarID = {car_id}"
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                self.load_car_data()

                QMessageBox.information(self, 'Success', 'Car information updated successfully!')
                self.car_edited.emit()
            except ValueError:
                QMessageBox.warning(self, 'Error', 'Invalid year format. Please enter a valid 4-digit year.')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all required fields (Make, Model, Year).')
