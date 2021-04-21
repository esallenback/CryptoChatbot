import os
import sys
import csv
import time
import pandas as pd
from dateutil import parser as date_parser
from chatterbot.conversation import Statement
from chatterbot.tagging import PosLemmaTagger
from chatterbot import utils


#currently reads the 
class CryptoTrainer(Trainer):
    
    # Accepts a tab separated value (.tsv) file formatted
    # id, question, answer
    
    def train(self, filename):
        dataset = tsvToList(filename)
        

    def tsvToList(self, filename):
        conversationList = []
        #file should include a header row
        
        datafile = open(filename, 'r')
        line = datafile.readline()
        isEnd = False
        while not isEnd:
            line = datafile.readline()
            if not line:
                isEnd = True
            else:
                linelist = line.split('\t')
                #add question, add answer
                conversationList.append(linelist[1])
                conversationList.append(linelist[2])
        
        return conversationList

    def tsvTo2DList(self, filename):
        conversationList = []
        #file should include a header row
        
        datafile = open(filename, 'r')
        line = datafile.readline()
        isEnd = False
        while not isEnd:
            line = datafile.readline()
            if not line:
                isEnd = True
            else:
                linelist = line.split('\t')
                #remove ID field
                linelist.remove(0)
                #add question, add answer
                conversationList.append(linelist)
        
        return conversationList