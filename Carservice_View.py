from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox, QDialog, QComboBox

class CarServiceView(QWidget):
    def __init__(self, connection, main_window):
        super().__init__()
        self.connection = connection
        self.main_window = main_window
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout()
        title = QLabel("Car Service Table")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Adjust columns as needed for CarService
        self.table.setHorizontalHeaderLabels(['Car', 'Service', 'Employee', 'Date Completed', 'Completion Status'])

        self.load_car_service_data()

        # Set column widths
        self.table.setColumnWidth(0, 200)  # Car ID
        self.table.setColumnWidth(1, 200)  # Service ID
        self.table.setColumnWidth(2, 200)  # Employee ID
        self.table.setColumnWidth(3, 150)  # Date Completed
        self.table.setColumnWidth(4, 150)  # Completion Status

        #Add Buttons
        self.back_button = QPushButton("Back")
        self.delete_car_service_button = QPushButton("Delete service")
        self.edit_car_service_button = QPushButton("Edit Service Information")

        #Add actions to buttons
        self.delete_car_service_button.clicked.connect(self.delete_car_service)
        self.edit_car_service_button.clicked.connect(self.edit_car_service)
        self.back_button.clicked.connect(self.switch_back)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.delete_car_service_button)
        button_layout.addWidget(self.edit_car_service_button)


        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def load_car_service_data(self):
        query = """
        SELECT Car.Year, Car.Model, CarService.CarID, Service.ServiceName, Service.ServiceID,
            Employee.FirstName, Employee.LastName, Employee.EmployeeID,
            CarService.DateCompleted, CarService.CompletionStatus
        FROM CarService
        JOIN Car ON Car.CarID = CarService.CarID
        JOIN Service ON Service.ServiceID = CarService.ServiceID
        JOIN Employee ON Employee.EmployeeID = CarService.EmployeeID
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.table.setRowCount(0)

        for row_number, (year, model, car_id, service_name, service_id, first_name, last_name, employee_id, date_completed, completion_status) in enumerate(cursor):
            self.table.insertRow(row_number)
            # Format displayed text
            year_str = year.strftime('%Y') if year else "N/A"  # Get only the year part
            car_display = f"{year_str} {model} ({car_id})"
            employee_display = f"{first_name} {last_name} ({employee_id})"
            service_display = f"{service_name} ({service_id})"
            # Convert datetime to string format if not None
            date_str = date_completed.strftime('%Y-%m-%d') if date_completed else ""

            # Set each cell in the row
            self.table.setItem(row_number, 0, QTableWidgetItem(car_display))
            self.table.setItem(row_number, 1, QTableWidgetItem(service_display))
            self.table.setItem(row_number, 2, QTableWidgetItem(employee_display))
            self.table.setItem(row_number, 3, QTableWidgetItem(date_str))
            self.table.setItem(row_number, 4, QTableWidgetItem(completion_status))
        cursor.close()

    def switch_back(self):
        self.main_window.show_initial_view()

    def delete_car_service(self):
            selected_row = self.table.currentRow()
            if selected_row != -1:
                car_id_item = self.table.item(selected_row, 0)  #CarID is first column
                service_id_item = self.table.item(selected_row, 1)  
                employee_id_item = self.table.item(selected_row, 2)  
                date_completed_item = self.table.item(selected_row, 3)

                car_id = car_id_item.text()
                service_id = service_id_item.text()
                employee_id = employee_id_item.text()
                date_completed = date_completed_item.text()

                # Confirmation dialog before deleting
                reply = QMessageBox.question(self, 'Delete Car Service', f"Delete car service with ID {service_id}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Delete car service from the database
                    query = f"DELETE FROM CarService WHERE CarID = {car_id} AND ServiceID = {service_id} AND EmployeeID = {employee_id} AND DateCompleted = '{date_completed}'"
                    cursor = self.connection.cursor()
                    cursor.execute(query)
                    self.connection.commit()

                    # Remove the row from the table
                    self.table.removeRow(selected_row)
                    self.load_car_service_data()
                    QMessageBox.information(self, 'Success', 'Car service deleted successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'Please select a car service to delete.')


    def edit_car_service(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            #Set the fields to auto fill with current info
            service_id_item = self.table.item(selected_row, 0)
            car_id_item = self.table.item(selected_row, 1)
            employee_id_item = self.table.item(selected_row, 2)
            date_completed_item = self.table.item(selected_row, 3)
            completion_status_item = self.table.item(selected_row, 4)

            service_id = service_id_item.text()
            car_id = car_id_item.text()
            employee_id = employee_id_item.text()
            date_completed = date_completed_item.text()
            completion_status = completion_status_item.text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Car Service")

            layout = QVBoxLayout()

            # Widgets for editable fields
            completion_status_label = QLabel("Completion Status:")
            self.completion_status_combo = QComboBox()
            self.completion_status_combo.addItems(["in progress", "in queue", "complete"])
            self.completion_status_combo.setCurrentText(completion_status)

            submit_button = QPushButton("Update Car Service")
            submit_button.clicked.connect(lambda: self.submit_car_service_edit(service_id))

            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.reject)

            layout.addWidget(completion_status_label)
            layout.addWidget(self.completion_status_combo)
            layout.addWidget(submit_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a car service entry to edit.')

    def submit_car_service_edit(self, service_id):
        completion_status = self.completion_status_combo.currentText()

        # Update the database with the new completion status
        query = "UPDATE CarService SET CompletionStatus = %s WHERE ServiceID = %s"
        values = (completion_status, service_id)

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
            # Reload car service data after updating
            self.load_car_service_data()
            QMessageBox.information(self, 'Success', 'Car service information updated successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Failed to update car service', f'An error occurred: {str(e)}')