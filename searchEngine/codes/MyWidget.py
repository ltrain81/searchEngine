from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import searchAlgo
import check
import os

basedir = os.path.dirname(__file__)

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()

        global entity, utterance, intent, checkedtoPrint, exampleSentence

        self.checkBoxes = []
        self.searchedIndex = []
        self.cbShow = []
        self.searchText = []
        self.category_to_show = []
        self.option_to_show = []
        checkedtoPrint = []
        exampleSentence = []
        entity = []

        filePath = self.openFile()
        utterance = pd.read_csv(filePath, encoding='UTF-8')
        intent = {"intentName": [], "exampleSentence": [], "category": [], "intStart": [], "utterCnt": []}

        utterCnt = 0
        for i in range(len(utterance)):
            utterCnt += 1
            #utterance's first column being the intent's name
            intentName = utterance.loc[i][0] + "_" + utterance.loc[i][1]
            intentName = intentName.lower()
            if intentName not in intent["intentName"]:
                intent["intentName"].append(intentName)
                intent["exampleSentence"].append(utterance.loc[i][4])
                intent["category"].append(utterance.loc[i][2])
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

        self.buttons()
        self.layout()


    def buttons(self):
        global quitBtn, searchBtn, printBtn, showOptionBox, categoryBox, selectAllBtn, deselectBtn
        quitBtn = QPushButton('닫기')
        quitBtn.setStyleSheet("color: black")
        quitBtn.setIcon(QIcon(os.path.join(basedir, "icons", "exit.png")))
        quitBtn.clicked.connect(QCoreApplication.instance().quit)

        searchBtn = QPushButton('Search')
        searchBtn.setIcon(QIcon(os.path.join(basedir, "icons", "Search_Icon.png")))
        searchBtn.setStyleSheet("color: black")
        searchBtn.clicked.connect(self.search_clicked)

        printBtn = QPushButton('Print')
        printBtn.setStyleSheet("color: black")
        printBtn.setIcon(QIcon(os.path.join(basedir, "icons", "print.png")))
        printBtn.clicked.connect(self.saveFile)

        showOptionBox = QComboBox(self)
        showOptionBox.addItem('모든 항목 표시')
        showOptionBox.addItem('선택 항목 숨김')
        showOptionBox.addItem('선택 항목만 표시')
        showOptionBox.setStyleSheet("color: black")
        showOptionBox.currentIndexChanged.connect(self.option_changed)

        categoryBox = QComboBox(self)
        categoryBox.setStyleSheet("color: black")
        categoryBox.addItem('전체')
        includedCategory = []
        for category in intent["category"]:
            if category not in includedCategory:
                categoryBox.addItem(category)
                includedCategory.append(category)
            else:
                pass
        categoryBox.currentIndexChanged.connect(self.categoryChanged)


        selectAllBtn = QPushButton('모두 선택', self)
        selectAllBtn.setStyleSheet("color: black")
        selectAllBtn.clicked.connect(self.selectAll)
        deselectBtn = QPushButton('전체 해제', self)
        deselectBtn.setStyleSheet("color: black")
        deselectBtn.clicked.connect(self.deselectAll)
        deselectBtn.move(400, 0)


    def layout(self):
        #search Bar
        searchBar = QGridLayout()
        searchBar.addWidget(searchBtn, 0, 1)
        self.searchText = QLineEdit()
        self.searchText.setStyleSheet("color: black")
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
            cb.setStyleSheet("color: black")
            self.checkBoxes.append(cb)
            sent = QLabel(intent["exampleSentence"][i])
            sent.setStyleSheet("color: black")
            exampleSentence.append(sent)
            self.cbShow.append(i)
            self.searchedIndex.append(i)
            self.category_to_show.append(i)
            self.option_to_show.append(i)

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
        logo = QPixmap(os.path.join(basedir, "icons", "logo.png"))
        logo = logo.scaledToHeight(100, Qt.SmoothTransformation)
        head_logo = QLabel()
        head_logo.setPixmap(logo)

        #bottom logo
        logo_2 = QPixmap(os.path.join(basedir, "icons", "kakao.png"))
        logo_2 = logo_2.scaledToHeight(20, Qt.SmoothTransformation)
        kakao_logo = QLabel()
        kakao_logo.setPixmap(logo_2)

        #가로 간격 조정
        logoBox = QHBoxLayout()
        logoBox.addStretch(1)
        logoBox.addWidget(kakao_logo)
        logoBox.addWidget(head_logo)
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
        optionBox.addWidget(categoryBox)
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
                    checkedtoPrint.append(i)
            else:
                if cb.text() in checkedtoPrint:
                    checkedtoPrint.remove(i)

        self.option_changed()

    def search_clicked(self):
        input = self.searchText.text()
        self.searchedIndex = searchAlgo.searchAlgo.IntentSearch(input)
        self.showCB()

    def categoryChanged(self):
        #intent["category"] 와 cb 순서가 같은 점을 이용해 인덱스로 활용
        current_category = categoryBox.currentText()
        searchGrid = self.searchGrid

        for i in range(searchGrid.rowCount() - 2):
            if current_category == '전체' and i not in self.category_to_show:
                self.category_to_show.append(i)
            elif current_category != '전체':
                print(current_category)
                if intent["category"][i] == current_category and i not in self.category_to_show:
                    self.category_to_show.append(i)
                elif intent["category"][i] != current_category and i in self.category_to_show:
                    self.category_to_show.remove(i)

        self.showCB()

    def selectAll(self):
        searchGrid = self.searchGrid
        option = showOptionBox.currentIndex()
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            if cb.isHidden() is False and cb.isChecked() is False: #not hidden -> check & add
                checkedtoPrint.append(i)
                cb.toggle()

        self.showCB()

    def deselectAll(self):
        #fix here
        searchGrid = self.searchGrid
        option = showOptionBox.currentIndex()
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            if cb.isHidden() is False and cb.isChecked() is True: #not hidden & checkecked
                checkedtoPrint.remove(i)
                cb.toggle()

        self.showCB()

    def option_changed(self):
        option = showOptionBox.currentIndex()
        searchGrid = self.searchGrid
        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if option == 0: #전체 보임
                if i not in self.option_to_show:
                    self.option_to_show.append(i)
            elif option == 1: #선택 항목 숨김
                if cb.isChecked() is True and i in self.option_to_show:
                    self.option_to_show.remove(i)
                elif cb.isChecked() is False and i not in self.option_to_show:
                    self.option_to_show.append(i)
            else: #선택 항목 표시
                if cb.isChecked() is True and i not in self.option_to_show:
                    self.option_to_show.append(i)
                elif cb.isChecked() is False and i in self.option_to_show:
                    self.option_to_show.remove(i)

        self.showCB()



    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'file', './')
        return fname[0]

    def saveFile(self):
        fname = QFileDialog.getSaveFileName(self, 'save', './')
        check.printClicked(fname[0])

    def showCB(self):
        #교집합 찾아서 해당 항목들만 출력한다.
        option = showOptionBox.currentIndex()
        searchGrid = self.searchGrid

        self.cbShow = set(self.searchedIndex) & set(self.category_to_show) & set(self.option_to_show)

        print("\n")
        print(self.searchedIndex)
        print(self.category_to_show)
        print(self.option_to_show)
        print(self.cbShow)

        for i in range(searchGrid.rowCount() - 2):
            cb = self.searchGrid.itemAtPosition(i+2, 0).widget()
            utter = self.searchGrid.itemAtPosition(i+2, 1).widget()
            if i in self.cbShow:
                cb.show()
                utter.show()
                self.cbShow.remove(i)
            else:
                cb.hide()
                utter.hide()