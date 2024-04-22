from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox, QDialog, QLineEdit, QComboBox

class ServiceView(QWidget):
    def __init__(self, connection, main_window):
        super().__init__()
        self.connection = connection
        self.main_window = main_window
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout()
        title = QLabel("Service Table")
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Service table has three columns
        self.table.setHorizontalHeaderLabels(['Service ID', 'Service Name', 'Service Cost'])

        self.load_service_data()

        self.table.setColumnWidth(1, 200)


        # Buttons for Service table operations
        self.back_button = QPushButton("Back")
        self.add_service_button = QPushButton("Add Service")
        self.delete_service_button = QPushButton("Delete Service")
        self.edit_service_button = QPushButton("Edit Service Information")
       
        # Connect buttons to their functions
        self.add_service_button.clicked.connect(self.add_service)
        self.delete_service_button.clicked.connect(self.delete_service)
        self.edit_service_button.clicked.connect(self.edit_service)
        self.back_button.clicked.connect(self.switch_back)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_service_button)
        button_layout.addWidget(self.delete_service_button)
        button_layout.addWidget(self.edit_service_button)

        #Add button layout to main layout
        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def load_service_data(self):
        query = """
        SELECT ServiceID, ServiceName, ServiceCost
        FROM Service
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(cursor):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_number, column_number, item)

    def switch_back(self):
        self.main_window.show_initial_view() 

    def delete_service(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            service_id_item = self.table.item(selected_row, 0)  # Service ID is in the first column
            service_id = service_id_item.text()

            # Confirmation dialog before deleting
            reply = QMessageBox.question(self, 'Delete Service', f"Delete service with ID {service_id}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Delete service from the database
                query = f"DELETE FROM Service WHERE ServiceID = {service_id}"
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()

                # Remove the row from the table
                self.table.removeRow(selected_row)
                self.load_service_data()
                QMessageBox.information(self, 'Success', 'Service deleted successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please select a service to delete.')

    def add_service(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Service")

        form_layout = QVBoxLayout()
        self.service_name_input = QLineEdit()
        self.service_cost_input = QLineEdit()

        form_layout.addWidget(QLabel("Service Name:"))
        form_layout.addWidget(self.service_name_input)
        form_layout.addWidget(QLabel("Service Cost:"))
        form_layout.addWidget(self.service_cost_input)

        submit_button = QPushButton("Add")
        submit_button.clicked.connect(self.submit_service)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)

        form_layout.addLayout(button_layout)
        dialog.setLayout(form_layout)

        dialog.exec_()

    def submit_service(self):
        service_name = self.service_name_input.text()
        service_cost = self.service_cost_input.text()

        if service_name and service_cost:
            # Insert new service into the database
            query = f"INSERT INTO Service (ServiceName, ServiceCost) VALUES ('{service_name}', '{service_cost}')"
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()

            # Reload service data after adding a new service
            self.load_service_data()

            QMessageBox.information(self, 'Success', 'Service added successfully!')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all required fields (Service Name, Service Cost).')


    def edit_service(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            service_id_item = self.table.item(selected_row, 0)  
            service_name_item = self.table.item(selected_row, 1)  
            service_price_item = self.table.item(selected_row, 2)  

            service_id = service_id_item.text()
            service_name = service_name_item.text()
            service_price = service_price_item.text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Service")

            layout = QVBoxLayout()

            service_name_label = QLabel("New Service Name:")
            self.service_name_input = QLineEdit(service_name)

            price_label = QLabel("New Price:")
            self.price_input = QLineEdit(service_price)

            submit_button = QPushButton("Update Service")
            submit_button.clicked.connect(lambda: self.submit_service_edit(service_id, self.service_name_input.text(), self.price_input.text()))
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.reject)

            layout.addWidget(service_name_label)
            layout.addWidget(self.service_name_input)
            layout.addWidget(price_label)
            layout.addWidget(self.price_input)
            layout.addWidget(submit_button)
            layout.addWidget(cancel_button)

            dialog.setLayout(layout)
            dialog.exec_()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a service to edit.')

    def submit_service_edit(self, service_id, new_name, new_price):
        # Update service name and price in the database
        query = f"UPDATE Service SET ServiceName = '{new_name}', ServiceCost = {new_price} WHERE ServiceID = {service_id}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        #reload the table after edit is successful
        self.load_service_data()

        QMessageBox.information(self, 'Success', 'Service updated successfully!')