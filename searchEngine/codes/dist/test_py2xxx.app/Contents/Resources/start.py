import sys
import pandas as pd
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import MyApp

if __name__ == "__main__":

    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./fonts/KakaoRegular.ttf')
    app.setFont(QFont('KakaoRegular'))
    ex = MyApp.MyApp()
    sys.exit(app.exec_())
