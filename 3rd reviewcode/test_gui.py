from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from jarvisSuperUI import Ui_Form

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = Main()
    jarvis.show()
    sys.exit(app.exec_())
