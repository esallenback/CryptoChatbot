from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
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

def main():
    chatbot = ChatBot(
        "CryptoCurrent",
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        read_only=True
    )

    datafile = "chatbot-development12.tsv"
    trainingList = tsvTo2DList(datafile)

    ans = input("Train? (y/n): ")
    if ans.lower()=='y':
        print("using datafile", datafile)
        trainChatbot(chatbot, datafile)
    elif ans.lower() != 'n':
        print("y/n only please")
        return 1
    
    
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
        except(KeyboardInterrupt, EOFError, SystemExit):
            notDone = False
            print("oh, bye then!")

main()