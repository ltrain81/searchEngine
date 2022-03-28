import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from PyQt5.QtCore import Qt
import MyWidget

def printClicked(fname):
    MyWidget.checkedtoPrint.sort()
    intent = MyWidget.intent
    utterance = MyWidget.utterance
    index_to_print = []

    for index in MyWidget.checkedtoPrint:
        utStart = intent["intStart"][index]
        utCount = intent["utterCnt"][index]
        df = utterance.loc[utStart:utStart+utCount-1]
        df.to_csv(fname, mode='a', header = False)

    print("Print Finished!")

