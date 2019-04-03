from PySide2.QtCore import * 
from PySide2.QtWidgets import * 
from PySide2.QtGui import * 

from mainwindow import MainWindow

import sys

app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()