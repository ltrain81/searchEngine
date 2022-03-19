import sys
import os
import pandas as pd
import MyWidget as MW

class searchAlgo:

    global IntentsToPrint
    IntentsToPrint = []

    def start(programStatus):

        yesList = ['yes', 'y', 'sure', 'si', '네', '끝']
        noList = ['no', 'add', '추가', '더']

        intent = MW.intent
        entity = MW.entity

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


    def AddIntent(IntentName):
        #1. add by check
        #2. sort first, then add (alphabetical order)
        print(1)

    def print(IntentsToPrint):
        searchResult_entity = open('entResult.txt', 'w', encoding="utf-8") #write here - entity
        searchResult_intent = open('intResult.txt', 'w', encoding="utf-8") #write here - intent