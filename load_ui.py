from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
import sys






if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = uic.loadUi('./untitled.ui')
    ui.show()

    sys.exit(app.exec_())