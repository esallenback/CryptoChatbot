from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk
from nltk.tokenize import word_tokenize




def tsvToList(filename):
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

def tsvTo2DList(filename):
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
                linelist.pop(0)
                linelist[1] = linelist[1].strip()
                #add question, add answer
                conversationList.append(linelist)
        
        return conversationList

def trainChatbot(chatbot, filename):

    trainingList = tsvToList(filename)
    print("List size: ", len(trainingList))

    trainer = ListTrainer(chatbot)

    trainer.train(trainingList)

def botInit():
    chatbot = ChatBot(
        "CryptoCurrent",
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        read_only=True
    )

    datafile = "chatbot-development12.tsv"

    print("using datafile", datafile)
    trainChatbot(chatbot, datafile)
    
    return chatbot    
    
    notDone = True
    print("Talk to me, or 'exit' to stop")
    while notDone:
        try:
            userResponse = input(">>")
            if userResponse == "exit":
                notDone = False
                print("goodbye!")
            else:
                bot_input = chatbot.get_response(userResponse)
                print(bot_input)
                if(bot_input=="No value for search_text was available on the provided input"):
                    raise ValueError("No message given")
        except(KeyboardInterrupt, EOFError, SystemExit):
            notDone = False
            print("oh, bye then!")
        except(ValueError):
            print("Hello? Anyone there?")
        except:
            print("uh oh! exception thrown")
            notDone = True

def respond(input):
    response = cryptobot.get_response(input)
    return nltk.tokenize.word_tokenize(str(response))
