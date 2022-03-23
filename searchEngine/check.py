import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from PyQt5.QtCore import Qt
import MyWidget

def printClicked():
    MyWidget.checkedtoPrint.sort()
    intent = MyWidget.intent
    utterance = MyWidget.utterance
    index_to_print = []

    for i in range(len(MyWidget.checkedtoPrint)):
        index = MyWidget.intent["intentName"].index(MyWidget.checkedtoPrint[i])
        index_to_print.append(index)

    for index in index_to_print:
        utStart = intent["intStart"][index]
        utCount = intent["utterCnt"][index]
        df = utterance.loc[utStart:utStart+utCount-1]
        df.to_csv("./results/result_intent", mode='a', header = False)

    print("Print Finished!")

def on_checked():
    searchGrid = MyWidget.searchGrid
    for i in range(searchGrid.rowCount() - 2):
        cb = searchGrid.itemAtPosition(i+2, 0).widget()
        if cb.isChecked() is True:
            if cb.text() not in MyWidget.checkedtoPrint:
                MyWidget.checkedtoPrint.append(cb.text())
        else:
            if cb.text() in MyWidget.checkedtoPrint:
                MyWidget.checkedtoPrint.remove(cb.text())

