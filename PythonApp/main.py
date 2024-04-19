import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QMessageBox, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Car_View import CarView
from Customer_View import CustomerView
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
        # Initialize the main layout
        layout = QVBoxLayout()

        # Information label at the top
        info_label = QLabel("Welcome to the auto repair shop. You can select, edit, and add customer, cars, employees, services, and tasks to the database from here. \n \n Note that in order to add cars, you must do that from the customer table. To add services to cars, do that from the car table")
        info_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        info_label.setFont(font)
        layout.addWidget(info_label, alignment=Qt.AlignTop)

        # Initialize the stacked widget
        self.stacked_widget = QStackedWidget()
        self.container = QWidget()
        self.container.setLayout(layout)
        self.stacked_widget.addWidget(self.container)

        # Define buttons
        self.buttons = {
            "Car": QPushButton("Car Table"),
            "Customer": QPushButton("Customer Table"),
            "Service": QPushButton("Service Table"),
            "Employee": QPushButton("Employee Table"),
            "CarService": QPushButton("Car Service Table")
        }

        # Add stretch to ensure the buttons are distributed evenly
        layout.addStretch(1)  # Adds a stretch factor above the buttons to ensure even spacing

        # Connect buttons to show_table_view method and add them to the layout with a stretch between them
        for key, button in self.buttons.items():
            button.clicked.connect(lambda checked, b=key: self.show_table_view(globals()[b + "View"]))
            layout.addWidget(button)
            layout.addStretch(1)  # Adds a stretch factor after each button to ensure even spacing

        self.container.setLayout(layout)
        self.stacked_widget.addWidget(self.container)
        self.setCentralWidget(self.stacked_widget)






    def show_table_view(self, view_class):
        if not hasattr(self, view_class.__name__.lower()):
            view = view_class(self.connection, self)
            setattr(self, view_class.__name__.lower(), view)
            self.stacked_widget.addWidget(view)
        self.stacked_widget.setCurrentWidget(getattr(self, view_class.__name__.lower()))
    
    def show_initial_view(self):
        """Switch back to the main menu (initial view)."""
        self.stacked_widget.setCurrentWidget(self.container)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
