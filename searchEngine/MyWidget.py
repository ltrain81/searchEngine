from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import searchAlgo
import check


class MyWidget(QWidget):
    global entity, utterance, intent, checkedtoPrint
    colsEnt = pd.read_csv('Entity.csv', nrows = 1).columns #list of entity column names
    colsInt = pd.read_csv('Intent.csv', nrows = 1).columns #list of intent column names
    entity = pd.read_csv('Entity.csv', usecols=colsEnt[1:], encoding='UTF-8')
    utterance = pd.read_csv('Intent.csv', encoding='UTF-8')
    intent = {"intentName": [], "exampleSentence": [], "intStart": [], "utterCnt": []}
    checkedtoPrint = []

    utterCnt = 0
    for i in range(len(utterance)):
        utterCnt += 1
        #utterance's first column being the intent's name
        if utterance.loc[i][1] not in intent["intentName"]:
            intent["intentName"].append(utterance.loc[i][1])
            intent["exampleSentence"].append(utterance.loc[i][4])
            intent["intStart"].append(i)
            intent["utterCnt"].append(utterCnt)
            utterCnt = 0

    intent["utterCnt"].pop(0)

    def __init__(self):
        super().__init__()
        self.checkBoxes = []
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
        printBtn.clicked.connect(check.printClicked)

    def layout(self):
        #search Bar
        searchBar = QGridLayout()
        searchBar.addWidget(searchBtn, 0, 1)
        searchBar.addWidget(QLineEdit(), 0, 0)

        #search scroll
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollAreaContents = QWidget()
        self.searchGrid = QGridLayout(scrollAreaContents)
        scrollArea.setWidget(scrollAreaContents)

        for i in range(len(intent["intentName"])):
            cb = QCheckBox(str(intent["intentName"][i]))
            self.checkBoxes.append(cb)

        for i in range(len(self.checkBoxes)):
            self.checkBoxes[i].stateChanged.connect(check.on_checked)
            self.checkBoxes[i].setChecked(Qt.Unchecked)
            self.searchGrid.addWidget(self.checkBoxes[i], i+2, 0)
            self.searchGrid.addWidget(QLabel(intent["exampleSentence"][i]), i+2, 1)

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
        vbox.addLayout(logoBox, 1)
        vbox.addLayout(hbox, 2)
        vbox.addLayout(scrollBox, 5)
        vbox.addLayout(bottomBox, 1)

        self.setLayout(vbox)


    def on_checked(self):
        searchGrid = self.searchGrid
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            if cb.isChecked() is True:
                if cb.text() not in checkedtoPrint:
                    checkedtoPrint.append(cb.text())
            else:
                if cb.text() in checkedtoPrint:
                    checkedtoPrint.remove(cb.text())


    def search_clicked(self, state):

        print(checkedtoPrint)