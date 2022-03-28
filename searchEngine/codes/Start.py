import sys
import pandas as pd
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import MyApp

basedir = os.path.dirname(__file__)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = MyApp.MyApp()
    sys.exit(app.exec_())