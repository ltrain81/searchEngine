import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import MyWidget
import check

basedir = os.path.dirname(__file__)

class MyApp(QMainWindow):

    width = 1200
    length = 1200

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("background-color: white;")

    def initUI(self):
        self.menu()
        self.statusBar().showMessage('slee.w')
        self.setWindowTitle('KEP Intent/Entity Search Engine')
        self.setWindowIcon(QIcon(os.path.join(basedir, "icons", "logo.png")))
        self.setGeometry(300, 300, self.width, self.length)

        self.show()

        widget = MyWidget.MyWidget()
        self.setCentralWidget(widget)

    def menu(self):
        #exit action
        exitAction = QAction(QIcon(os.path.join(basedir, "icons", "exit.png")), 'Exit', self)
        exitAction.setShortcut('ESC')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        #print action
        printAction = QAction(QIcon('os.path.join(basedir, "icons", "print.png")'), 'Print', self)
        printAction.setShortcut('Ctrl+h')
        printAction.setStatusTip('Print Intents as CSV')
        printAction.triggered.connect(check.printClicked) #change this to print

        #status bar
        self.statusBar()
        menubar = self.menuBar()
        menubar.setStyleSheet("color: black")
        menubar.setNativeMenuBar(False)

        #menu options
        filemenu = menubar.addMenu('&File')
        editmenu = menubar.addMenu('&Edit')
        viewmenu = menubar.addMenu('&View')
        toolsmenu = menubar.addMenu('&Tools')
        helpmenu = menubar.addMenu('&Help')

        #add action to menu
        filemenu.addAction(printAction)
        filemenu.addAction(exitAction)

        self.statusBar()
