from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import searchAlgo
import check


class MyWidget(QWidget):
    global entity, utterance, intent, checkedtoPrint, exampleSentence

    utterance = pd.read_csv('Intent.csv', encoding='UTF-8')
    intent = {"intentName": [], "exampleSentence": [], "intStart": [], "utterCnt": []}
    checkedtoPrint = []
    exampleSentence = []

    utterCnt = 0
    for i in range(len(utterance)):
        utterCnt += 1
        #utterance's first column being the intent's name
        intentName = utterance.loc[i][0] + "_" + utterance.loc[i][1]
        intentName = intentName.lower()
        if intentName not in intent["intentName"]:
            intent["intentName"].append(intentName)
            intent["exampleSentence"].append(utterance.loc[i][4])
            intent["intStart"].append(i)
            intent["utterCnt"].append(utterCnt)
            utterCnt = 0

    #j : index for the start point in utterance of last intent
    utterCnt = 0
    j = intent["intStart"][len(intent["intentName"]) -1]
    for i in range(j, len(utterance)):
        utterCnt += 1
    intent["utterCnt"].append(utterCnt)

    intent["utterCnt"].pop(0)


    def __init__(self):
        super().__init__()
        self.checkBoxes = []
        self.searchedIndex = []
        self.buttons()
        self.layout()


    def buttons(self):
        global quitBtn, searchBtn, printBtn, showOptionBox, selectAllBtn, deselectBtn
        quitBtn = QPushButton('닫기')
        quitBtn.setIcon(QIcon('./icons/exit.png'))
        quitBtn.setBaseSize(50, 20)
        quitBtn.clicked.connect(QCoreApplication.instance().quit)

        searchBtn = QPushButton('Search')
        searchBtn.setIcon(QIcon('./icons/Search_Icon.png'))
        searchBtn.resize(quitBtn.sizeHint())
        searchBtn.clicked.connect(self.search_clicked)

        printBtn = QPushButton('Print')
        printBtn.setIcon(QIcon('./icons/print.png'))
        printBtn.resize(quitBtn.sizeHint())
        printBtn.clicked.connect(check.printClicked)

        showOptionBox = QComboBox(self)
        showOptionBox.addItem('모든 항목 표시')
        showOptionBox.addItem('선택 항목 숨김')
        showOptionBox.addItem('선택 항목만 표시')
        showOptionBox.resize(quitBtn.sizeHint())
        showOptionBox.currentIndexChanged.connect(self.comboBoxFunc)

        selectAllBtn = QPushButton('모두 선택', self)
        selectAllBtn.clicked.connect(self.selectAll)

        deselectBtn = QPushButton('전체 해제', self)
        deselectBtn.clicked.connect(self.deselectAll)
        deselectBtn.move(400, 0)


    def layout(self):
        #search Bar
        searchBar = QGridLayout()
        searchBar.addWidget(searchBtn, 0, 1)
        self.searchText = QLineEdit()
        self.searchText.setBaseSize(60, 20)
        self.searchText.returnPressed.connect(self.search_clicked)
        searchBar.addWidget(self.searchText, 0, 0)

        #search scroll
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollAreaContents = QWidget()
        self.searchGrid = QGridLayout(scrollAreaContents)
        scrollArea.resize(self.searchGrid.sizeHint())
        scrollArea.setWidget(scrollAreaContents)

        for i in range(len(intent["intentName"])):
            cb = QCheckBox(str(intent["intentName"][i]))
            cb.resize(quitBtn.sizeHint())
            self.checkBoxes.append(cb)
            sent = QLabel(intent["exampleSentence"][i])
            sent.resize(quitBtn.sizeHint())
            #sent.setMaximumHeight(20)
            exampleSentence.append(sent)

        for i in range(len(self.checkBoxes)):
            self.checkBoxes[i].stateChanged.connect(self.on_checked)
            self.checkBoxes[i].setChecked(Qt.Unchecked)
            self.searchGrid.addWidget(self.checkBoxes[i], i+2, 0, Qt.AlignTop)
            self.searchGrid.addWidget(exampleSentence[i], i+2, 1, Qt.AlignTop)

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

        #optionBox
        optionBox = QHBoxLayout()
        optionBox.addStretch(1)
        optionBox.addWidget(selectAllBtn)
        optionBox.addWidget(deselectBtn)
        optionBox.addStretch(2)
        optionBox.addWidget(showOptionBox)
        optionBox.addStretch(1)

        #세로 간격 조정
        vbox = QVBoxLayout()
        vbox.addLayout(logoBox, 1)
        vbox.addLayout(hbox, 2)
        vbox.addLayout(optionBox, 1)
        vbox.addLayout(scrollBox, 5)
        vbox.addLayout(bottomBox, 1)

        self.setLayout(vbox)

    def on_checked(self):
        searchGrid = self.searchGrid
        option = showOptionBox.currentIndex()
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if cb.isChecked() is True:
                if cb.text() not in checkedtoPrint:
                    checkedtoPrint.append(cb.text())
                if option == 1:
                    cb.setHidden(True)
                    utter.setHidden(True)
            else:
                if cb.text() in checkedtoPrint:
                    checkedtoPrint.remove(cb.text())
                if option == 2:
                    cb.setHidden(True)
                    utter.setHidden(True)


    def search_clicked(self):
        input = self.searchText.text()
        self.searchedIndex = searchAlgo.searchAlgo.IntentSearch(input)
        searchGrid = self.searchGrid

        option = showOptionBox.currentIndex()
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if option == 0:
                if i in self.searchedIndex:
                    cb.setHidden(False)
                    utter.setText(exampleSentence[i].text())
                    utter.setHidden(False)
                else:
                    cb.setHidden(True)
                    utter.setHidden(True)
            elif option == 1: #선택 항목 제외
                if cb.isChecked() == False and i in self.searchedIndex:
                    cb.setHidden(False)
                    utter.setText(exampleSentence[i].text())
                    utter.setHidden(False)
                else:
                    cb.setHidden(True)
                    utter.setHidden(True)
            elif option == 2: #선택항목만 표시
                if cb.isChecked() == True and i in self.searchedIndex:
                    cb.setHidden(False)
                    utter.setText(exampleSentence[i].text())
                    utter.setHidden(False)
                else:
                    cb.setHidden(True)
                    utter.setHidden(True)


    def comboBoxFunc(self):
        self.search_clicked()

    def selectAll(self):
        searchGrid = self.searchGrid
        option = showOptionBox.currentIndex()
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if cb.isHidden() is False and cb.isChecked() is False: #not hidden -> check & add
                cb.toggle()
                checkedtoPrint.append(cb.text())
                if option == 1:
                    cb.setHidden(True)
                    utter.setHidden(True)


    def deselectAll(self):
        searchGrid = self.searchGrid
        option = showOptionBox.currentIndex()
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if cb.isHidden() is False and cb.isChecked() is True: #not hidden -> check
                cb.toggle()
                checkedtoPrint.remove(cb.text())
                if option == 2:
                    cb.setHidden(True)
                    utter.setHidden(True)


''''
    def hideSelected(self):
        searchGrid = self.searchGrid

        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if cb.text() in checkedtoPrint:
                cb.setHidden(True)
                utter.setHidden(True)
            else:
                cb.setHidden(False)
                utter.setHidden(False)

    def showSelected(self):
        searchGrid = self.searchGrid

        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if cb.text() not in checkedtoPrint:
                cb.setHidden(True)
                utter.setHidden(True)
            else:
                cb.setHidden(False)
                utter.setHidden(False)

    def showAll(self):
        searchGrid = self.searchGrid

        for i in range(searchGrid.rowCount() -2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if cb.isHidden() is True:
                cb.setHidden(False)
                utter.setHidden(False)
'''