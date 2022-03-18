import sys
import pandas as pd


def start():

    yesList = ['yes', 'y', 'sure', 'si', '네', '끝']
    noList = ['no', 'add', '추가', '더']

    searchResult_entity = open('entResult.txt', 'w', encoding="utf-8") #write here - entity
    searchResult_intent = open('intResult.txt', 'w', encoding="utf-8") #write here - intent

    colsEnt = pd.read_csv('Entity.csv', nrows = 1).columns #list of entity column names
    colsInt = pd.read_csv('Intent.csv', nrows = 1).columns #list of intent column names
    entity = pd.read_csv('Entity.csv', usecols=colsEnt[1:], encoding='UTF-8')
    intent = pd.read_csv('Intent.csv', usecols=colsInt[1:], encoding='UTF-8')
    programStatus = True

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
