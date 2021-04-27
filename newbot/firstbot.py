from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.conversation import Statement



#TSV formatted with a column header,
#ID\tQuestion\tAnswer
def trainFromTSV(chatbot, filename):

    #file should include a header row
    trainer = ListTrainer(chatbot, show_training_progress=False)
    
    datafile = open(filename, 'r')
    line = datafile.readline()
    isEnd = False
    linesTrained = 0
    while not isEnd:
        line = datafile.readline()
        if linesTrained%1000 == 0:
            print(linesTrained, "lines trained so far")
        if not line:
            isEnd = True
        else:
            linelist = line.split('\t')
            #remove ID field
            linelist.pop(0)
            linelist[1] = linelist[1].strip()
            #add question, add answer
            trainer.train(linelist)
            linesTrained += 1
    return linesTrained
                
def trainEnglishGreetings(chatbot):
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english.greetings")


def initializeBot(doTrain, datafile):
    chatbot = ChatBot(
        "CryptoCurrent",
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'botadapter.PriceAdapter'
            },
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I\'m not sure how to answer that',
                'maximum_similarity_threshold': 0.95
            }
            
        ],
        database_uri='sqlite:///database.sqlite3',
        read_only=True
    )

    if doTrain:
        print("using datafile", datafile)
        trainEnglishGreetings(chatbot)
        print("Lines trained", trainFromTSV(chatbot, datafile))
    
    return chatbot

def getResponse(chatbot, usrInput):

    try:
        bot_input = chatbot.get_response(usrInput)
        return bot_input
    except(ValueError):
        err = Statment(text='Please enter a response')
        return err
#    except Exception as e:
#        print(e)
#        return ("Encountered exception: \n\t" + str(e))
    return "Please enter a response"

