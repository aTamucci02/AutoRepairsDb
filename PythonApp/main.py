import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QMessageBox, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Customer_View import CustomerView
from Car_View import CarView
from Service_View import ServiceView
from Employee_View import EmployeeView
from Carservice_View import CarServiceView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = self.connect_to_database()
        self.setWindowTitle('Auto Repair Shop')
        self.setGeometry(100, 100, 800, 600)
        self.initializeUI()
        self.views = {}

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                user='root', password='Parkeradam10!', host='localhost',
                database='repairsdb', port='3306'
            )
            return connection
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Connection Error", f"Failed to connect to the database: {err}")
            sys.exit(1)

    def initializeUI(self):
        layout = QVBoxLayout()

        # Information label at the top
        info_label = QLabel("Welcome to the auto repair shop. You can select, edit, and add customer, cars, employees, services, and tasks to the database from here.")
        info_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        info_label.setFont(font)
        layout.addWidget(info_label)

        # Initialize the stacked widget
        self.stacked_widget = QStackedWidget()
        self.container = QWidget()
        self.container.setLayout(layout)

        self.buttons = {
            "Car": QPushButton("Car Table"),
            "Customer": QPushButton("Customer Table"),
            "Service": QPushButton("Service Table"),
            "Employee": QPushButton("Employee Table"),
            "CarService": QPushButton("Car Service Table")
        }

        # Add a stretch factor at the top to push all content to the bottom
        layout.addStretch(1)

        # Add each button to the layout and a minimal stretch between them to distribute them evenly
        for key, button in self.buttons.items():
            button.clicked.connect(lambda checked, b=key: self.show_table_view(globals()[b + "View"]))
            layout.addWidget(button)
            layout.addStretch(1)  # Adds a small stretch factor after each button, set to 0 for minimal spacing

        # Add one last stretch at the bottom to balance the layout, if desired
        # layout.addStretch(1)

        self.stacked_widget.addWidget(self.container)
        self.setCentralWidget(self.stacked_widget)

    def show_table_view(self, view_class):
        view_name = view_class.__name__.lower()
        if view_name not in self.views:
            view_instance = view_class(self.connection, self)
            self.views[view_name] = view_instance
            self.stacked_widget.addWidget(view_instance)
            if view_name == 'customerview':
                view_instance.car_added.connect(self.handle_car_added)
            if view_name == 'carview':
                view_instance.task_added.connect(self.handle_task_added)
                view_instance.car_deleted.connect(self.handle_car_deleted)
                view_instance.car_edited.connect(self.handle_car_edited)
            if view_name == 'customerview':
                view_instance.customer_deleted.connect(self.handle_customer_deleted)
                view_instance.customer_edited.connect(self.handle_customer_edited)

        self.stacked_widget.setCurrentWidget(self.views[view_name])

    def handle_car_added(self):
        if 'carview' in self.views:
            self.views['carview'].load_car_data()
    def handle_car_deleted(self):
        if 'carserviceview' in self.views:
            self.views['carserviceview'].load_car_service_data()
    def handle_car_edited(self):
        if 'carserviceview' in self.views:
            self.views['carserviceview'].load_car_service_data()


    
    def handle_task_added(self):
        if 'carserviceview' in self.views:
            self.views['carserviceview'].load_car_service_data()
    
    
    def handle_customer_deleted(self, customer_id):
        if 'carview' in self.views:
            self.views['carview'].load_car_data()  # Reload car data
        if 'carserviceview' in self.views:
            self.views['carserviceview'].load_car_service_data()  # Reload car service data

    def handle_customer_edited(self):
        if 'carview' in self.views:
            self.views['carview'].load_car_data()  # Reload car data


    def show_initial_view(self):
        self.stacked_widget.setCurrentWidget(self.container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
