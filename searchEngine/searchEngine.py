import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QMainWindow):

    width = 1200
    length = 1200
    #entity = pd.read_csv('Entity.csv', usecols=colsEnt[1:], encoding='UTF-8')
    #intent = pd.read_csv('Intent.csv', usecols=colsInt[1:], encoding='UTF-8')

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("background-color: white;")

    def initUI(self):
        self.menu()
        self.statusBar().showMessage('Home')
        self.setWindowTitle('KEP Intent/Entity Search Engine')
        self.setWindowIcon(QIcon('./icons/logo.png'))

        widget = MyWidget()
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

class MyWidget(QWidget):
    global checkBoxArr, entity, utterance, intent
    checkBoxArr = []
    colsEnt = pd.read_csv('Entity.csv', nrows = 1).columns #list of entity column names
    colsInt = pd.read_csv('Intent.csv', nrows = 1).columns #list of intent column names
    entity = pd.read_csv('Entity.csv', usecols=colsEnt[1:], encoding='UTF-8')
    utterance = pd.read_csv('Intent.csv', usecols=colsInt[1:], encoding='UTF-8')
    intent = {"intentName": [], "exampleSentence":[]}

    print(len(utterance))

    for i in range(len(utterance)):
        if utterance.loc[i][0] not in intent["intentName"]:
            intent["intentName"].append(utterance.loc[i][0])
            intent["exampleSentence"].append(utterance.loc[i][3])

    def __init__(self):
        super().__init__()
        self.buttons()
        self.layout()

    def buttons(self):
        global quitBtn, searchBtn, printBtn
        quitBtn = QPushButton('닫기')
        quitBtn.setIcon(QIcon('./icons/exit.png'))
        quitBtn.resize(quitBtn.sizeHint())
        quitBtn.clicked.connect(QCoreApplication.instance().quit)

        searchBtn = QPushButton('Search')
        searchBtn.setIcon(QIcon('./icons/Search_Icon.png'))
        searchBtn.resize(quitBtn.sizeHint())
        searchBtn.clicked.connect(self.search_clicked)

        printBtn = QPushButton('Print')
        printBtn.setIcon(QIcon('./icons/print.png'))
        printBtn.resize(quitBtn.sizeHint())
        printBtn.clicked.connect(QCoreApplication.instance().quit)

    def layout(self):

        #search Bar
        searchBar = QGridLayout()
        searchBar.addWidget(searchBtn, 0, 1)
        searchBar.addWidget(QLineEdit(), 0, 0)

        #search scroll
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollAreaContents = QWidget()
        searchGrid = QGridLayout(scrollAreaContents)
        scrollArea.setWidget(scrollAreaContents)

        for i in range(len(intent["intentName"])):
            cb = QCheckBox(str(intent["intentName"][i]))
            searchGrid.addWidget(cb, i+2, 0)
            searchGrid.addWidget(QLabel(intent["exampleSentence"][i]), i+2, 1)

        scrollBox = QHBoxLayout()
        scrollBox.addStretch(1)
        scrollBox.addWidget(scrollArea, 4)
        scrollBox.addStretch(1)

        #bottom box
        bottomBox = QHBoxLayout()
        bottomBox.addStretch(1)
        bottomButtons = QGridLayout()
        bottomButtons.addWidget(printBtn, 0, 0)
        bottomButtons.addWidget(quitBtn, 0, 1)
        bottomBox.addLayout(bottomButtons)
        bottomBox.addStretch(1)

        #top logo
        logo = QPixmap('./icons/logo.png')
        logo = logo.scaledToWidth(300)
        kakao_logo = QLabel()
        kakao_logo.setPixmap(QPixmap(logo))

        #가로 간격 조정
        logoBox = QHBoxLayout()
        logoBox.addStretch(1)
        logoBox.addWidget(kakao_logo)
        logoBox.addStretch(1)

        #main place
        hbox = QHBoxLayout()
        hbox.addStretch(3)
        hbox.addLayout(searchBar)
        hbox.addStretch(3)

        #세로 간격 조정
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(logoBox)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(scrollBox)
        vbox.addStretch(1)
        vbox.addLayout(bottomBox)

        self.setLayout(vbox)

    def search_clicked(self):
        searchAlgo.start(True)

    def image(path):
        pixmap = QPixmap(path)
        return QLabel(pixmap)

class searchAlgo:
    def start(programStatus):

        yesList = ['yes', 'y', 'sure', 'si', '네', '끝']
        noList = ['no', 'add', '추가', '더']

        searchResult_entity = open('entResult.txt', 'w', encoding="utf-8") #write here - entity
        searchResult_intent = open('intResult.txt', 'w', encoding="utf-8") #write here - intent

        colsEnt = pd.read_csv('Entity.csv', nrows = 1).columns #list of entity column names
        colsInt = pd.read_csv('Intent.csv', nrows = 1).columns #list of intent column names
        entity = pd.read_csv('Entity.csv', usecols=colsEnt[1:], encoding='UTF-8')
        intent = pd.read_csv('Intent.csv', usecols=colsInt[1:], encoding='UTF-8')

        while programStatus is True:
            text = input('Which Intent do you wish to find? : ').lower()
            print('Okay! We will find "{}" for you!'.format(text))
            j = 1
            print('\n')

            for i in range(len(entity)):
                while pd.notnull(entity.loc[i][j]):
                    if text in entity.loc[i][j].lower():
                        print(entity.loc[i])
                        break
                    if j == len(entity.loc[i]) - 1:
                        break
                    j+=1

            text_end = input('Will that be all for today?(y/n) : ').lower()
            while text_end not in yesList and noList:
                text_end = input('Please type y or n: ')

            if text_end in yesList:
                programStatus = False



if __name__ == "__main__":
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./fonts/KakaoRegular.ttf')
    app.setFont(QFont('KakaoRegular'))

    ex = MyApp()
    sys.exit(app.exec())