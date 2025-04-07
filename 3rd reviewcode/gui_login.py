import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

API_URL = "http://127.0.0.1:5000/auth/login"  # Flask login API endpoint

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Jarvis")
        self.setGeometry(100, 100, 500, 400)

        # UI Elements
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        # Button Actions
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        """Handles login request."""
        username = self.input_username.text()
        password = self.input_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        # Send login request to Flask API
        response = requests.post(API_URL, json={"username": username, "password": password})
        data = response.json()

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Login successful!")
            self.close()  # Close login window after success
        else:
            QMessageBox.warning(self, "Error", data.get("message", "Login failed!"))

    def register(self):
        """Redirect to registration page."""
        QMessageBox.information(self, "Redirect", "Redirecting to registration...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
