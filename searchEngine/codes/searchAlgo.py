import sys
import os
import pandas as pd
import MyWidget as MW
from PyQt5.QtWidgets import *

class searchAlgo:

    def IntentSearch(text):
        input = text.lower()
        searchResultIndex = []

        intent = MW.intent
        utterance = MW.utterance

        for i in range(len(intent["intentName"])):
            intentName = intent["intentName"][i]
            if input in intentName:
                searchResultIndex.append(i)
            else:
                for j in range(intent["utterCnt"][i]):
                    utIndex = (intent["intStart"][i]) + j
                    if input in utterance.loc[utIndex][4]:
                        searchResultIndex.append(i)
                        MW.exampleSentence[i] = QLabel(utterance.loc[utIndex][4])
                        break

        return searchResultIndex