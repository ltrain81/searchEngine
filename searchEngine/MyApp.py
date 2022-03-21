import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import MyWidget

class MyApp(QMainWindow):

    width = 1200
    length = 1200

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("background-color: white;")

    def initUI(self):
        self.menu()
        self.statusBar().showMessage('Home')
        self.setWindowTitle('KEP Intent/Entity Search Engine')
        self.setWindowIcon(QIcon('./icons/logo.png'))

        widget = MyWidget.MyWidget()
        self.setCentralWidget(widget)
        self.setGeometry(300, 300, self.width, self.length)
        self.show()

    def menu(self):
        #exit action
        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('ESC')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        #back action
        backAction = QAction(QIcon('./icons/back.png'), 'Back', self)
        backAction.setShortcut('Backspace')
        backAction.setStatusTip('Go back a page')
        backAction.triggered.connect(qApp.quit) #change this to back

        #save action
        saveAction = QAction(QIcon('./icons/save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+s')
        saveAction.setStatusTip('Save State')
        saveAction.triggered.connect(qApp.quit) #change this to save

        #print action
        printAction = QAction(QIcon('./icons/print.png'), 'Print', self)
        printAction.setShortcut('Ctrl+h')
        printAction.setStatusTip('Print Intents as CSV')
        printAction.triggered.connect(qApp.quit) #change this to print

        #status bar
        self.statusBar()
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        #menu options
        filemenu = menubar.addMenu('&File')
        editmenu = menubar.addMenu('&Edit')
        viewmenu = menubar.addMenu('&View')
        toolsmenu = menubar.addMenu('&Tools')
        helpmenu = menubar.addMenu('&Help')

        #add action to menu
        filemenu.addAction(backAction)
        filemenu.addAction(printAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(exitAction)

        self.statusBar()
        self.toolbar = self.addToolBar('Toolbar')
        self.setIconSize(QSize(50, 50))
        self.toolbar.addAction(backAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(printAction)
